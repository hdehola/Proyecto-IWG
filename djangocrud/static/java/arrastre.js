function allowDrop(event) {
    event.preventDefault();
}

function drag(event) {
    event.dataTransfer.setData("text", event.target.id);
}

function drop(event) {
    event.preventDefault();
    var data = event.dataTransfer.getData("text");
    var draggedElement = document.getElementById(data);
    var container = event.target.closest(".container");

    if (container) {
        if (container.querySelector("img")) {
            return;
        }
        document.querySelectorAll(".container img").forEach(function (img) {
            img.style.zIndex = "-2";
        });
        draggedElement.style.zIndex = "8";
        

        // Establece el tamaño del contenedor
        var containerWidth = container.offsetWidth;
        var containerHeight = container.offsetHeight;

        // Establece el tamaño de la imagen
        draggedElement.style.width = 40 + "px";
        draggedElement.style.height = 20 + "px";

        // Establece la posición de la imagen
        draggedElement.style.position = "absolute";
        draggedElement.style.left = "-150px"; // Ajusta según tus necesidades
        draggedElement.style.top = "-70px"; // Ajusta según tus necesidades

        // Agrega la imagen al contenedor
        container.appendChild(draggedElement);

        var imageName = draggedElement.getAttribute('id');
        callEstados(imageName);
    }
}


function callEstados(imageName) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", window.location.origin + "/estados/" + imageName + "/", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            updateCities(imageName, response.cities);
        }
    };
    xhr.send();
}

function updateCities(imageName, cities) {
    var container = document.querySelector("#cityList");

    var lista = document.getElementById("lista");
    lista.innerHTML = "";

    cities.forEach(function (city) {
        var item = document.createElement("li");
        var button = document.createElement("button");
        button.textContent = city;
        button.id = city.replace(/\s+/g, '-').toLowerCase();
        item.appendChild(button);
        lista.appendChild(item);

        button.addEventListener("click", function () {
            var cityName = city;
            callPythonFunction(imageName, cityName);
        });

        container.appendChild(lista);
    });
}

function callPythonFunction(imageName, cityName) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", window.location.origin + '/obtener_calidad_aire_ciudad/' + imageName + '/' + cityName + '/', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                console.log("Datos de la calidad del aire:", response);

                mostrarResultado(response);
            } else {
                console.error("Error en la solicitud:", xhr.status);
            }
        }
    };
    xhr.send();
}

function mostrarResultado(response) {
    var resultadoDiv = document.getElementById("resultado");
    if (response.error) {
        resultadoDiv.innerHTML = "Error: " + response.error;
    } else {
        resultadoDiv.innerHTML = "Comuna: " + response.comuna + ", calidad del aire: " + response.dato +"<br><br>Estado:" + response.texto;
    }
}

document.querySelectorAll('#lista button').forEach(function(button) {
    button.addEventListener("click", function () {
        var cityName = this.textContent;
        var imageName = this.id;
        callPythonFunction(imageName, cityName);
    });
});