import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generar_articulo_y_datos(tema):
    prompt = f"""Eres un redactor experto en blogs de videojuegos. Basado en los artículos anteriores del blog 'Shadow-Bit',
genera un artículo largo y detallado en formato HTML, estilo narrativo con título, imagen, y curiosidades si aplica,
y siempre incluye el sello 'Trickster's Pick'. El tema es: {tema}. Al final, genera un resumen SEO y hasta 3 categorías.
Devuelve el resultado en este formato exacto:
===HTML===
[contenido HTML]
===RESUMEN===
[resumen para el JSON]
===CATEGORIAS===
[categoría1, categoría2]
"""

    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    texto = respuesta.choices[0].message.content
    partes = texto.split("===RESUMEN===")
    html = partes[0].replace("===HTML===", "").strip()
    resumen_data = partes[1].strip().split("===CATEGORIAS===")
    resumen = resumen_data[0].strip()
    categorias = [c.strip() for c in resumen_data[1].split(",")]

    return html, resumen, categorias

def guardar_articulo(id_articulo, titulo, html):
    ruta = f"posts/{id_articulo}.html"
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[✓] Artículo guardado como {ruta}")

def actualizar_json(id_articulo, titulo, resumen, categorias):
    ruta_json = "js/posts.json"
    if not os.path.exists(ruta_json):
        print("[!] posts.json no encontrado.")
        return

    with open(ruta_json, "r", encoding="utf-8") as f:
        datos = json.load(f)

    datos.insert(0, {
        "id": id_articulo,
        "titulo": titulo,
        "resumen": resumen,
        "categorias": categorias
    })

    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    print(f"[✓] posts.json actualizado.")

def main():
    tema = input("Tema del nuevo artículo: ").strip()
    id_articulo = f"articulo_auto"
    titulo = tema.title()

    print("[...] Generando contenido con IA...")
    html, resumen, categorias = generar_articulo_y_datos(tema)
    guardar_articulo(id_articulo, titulo, html)
    actualizar_json(id_articulo, titulo, resumen, categorias)

if __name__ == "__main__":
    main()