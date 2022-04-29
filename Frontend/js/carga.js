
var text;

async function cargaPrevia(file) {
  text = await file.text();
}

function enviarArchivo(){
  document.getElementById("Upload").style.display = "None";
  alert("Archivo cargado con exito")
  fetch("http://localhost:5000/carga", {
    method: "POST",
    body: JSON.stringify(text),
    headers: {
      "Content-Type": "application/json",
    },
  }).then((res) => res.json()).catch(function (error) { console.log(error);});
  getPacientes()
}


function getPacientes() {
  fetch("http://localhost:5000/carga", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then(function (response) {
      let data = response;
      console.log("Si cargo papito")
      document.getElementById('textAreaUno').value = data;
    })
    .catch(function (error) {
      console.log(error);
    });
}