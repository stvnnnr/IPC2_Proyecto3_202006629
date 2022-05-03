
function procesar() {
    fetch("http://localhost:5000/procesar", {
        method: "POST",
        body: JSON.stringify("Procesa"),
        headers: {
            "Content-Type": "application/json",
        },
    }).then(res => res.json())
        .then(function (response) {
            console.log(response.status)
            if (response.status = '200') {
                alert("Se procesó satisfactoriamente el archivo")
                getProcesado()
            }

        })
        .catch(function (error) { console.log(error); });
}

function getProcesado() {
    fetch("http://localhost:5000/procesado", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((res) => res.json())
        .then(function (response) {
            let data = response;
            console.log("Si se lleno el textArea 2 papito")
            document.getElementById('textAreaDos').value = data;
        })
        .catch(function (error) {
            console.log(error);
        });
}