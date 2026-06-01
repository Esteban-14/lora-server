from flask import Flask, render_template, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

datos_lora = {i: {"valor": None, "timestamp": None} for i in range(1, 6)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    return jsonify(datos_lora)

@app.route('/api/actualizar', methods=['POST'])
def actualizar_dato():
    data = request.json
    id_lora = data.get('id')
    valor = data.get('valor')

    if id_lora in datos_lora and valor is not None:
        datos_lora[id_lora]["valor"] = valor
        datos_lora[id_lora]["timestamp"] = datetime.now().isoformat()
        return jsonify({"status": "ok"}), 200

    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
