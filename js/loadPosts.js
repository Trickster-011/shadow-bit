// js/loadPosts.js
const posts = ["articulo1.html"];
const contentContainer = document.getElementById("content");

posts.forEach(postFile => {
  fetch(`posts/${postFile}`)
    .then(res => res.text())
    .then(html => {
      const div = document.createElement("div");
      div.innerHTML = html;
      contentContainer.appendChild(div);
    });
});