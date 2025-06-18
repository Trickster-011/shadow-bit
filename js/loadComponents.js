// js/loadComponents.js
function loadComponent(id, file) {
  fetch(file)
    .then(res => res.text())
    .then(data => {
      document.getElementById(id).innerHTML = data;
    });
}

loadComponent("header", "components/header.html");
loadComponent("content", "components/home.html");
loadComponent("footer", "components/footer.html");