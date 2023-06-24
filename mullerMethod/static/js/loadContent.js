// Seleccionamos los enlaces y el div de contenido
const findRootsBtn = document.querySelector("[data-find-roots]");
const iterationsDestiny = document.getElementById("iterationsDestiny")
const graphics = document.getElementById("graphics");

// Agregamos un evento de clic a cada enlace
if(findRootsBtn){
    findRootsBtn.addEventListener("click", function() {
        event.preventDefault();
        loadHtmlIterations("http://127.0.0.1:8000/iterations/");
    });

    // Función para cargar el contenido de la página HTML y reemplazar el contenido del div
    const loadHtmlIterations = (iterationsUrl) => {
        fetch(iterationsUrl)
            .then(response => response.text())
            .then(dataIterations => {
                iterationsDestiny.innerHTML = dataIterations;
            });
        graphics.classList.remove("d-none");
    };
}
