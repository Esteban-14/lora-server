from flask import Flask, render_template, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

datos_lora = {i: {"valor": None, "timestamp": None} for i in range(1, 6)}

DISPOSITIVOS_AUTORIZADOS = {
    "ESP-LORA-1": 1,
    "ESP-LORA-2": 2,
    "ESP-LORA-3": 3,
    "ESP-LORA-4": 4,
    "ESP-LORA-5": 5,
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    return jsonify(datos_lora)

@app.route('/api/actualizar', methods=['POST'])
def actualizar_dato():
    data = request.get_json(silent=True) or {}

    device_key = data.get('device_key')
    id_lora = data.get('id')
    valor = data.get('valor')

    if device_key not in DISPOSITIVOS_AUTORIZADOS:
        return jsonify({"status": "error", "message": "dispositivo no autorizado"}), 403

    if DISPOSITIVOS_AUTORIZADOS[device_key] != id_lora:
        return jsonify({"status": "error", "message": "id no coincide con la clave"}), 400

    if valor is None:
        return jsonify({"status": "error", "message": "valor requerido"}), 400

    datos_lora[id_lora]["valor"] = valor
    datos_lora[id_lora]["timestamp"] = datetime.now().isoformat()

    return jsonify({"status": "ok"}), 200

@app.route('/api/reset', methods=['POST'])
def reset_datos():
    for i in range(1, 6):
        datos_lora[i]["valor"] = None
        datos_lora[i]["timestamp"] = None
    return jsonify({"status": "reseteado"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
