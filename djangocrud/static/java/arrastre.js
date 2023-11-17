
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
    
        var x = event.clientX - container.getBoundingClientRect().left;
        var y = event.clientY - container.getBoundingClientRect().top;
    
        draggedElement.style.position = "absolute";
        draggedElement.style.left = x + 700 + "px"; // Ajusta según tus necesidades
        draggedElement.style.top = y + 300 + "px"; // Ajusta según tus necesidades
    
        container.appendChild(draggedElement);
        var imageName = draggedElement.getAttribute('id');
        callEstados(imageName);
    }
}

function callEstados(imageName) {
    // Realiza una solicitud AJAX para llamar a la función estados en Django
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/estados/" + imageName + "/", true);
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
    lista.innerHTML = ""
    cities.forEach(function (city) {
        var item = document.createElement("li")
        var button = document.createElement("button");
        button.textContent = city;
        button.id = city.replace(/\s+/g, '-').toLowerCase();
        item.appendChild(button)
        console.log(item)
        lista.appendChild(item)
        
        button.addEventListener("click", function () {
            var cityName = city; 
            callPythonFunction(imageName, cityName);
        });

        container.appendChild(lista);
    });
}

function callPythonFunction(imageName, cityName) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", '/obtener_calidad_aire_ciudad/' + imageName + '/' + cityName + '/', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                console.log("Datos de la calidad del aire:", response);
                // Manejar la respuesta, por ejemplo, mostrarla en un elemento HTML
                mostrarResultado(response);
            } else {
                console.error("Error en la solicitud:", xhr.status);
            }
        }
    };
    xhr.send();
}

function mostrarResultado(response) {
    // Manejar la respuesta, por ejemplo, mostrarla en un elemento HTML
    var resultadoDiv = document.getElementById("resultado");
    if (response.error) {
        resultadoDiv.innerHTML = "Error: " + response.error;
    } else {
        resultadoDiv.innerHTML = "Dato: " + response.dato + ", Calidad del aire: " + response.calidad_aire;
    }
}

document.querySelectorAll('#lista button').forEach(function(button) {
    button.addEventListener("click", function () {
        var cityName = this.textContent;
        var imageName = this.id;
        callPythonFunction(imageName, cityName);
    });
});