from xml.dom.expatbuilder import parseString
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from empresa import empresa
from servicio import servicio
from mensaje import mensajito
from fpdf import FPDF
import json
import re
global Positivas
global Negativas
global listaEmpresas
global listaMensaje
global letras
global fechas
global var
global varPDF

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#Metodo Inicial, comprobar Servidor
@app.route("/")
def index():
    return jsonify({"status": 200})

# Metodo de carga y enviar informacion al text area 1
@app.route('/carga', methods=['POST'])
def cargaArchivo():
    global letras
    if request.method == 'POST':
        letras = json.loads(request.data)
        tav =msj(letras)
        if tav == "Yep":
            return jsonify({"status": 200})
        else:
            return jsonify({"status": 500})

@app.route('/cargaPostman', methods=['POST'])
def cargaArchivoPost():
    global letras
    if request.method == 'POST':
        letras = request.data.decode('utf-8')
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

#Metodo procesar Info y enviar Info procesada
@app.route('/procesar', methods=['POST'])
def procesarTexto():
    if request.method == 'POST':
        letras = json.loads(request.data)
        if letras == "Procesa":
            tav = procesar()
            if tav == "Yep":
                return jsonify({"status": 200})
            else:
                return jsonify({"status": 500})

@app.route('/procesarPostman', methods=['POST'])
def procesarTextoPost():
    if request.method == 'POST':
        letras = request.data.decode('utf-8')
        if letras == "Procesa":
            tav = procesar()
            if tav == "Yep":
                return jsonify({"status": 200})
            else:
                return jsonify({"status": 500})

@app.route('/procesado', methods=['GET'])
def envioProcesado():
    global var
    if request.method == 'GET':
        return json.dumps(var)

#Metodo generar PDF
@app.route('/generatePDF', methods=['POST'])
def generexPDF():
    if request.method == 'POST':
        letras = json.loads(request.data)
        if letras == "PDF":
            tav = genePDF()
            if tav == "Yep":
                return jsonify({"status": 200})
            else:
                return jsonify({"status": 500})

@app.route('/generatePDFPostman', methods=['POST'])
def pdfPost():
    if request.method == 'POST':
        letras = request.data.decode('utf-8')
        if letras == "PDF":
            tav = procesar()
            if tav == "Yep":
                return jsonify({"status": 200})
            else:
                return jsonify({"status": 500})

#Metodo probar mensaje
@app.route('/probarMensaje', methods=['POST'])
def pruebaM():
    if request.method == 'POST':
        mensae = request.data.decode('utf-8')
        vari = msjUno(mensae)
        return jsonify({"vari": vari})
    
#Metodo clasi por fecha y empresa
@app.route('/clasiEmpresa', methods=['POST'])
def clasiEmpresa():
    if request.method == 'POST':
        mensae = request.data.decode('utf-8')
        y = json.loads(mensae)
        fecha = y["fecha"]
        empresa = y["empresa"]
        vari = clasiporEmpresa(fecha,empresa)
        return jsonify({"vari": vari})

#Metodos propios en python para procesar todos los archivos de manera interna
def msj(letras):
    global Positivas
    global Negativas
    global listaEmpresas
    global listaMensaje
    global fechas
    Positivas = []
    Negativas = []
    listaEmpresas = []
    listaMensaje = []
    fechas = []

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
            fechas.append(fecha)
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
            msjLimpio = re.sub(r"""[:!?'".<>(){}@%&*/[/]""", " ", msjLimpio)
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
    fechas = list(set(fechas))
    fechas = sorted(fechas)
    listaEmpresas = list(set(listaEmpresas))
    return "Yep"

def FuncionDos(msj):
    global Positivas
    global Negativas
    global listaEmpresas
    contNegativas = 0
    contPositivas = 0
    for posi in Positivas:
        posiUno = castear(posi)
        msjUno = castear(msj)
        msjDos = msjUno.split(" ")
        for ss in msjDos:
            if posiUno in ss:
                print(posiUno)
                contPositivas = contPositivas + 1
    
    for nega in Negativas:
        nega = castear(nega)
        msj = castear(msj)
        msjTres = msj.split(" ")
        for rr in msjTres:
            if nega == rr:
                print(nega)
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

