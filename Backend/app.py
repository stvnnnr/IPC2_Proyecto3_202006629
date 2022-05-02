from xml.dom.expatbuilder import parseString
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from empresa import empresa
from servicio import servicio
from mensaje import mensajito
import json
global Positivas
global Negativas
global listaEmpresas
global listaMensaje
global listaFechas
global letras

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def index():
    return("Hola bb")


@app.route('/carga', methods=['POST'])
def cargaPacientes():
    global letras
    if request.method == 'POST':
        letras = json.loads(request.data)
        tav =msj(letras)
        if tav == "Yep":
            return jsonify({"status": 200})
        else:
            return jsonify({"status": 500})


@app.route('/carga', methods=['GET'])
def envioInfo():
    global letras
    if request.method == 'GET':
        return json.dumps(letras)


def msj(letras):
    global Positivas
    global Negativas
    global listaEmpresas
    global listaMensaje
    global listaFechas
    Positivas = []
    Negativas = []
    listaEmpresas = []
    listaMensaje = []
    listaFechas = []

    documentt = parseString(str(letras))
    raicita = documentt.documentElement
    positivos = raicita.getElementsByTagName("sentimientos_positivos")
    negativos = raicita.getElementsByTagName("sentimientos_negativos")
    companies = raicita.getElementsByTagName("empresa")
    mensajes = raicita.getElementsByTagName("lista_mensajes")


    for posi in positivos:
                words = posi.getElementsByTagName("palabra")
                for pal in words:
                    textoCrudo = str(pal.childNodes[0].nodeValue)
                    palab = textoCrudo.strip()#
                    Positivas.append(palab)

    for nega in negativos:
                words = nega.getElementsByTagName("palabra")
                for pal in words:
                    textoCrudo = str(pal.childNodes[0].nodeValue)
                    palab = textoCrudo.strip()#
                    Negativas.append(palab)

    for empre in companies:
        nombreSucio = empre.getElementsByTagName("nombre")[0]
        nombreEspacio = str(nombreSucio.childNodes[0].data)
        nombre = nombreEspacio.strip()#
        empUno = empresa(nombre)

        servi = empre.getElementsByTagName("servicio")
        for x in servi:
            nombreServi = str(x.getAttribute("nombre"))#
            serUno = servicio(nombreServi)
            alis = x.getElementsByTagName("alias")
            for y in alis:
                textoCrudo = str(y.childNodes[0].nodeValue)
                alia = textoCrudo.strip()#
                serUno.setAlias(alia)
            empUno.setServicio(serUno)
        listaEmpresas.append(empUno)

    for mensaje in mensajes:
        nam = mensaje.getElementsByTagName("mensaje")
        for x in nam:
            #print("-------------------------------------")
            textoCrudo = str(x.childNodes[0].nodeValue)
            mensajeCrudo = textoCrudo.strip()#
            crudUno = mensajeCrudo.split("Lugar y fecha:")[1]
            lugar = crudUno.split(",")[0].strip()#
            #print(lugar)
            crudDos = crudUno.split(",")[1].strip()
            crudoDos = crudDos.split()
            fecha = crudoDos[0]#
            #print(fecha)
            hora = crudoDos[1]#
            #print(hora)
            resto = crudDos.split("Usuario:")[1].strip()
            usuario = resto.split()[0]#
            #print(usuario)
            restoDos = resto.split("Red social:")[1].strip()
            redSocial = restoDos.split()[0]#
            #print(redSocial)
            restoTres = crudUno.split(redSocial)[1].strip()
            msjSucio = restoTres.replace("\n"," ")
            msjSucio = msjSucio.replace("\t","")
            msjSucio = msjSucio.replace("  "," ")
            msjLimpio = msjSucio.replace("  "," ")#
            msj = mensajito(lugar,fecha,hora,usuario,redSocial,msjLimpio)
            
            for empre in listaEmpresas:
                if empre.nombre in msjLimpio:
                    msj.setEmpresa(empre.nombre)
            
            sentimiento = FuncionDos(msjLimpio)
            msj.setSentimiento(sentimiento[0])
            msj.setPositivas(sentimiento[1])
            msj.setNegativas(sentimiento[2])
            msj.setPorcePositivas(sentimiento[3])
            msj.setPorceNegativas(sentimiento[4])
            listaMensaje.append(msj)
    return "Yep"

def FuncionDos(msj):
    global Positivas
    global Negativas
    global listaEmpresas
    contNegativas = 0
    contPositivas = 0
    for posi in Positivas:
        if posi in msj:
            contPositivas = contPositivas + 1
    
    for nega in Negativas:
        if nega in msj:
            contNegativas = contNegativas + 1
    
    sumPal = (contPositivas+contNegativas)
    porPosiNum = ((contPositivas*100)/sumPal)
    porNegaNum = ((contNegativas*100)/sumPal)

    porPosi = (str(porPosiNum)+"%")
    porNega = (str(porNegaNum)+"%")
    
    if contPositivas>contNegativas:
        return ("Positivo",contPositivas,contNegativas,porPosi,porNega)
    elif contPositivas<contNegativas:
        return ("Negativo",contPositivas,contNegativas,porPosi,porNega)
    else:
        return ("Neutro",contPositivas,contNegativas,porPosi,porNega)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
