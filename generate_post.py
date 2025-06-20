
from datetime import datetime
import os
import json
import re

# Rutas
POSTS_DIR = "posts"
IMG_DIR = "img"
JSON_PATH = "js/posts.json"

# Asegurar que las carpetas existen
os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# Utilidad para slug
def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", '', text)
    return re.sub(r"[\s_]+", '-', text).strip("-")

# Leer posts.json
def cargar_json():
    if not os.path.exists(JSON_PATH):
        return []
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Obtener próximo ID
def siguiente_id(posts):
    existentes = [int(p["id"].replace("articulo", "")) for p in posts if p["id"].startswith("articulo")]
    return max(existentes, default=0) + 1

# Generar HTML básico
def generar_html(titulo, resumen, imagen_path):
    return f"""<article class="post">
  <img src="{imagen_path}" alt="{titulo}" style="width: 100%; border-radius: 8px; margin-bottom: 20px;">
  <h2>{titulo}</h2>
  <p>{resumen}</p>
  <h3>1. Curiosidad profunda</h3>
  <p>Aquí se desarrollará una curiosidad detallada basada en el tema del artículo.</p>
  <h3>2. Otra curiosidad destacada</h3>
  <p>Contenido profundo siguiendo el estilo narrativo del artículo de Red Dead Redemption 2.</p>
  <p><strong>Trickster’s Pick:</strong> Un detalle oculto que convierte el artículo en una joya para los gamers atentos.</p>
</article>"""

# Guardar nuevo artículo e imagen
def guardar_articulo(articulo_id, html_content, titulo, resumen, categorias):
    filename = f"articulo{articulo_id}.html"
    filepath = os.path.join(POSTS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Guardar imagen falsa como marcador
    imagen_destino = os.path.join(IMG_DIR, f"articulo{articulo_id}.png")
    with open(imagen_destino, "wb") as f:
        f.write(b"")

    # Actualizar JSON
    posts = cargar_json()
    posts.append({
        "id": f"articulo{articulo_id}",
        "titulo": titulo,
        "resumen": resumen,
        "categorias": categorias
    })
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    return filename, f"img/articulo{articulo_id}.png"

# Script principal
def main():
    print("=== Shadow-Bit: Generador de artículos ===")
    titulo = input("Título o tema del artículo: ").strip()
    resumen = input("Resumen breve para portada (SEO): ").strip()
    categorias = input("Categorías (separadas por coma): ").strip().split(",")

    posts = cargar_json()
    nuevo_id = siguiente_id(posts)
    imagen_path = f"img/articulo{nuevo_id}.png"

    html = generar_html(titulo, resumen, imagen_path)
    archivo, img = guardar_articulo(nuevo_id, html, titulo, resumen, [c.strip() for c in categorias])

    print(f"\n✅ Artículo guardado como: {archivo}")
    print(f"🖼 Imagen esperada: {img}")
    print("📘 posts.json actualizado correctamente.")

if __name__ == "__main__":
    main()