def msjUno(letras):
    global Positivas
    global Negativas
    global listaEmpresas
    global fechas

    documentt = parseString(str(letras))
    mensajes = documentt.getElementsByTagName("mensaje")
    
    for x in mensajes:
        textoCrudo = str(x.childNodes[0].nodeValue)
        mensajeCrudo = textoCrudo.strip()#
        crudUno = mensajeCrudo.split("Lugar y fecha:")[1]
        lugar = crudUno.split(",")[0].strip()#
        crudDos = crudUno.split(",")[1].strip()
        crudoDos = crudDos.split()
        fecha = crudoDos[0]#
        hora = crudoDos[1]#
        resto = crudDos.split("Usuario:")[1].strip()
        usuario = resto.split()[0]#
        restoDos = resto.split("Red social:")[1].strip()
        redSocial = restoDos.split()[0]#
        restoTres = crudUno.split(redSocial)[1].strip()
        msjSucio = restoTres.replace("\n"," ")
        msjSucio = msjSucio.replace("\t","")
        msjSucio = msjSucio.replace("  "," ")
        msjLimpio = msjSucio.replace("  "," ")#
        msjLimpio = re.sub(r"""[:!?'".<>(){}@%&*/[/]""", " ", msjLimpio)
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
        vari = procesarUno(msj)

        return vari

def procesarUno(msj):
    global listaEmpresas

    var = ""
    var  = var + f'''<respuesta><fecha>{msj.fecha}</fecha>'''
    var  = var + f'''<red_social>{msj.redSocial}</red_social>'''
    var  = var + f'''<usuario>{msj.usuario}</usuario><empresas>'''
    for emprex in listaEmpresas:
            varDos = ""
            empresitas = msj.getEmpresa()
            if emprex.nombre in empresitas:
                servix = emprex.getServicios()
                varTres = ""
                for serv in servix:
                    listaAlias = serv.getAlias()
                    nombreServi = serv.nombre
                    for alix in listaAlias:
                        alixUno = (alix)
                        mms = (msj.msjLimpio)
                        if castear(alixUno) in castear(mms):
                            varTres = varTres + f'''<servicio>{nombreServi}</servicio>'''
                            break
                    if castear(nombreServi) in castear(mms):
                        varTres = varTres + f'''<servicio>{nombreServi}</servicio>'''
                varDos = varDos + f'''<empresa nombre={emprex.nombre}>'''
                varDos = varDos + varTres
                varDos = varDos +f'''</empresa>'''
    var = var + varDos
    var = var + f'''</empresas>'''
    var = var + f'''<palabras_positivas>{msj.getPositivas()}</palabras_positivas>'''
    var = var + f'''<palabras_negativas>{msj.getNegativas()}</palabras_negativas>'''
    var = var + f'''<sentimiento_positivo>{msj.getPorcePositivas()}</sentimiento_positivo>'''
    var = var + f'''<sentimiento_negativo>{msj.getPorceNegativas()}</sentimiento_negativo>'''
    var = var + f'''<sentimiento_analizado>{msj.getSentimiento()}</sentimiento_analizado>'''
    var = var + f'''</respuesta>'''
    return var

