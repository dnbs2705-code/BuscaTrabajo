import os
import time
from google import genai
from google.genai.errors import ServerError, APIError

client = genai.Client()

def adaptar_cv(archivo_cv_maestro, archivo_oferta, archivo_salida_md):
    if not os.path.exists(archivo_cv_maestro):
        print(f"Error: No se encontró el CV maestro {archivo_cv_maestro}")
        return
    if not os.path.exists(archivo_oferta):
        print(f"Error: No se encontró el archivo de la oferta {archivo_oferta}")
        return

    with open(archivo_cv_maestro, 'r', encoding='utf-8') as f:
        cv_texto = f.read()

    with open(archivo_oferta, 'r', encoding='utf-8') as f:
        oferta_texto = f.read()

    prompt = f"""
    Eres un experto en reclutamiento y optimización de CVs para sistemas ATS.
    Tu tarea es adaptar el siguiente CV Maestro a la oferta de trabajo indicada.

    REGLAS ESTRICTAS:
    1. NO inventes experiencia, datos de contacto, empresas ni fechas.
    2. Mantén exactamente la estructura ATS en formato texto plano/Markdown.
    3. Reordena y ajusta la redacción de las funciones para resaltar las palabras clave de la oferta.
    4. Devuelve SOLO el texto del CV adaptado, sin comentarios ni introducciones.

    CV MAESTRO:
    {cv_texto}

    OFERTA DE TRABAJO:
    {oferta_texto}
    """

    print("🤖 Procesando adaptación con IA...")

    # Intentos de llamada a la API con pausa preventiva si hay error 503
    max_intentos = 3
    for intento in range(1, max_intentos + 1):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-lite',
                contents=prompt,
            )
            with open(archivo_salida_md, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"✅ CV adaptado guardado en: {archivo_salida_md}")
            break
        except (ServerError, APIError) as e:
            if intento < max_intentos:
                print(f"⚠️ Servidor ocupado (intento {intento}/{max_intentos}). Reintentando en 5 segundos...")
                time.sleep(5)
            else:
                print("❌ No se pudo completar la solicitud por alta demanda en el servidor. Intenta de nuevo en unos momentos.")
                raise e

if __name__ == "__main__":
    adaptar_cv("cv_santiago.md", "oferta.txt", "cv_santiago_adaptado.md")

