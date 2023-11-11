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
            return;}
        draggedElement.style.position = "absolute";
        draggedElement.style.left = 530 + "px"; // Ajusta según tus necesidades
        draggedElement.style.top = 183 + "px"; // Ajusta según tus necesidades
        container.appendChild(draggedElement);
    }
}
