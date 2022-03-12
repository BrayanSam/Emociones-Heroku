var xhr = new XMLHttpRequest();
function documentoCargado() {
    const body = new FormData();
    xhr.open('POST', '/borrar', true);
    xhr.onload = () => {
        console.log(xhr.responseText)
    };
    xhr.send(body);
    $estado.innerHTML = "Fotos elimindas";
}
document.addEventListener('DOMContentLoaded', documentoCargado, false);

