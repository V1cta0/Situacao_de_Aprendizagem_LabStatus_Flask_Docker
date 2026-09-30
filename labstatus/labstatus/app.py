from flask import Flask, render_template, jsonify
from flask_cors import CORS 


app = Flask(__name__)
CORS(app) 
SERVICOS = [
    {"nome": "Servidor de Arquivos", "status": "online"},
    {"nome": "Portal Acadêmico", "status": "online"},
    {"nome": "Sistema de Impressão", "status": "manutencao"},
    {"nome": "Ambiente de Desenvolvimento", "status": "online"},
]


ROTULOS = {"online": "Online", "manutencao": "Em manutenção"}

@app.route("/")
def index():
    return render_template("index.html", servicos=SERVICOS, rotulos=ROTULOS)


@app.route("/api/status")
def api_status():
    return jsonify({"servicos": SERVICOS})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
