function getProcesadoUno() {
    fetch("http://localhost:5000/procesado", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((res) => res.json())
        .then(function (response) {
            let data = response;
            alert("Ultima salida recuperada")
            console.log("Si se lleno el textArea 2 papito")
            document.getElementById('textAreaDos').value = data;
        })
        .catch(function (error) {
            console.log(error);
        });
}