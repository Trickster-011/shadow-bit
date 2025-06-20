import os
import openai
import json
import time
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Rutas de proyecto
json_path = "js/posts.json"
output_folder = "posts"
image_folder = "img"

# Plantilla HTML base
HTML_TEMPLATE = """
<article class="post">
  <img src="{img_path}" alt="{img_alt}" style="width: 100%; border-radius: 8px; margin-bottom: 20px;">
  <h2>{titulo}</h2>
  {contenido}
</article>
"""

def generar_imagen(titulo):
    prompt = f"A pixel-art style illustration for an article titled '{titulo}' about gaming, in a retro aesthetic, suitable for a blog header."
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url

def generar_articulo(tema):
    prompt = f"""Genera un artículo detallado, con encabezado atractivo, sobre el tema: "{tema}". El formato debe ser HTML, debe tener una estructura narrativa clara, con múltiples subtítulos (h2/h3), tabla si aplica, datos reales, profundidad en las explicaciones y un momento especial para incluir la frase 'Trickster’s Pick'. El tono debe ser serio pero con estilo gamer amigable, y estar optimizado para blog."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def actualizar_json(titulo, resumen, categorias, id_articulo):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.insert(0, {
        "id": id_articulo,
        "titulo": titulo,
        "resumen": resumen,
        "categorias": categorias
    })

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def guardar_html(id_articulo, titulo, contenido, img_filename):
    html = HTML_TEMPLATE.format(titulo=titulo, contenido=contenido, img_path=f"img/{img_filename}", img_alt=titulo)
    file_path = os.path.join(output_folder, f"{id_articulo}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

def main():
    tema = input("Tema del artículo: ").strip()
    id_articulo = f"articulo{int(time.time())}"
    titulo = input("Título visible del artículo: ").strip()
    resumen = input("Resumen corto del artículo: ").strip()
    categorias = input("Categorías (coma separadas): ").strip().split(",")

    print("Generando artículo...")
    contenido_html = generar_articulo(tema)

    print("Generando imagen...")
    image_url = generar_imagen(titulo)
    img_filename = f"{id_articulo}.png"
    img_path = os.path.join(image_folder, img_filename)
    os.system(f"curl -o {img_path} {image_url}")

    print("Guardando archivo...")
    guardar_html(id_articulo, titulo, contenido_html, img_filename)
    actualizar_json(titulo, resumen, categorias, id_articulo)
    print(f"Artículo '{titulo}' creado con éxito como {id_articulo}.html")

if __name__ == "__main__":
    main()
