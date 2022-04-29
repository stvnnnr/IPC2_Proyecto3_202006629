from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

global letras

@app.route("/")
def index():
    return("Hola bb")

@app.route('/carga', methods=['POST'])
def cargaPacientes():
    global letras
    if request.method == 'POST':
        letras = json.loads(request.data)
        print(letras)         
        return jsonify({"status": 200})
    
@app.route('/carga', methods=['GET'])
def envioInfo():
    global letras
    if request.method == 'GET':
        return json.dumps(letras)

if __name__=="__main__":
    app.run(port=5000, debug=True)