def procesar():
    global Positivas
    global Negativas
    global listaEmpresas
    global listaMensaje
    global fechas
    global var
    global letras
    var = '''<?xml version=\"1.0\"?>\n\t<lista_respuestas>\n'''
    for date in fechas:
        positivs = 0
        negativs = 0
        neutros = 0
        nom = 0
        var  = var + f'''\t\t<respuesta>\n\t\t\t<fecha>{date}</fecha>\n\t\t\t<mensajes>\n'''

        for mensa in listaMensaje:
            if str(mensa.fecha) == str(date):
                
                nom = nom+1
                if mensa.getSentimiento() == "Positivo":
                    positivs = positivs+1
                elif mensa.getSentimiento() == "Negativo":
                    negativs = negativs+1
                else:
                    neutros = neutros+1
                
        var = var + f'''\t\t\t\t<total> {nom}</total>\n\t\t\t\t\t<positivos>{positivs}</positivos>\n\t\t\t\t\t<negativos>{negativs}</negativos>\n\t\t\t\t\t<neutros>{neutros}</neutros>\n\t\t\t\t</mensajes>\n'''
        var = var +f'''\t\t\t<analisis>\n'''
        
        
        for emprex in listaEmpresas:
            varDos = ""
            toti = 0
            posi = 0
            negi = 0
            neutri = 0
            for men in listaMensaje:
                if str(men.fecha) == str(date):
                    empresitas = men.getEmpresa()
                    if emprex.nombre in empresitas:
                        toti = toti + 1
                        if men.getSentimiento() == "Positivo":
                            posi = posi+1
                        elif men.getSentimiento() == "Negativo":
                            negi = negi+1
                        else:
                            neutri = neutri+1
            servix = emprex.getServicios()
            varTres = ""
            for serv in servix:
                totix = 0
                posix = 0
                negix = 0
                neutrix = 0
                listaAlias = serv.getAlias()
                nameUno = castear(serv.nombre)
                name = serv.nombre
                for men in listaMensaje:
                    if str(men.fecha) == str(date):
                        msj = castear(men.msjLimpio)
                        if nameUno in msj:
                            totix = totix + 1
                            if men.getSentimiento() == "Positivo":
                                posix = posix+1
                            elif men.getSentimiento() == "Negativo":
                                negix = negix+1
                            else:
                                neutri = neutri+1
                        for alix in listaAlias:
                            alixUno = castear(alix)

                            if alixUno in msj:
                                totix = totix + 1
                                if men.getSentimiento() == "Positivo":
                                    posix = posix+1
                                elif men.getSentimiento() == "Negativo":
                                    negix = negix+1
                                else:
                                    neutrix = neutrix+1
                varTres = varTres + f'''\t\t\t\t\t\t<servicio nombre="{name}">\n\t\t\t\t\t\t<mensajes>\n'''
                varTres = varTres + f'''\t\t\t\t\t\t\t<total>{totix}</total>\n\t\t\t\t\t\t\t<positivos>{posix}</positivos>\n\t\t\t\t\t\t\t<negativos>{negix}</negativos>\n\t\t\t\t\t\t\t<neutros>{neutrix}</neutros>\n\t\t\t\t\t\t</mensajes>\n\t\t\t\t\t\t</servicio>\n'''


            varDos = varDos + f'''\t\t\t\t<empresa nombre="{emprex.nombre}">\n\t\t\t\t\t<mensajes>\n'''
            varDos = varDos +f'''\t\t\t\t\t\t<total>{toti}</total>\n\t\t\t\t\t\t<positivos>{posi}</positivos>\n\t\t\t\t\t\t<negativos>{negi}</negativos>\n\t\t\t\t\t\t<neutros>{neutri}</neutros>\n\t\t\t\t\t</mensajes>\n'''
            varDos = varDos +f'''\t\t\t\t\t<servicios>\n'''
            varDos = varDos + varTres
            varDos = varDos +f'''\t\t\t\t\t</servicios>\n\t\t\t\t</empresa>\n'''
            var = var + varDos
        var = var + f'''\t\t\t</analisis>\n\t\t</respuesta>\n'''
    var = var + f'''\t</lista_respuestas>'''

    geneTXT(letras,var)
    return "Yep"

def castear(texto):
    textoUno = texto.replace("á","a")
    textoDos = textoUno.replace("é","e")
    textoTres = textoDos.replace("í","i")
    textoCuatro = textoTres.replace("ó","o")
    textoCinco = textoCuatro.replace("ú","u")
    textoA = textoCinco.replace("Á","A")
    textoB = textoA.replace("É","E")
    textoC = textoB.replace("Í","I")
    textoD = textoC.replace("Ó","O")
    textoE = textoD.replace("Ú","U")
    textoZ = textoE.lower()
    return textoZ

def geneTXT(texto,textoDos):
    f = open ('db.txt','a')
    varUno = "Entrada: \n"+texto+"\n\n"
    varDos = "Salida: \n"+textoDos+"\n\n"
    vass = varUno+varDos
    f.write(vass)
    f.close()

def genePDF():
    fichero = open("db.txt","r")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial",'B',size=10)
    line = 1

    for linea in fichero:
        pdf.cell(200,7,txt=linea,ln=line,align="L")
        if linea[-1]==("\n"):
            linea = linea[:-1]
        line+=1
    
    pdf.output("REPORTE.pdf")
    fichero.close()
    return "Yep"

