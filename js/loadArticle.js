// js/loadArticle.js

function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

const articleId = getQueryParam("id");

if (articleId) {
  fetch(`posts/${articleId}.html`)
    .then(res => {
      if (!res.ok) throw new Error("Artículo no encontrado.");
      return res.text();
    })
    .then(html => {
      document.getElementById("article-content").innerHTML = html;
    })
    .catch(err => {
      document.getElementById("article-content").innerHTML = `<p>${err.message}</p>`;
    });
} else {
  document.getElementById("article-content").innerHTML = "<p>ID de artículo no proporcionado.</p>";
}
