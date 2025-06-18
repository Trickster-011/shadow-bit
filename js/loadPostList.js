let posts = [];
let currentCategory = "";

// Esperar hasta que #post-list exista en el DOM
const esperarElemento = (selector, callback) => {
  const elemento = document.querySelector(selector);
  if (elemento) {
    callback();
  } else {
    setTimeout(() => esperarElemento(selector, callback), 100); // intenta de nuevo
  }
};

function iniciarPostList() {
  fetch("js/posts.json")
    .then(res => res.json())
    .then(data => {
      posts = data;
      renderPosts(posts);
      renderCategories(posts);
    });
}

function renderPosts(postArray) {
  const container = document.getElementById("post-list");
  if (!container) return;
  container.innerHTML = "";

  postArray.forEach(post => {
    if (currentCategory && !post.categorias.includes(currentCategory)) return;

    const section = document.createElement("section");
    section.classList.add("post-preview");

    section.innerHTML = `
      <h2>${post.titulo}</h2>
      <p>${post.resumen}</p>
      <a href="post.html?id=${post.id}">Leer más</a>
    `;

    container.appendChild(section);
  });
}

function renderCategories(postArray) {
  const container = document.getElementById("categoria-filtros");
  if (!container) return;
  const categorias = new Set();

  postArray.forEach(post => post.categorias.forEach(cat => categorias.add(cat)));

  container.innerHTML = `<button onclick="filterByCategory('')">Todas</button>`;
  categorias.forEach(cat => {
    container.innerHTML += `<button onclick="filterByCategory('${cat}')">${cat}</button>`;
  });
}

function filterByCategory(cat) {
  currentCategory = cat;
  renderPosts(posts);
}

// Buscador
document.addEventListener("input", e => {
  if (e.target.id === "searchInput") {
    const texto = e.target.value.toLowerCase();
    const filtrados = posts.filter(post =>
      post.titulo.toLowerCase().includes(texto) || post.resumen.toLowerCase().includes(texto)
    );
    renderPosts(filtrados);
  }
});

// Ejecutar solo cuando exista #post-list
esperarElemento("#post-list", iniciarPostList);