def clasiporEmpresa(fecha, empresa):
    global Positivas
    global Negativas
    global listaEmpresas
    global listaMensaje
    global fechas
    var = '''<?xml version=\"1.0\"?><lista_respuestas>'''
    positivs = 0
    negativs = 0
    neutros = 0
    nom = 0
    var  = var + f'''<respuesta><fecha>{fecha}</fecha><mensajes>'''

    for mensa in listaMensaje:
        if str(mensa.fecha) == str(fecha):
            nom = nom+1
            if mensa.getSentimiento() == "Positivo":
                positivs = positivs+1
            elif mensa.getSentimiento() == "Negativo":
                negativs = negativs+1
            else:
                neutros = neutros+1
            
    var = var + f'''<total>{nom}</total><positivos>{positivs}</positivos><negativos>{negativs}</negativos><neutros>{neutros}</neutros></mensajes>'''
    var = var +f'''<analisis>'''
    
    if str(empresa) == "todas":
        for emprex in listaEmpresas:
            varDos = ""
            toti = 0
            posi = 0
            negi = 0
            neutri = 0
            for men in listaMensaje:
                if str(men.fecha) == str(fecha):
                    empresitas = men.getEmpresa()
                    if emprex.nombre in empresitas:
                        toti = toti + 1
                        if men.getSentimiento() == "Positivo":
                            posi = posi+1
                        elif men.getSentimiento() == "Negativo":
                            negi = negi+1
                        else:
                            neutri = neutri+1
            servix = emprex.getServicios()
            varTres = ""
            for serv in servix:
                totix = 0
                posix = 0
                negix = 0
                neutrix = 0
                listaAlias = serv.getAlias()
                nameUno = castear(serv.nombre)
                name = serv.nombre
                for men in listaMensaje:
                    if str(men.fecha) == str(fecha):
                        msj = castear(men.msjLimpio)
                        if nameUno in msj:
                            totix = totix + 1
                            if men.getSentimiento() == "Positivo":
                                posix = posix+1
                            elif men.getSentimiento() == "Negativo":
                                negix = negix+1
                            else:
                                neutri = neutri+1
                        for alix in listaAlias:
                            alixUno = castear(alix)
                            if alixUno in msj:
                                totix = totix + 1
                                if men.getSentimiento() == "Positivo":
                                    posix = posix+1
                                elif men.getSentimiento() == "Negativo":
                                    negix = negix+1
                                else:
                                    neutrix = neutrix+1
                varTres = varTres + f'''<servicio nombre="{name}"><mensajes>'''
                varTres = varTres + f'''<total>{totix}</total><positivos>{posix}</positivos><negativos>{negix}</negativos><neutros>{neutrix}</neutros></mensajes></servicio>'''


            varDos = varDos + f'''\t\t\t\t<empresa nombre="{emprex.nombre}">\n\t\t\t\t\t<mensajes>\n'''
            varDos = varDos +f'''<total>{toti}</total><positivos>{posi}</positivos><negativos>{negi}</negativos><neutros>{neutri}</neutros></mensajes>'''
            varDos = varDos +f'''<servicios>'''
            varDos = varDos + varTres
            varDos = varDos +f'''</servicios></empresa>'''
            var = var + varDos
    else:
        for emmm in listaEmpresas:
            if str(empresa) == emmm.nombre:
                varDos = ""
                toti = 0
                posi = 0
                negi = 0
                neutri = 0
                for men in listaMensaje:
                    if str(men.fecha) == str(fecha):
                        empresitas = men.getEmpresa()
                        if empresa in empresitas:
                            toti = toti + 1
                            if men.getSentimiento() == "Positivo":
                                posi = posi+1
                            elif men.getSentimiento() == "Negativo":
                                negi = negi+1
                            else:
                                neutri = neutri+1
                for em in listaEmpresas:
                    varTres = ""
                    if castear(empresa) == castear(str(em.nombre)):
                        servixx = em.getServicios()
                        for serv in servixx:
                            totix = 0
                            posix = 0
                            negix = 0
                            neutrix = 0
                            listaAlias = serv.getAlias()
                            nameUno = castear(serv.nombre)
                            name = serv.nombre
                            for men in listaMensaje:
                                if str(men.fecha) == str(fecha):
                                    msj = castear(men.msjLimpio)
                                    if nameUno in msj:
                                        totix = totix + 1
                                        if men.getSentimiento() == "Positivo":
                                            posix = posix+1
                                        elif men.getSentimiento() == "Negativo":
                                            negix = negix+1
                                        else:
                                            neutri = neutri+1
                                    for alix in listaAlias:
                                        alixUno = castear(alix)
                                        if alixUno in msj:
                                            totix = totix + 1
                                            if men.getSentimiento() == "Positivo":
                                                posix = posix+1
                                            elif men.getSentimiento() == "Negativo":
                                                negix = negix+1
                                            else:
                                                neutrix = neutrix+1
                            varTres = varTres + f'''<servicio nombre="{name}"><mensajes>'''
                            varTres = varTres + f'''<total>{totix}</total><positivos>{posix}</positivos><negativos>{negix}</negativos><neutros>{neutrix}</neutros></mensajes></servicio>'''


                varDos = varDos + f'''<empresa nombre="{em.nombre}"><mensajes>'''
                varDos = varDos +f'''<total>{toti}</total><positivos>{posi}</positivos><negativos>{negi}</negativos><neutros>{neutri}</neutros></mensajes>'''
                varDos = varDos +f'''<servicios>'''
                varDos = varDos + varTres
                varDos = varDos +f'''</servicios></empresa>'''
                var = var + varDos
    var = var + f'''</analisis></respuesta>'''
    var = var + f'''</lista_respuestas>'''
    geneTXT("La misma entrada",var)
    return var

if __name__ == "__main__":
    app.run(port=5000, debug=True)
