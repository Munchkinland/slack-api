from flask import Flask, request, jsonify
import json
import os
from survey_manager import SurveyManager
from sentiment_analysis import SentimentAnalyzer
from report_generator import ReportGenerator

app = Flask(__name__)

# Cargar el token de autenticación
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

# Instancias de las clases necesarias
sentiment_analyzer = SentimentAnalyzer()  # Sin argumento de modelo
survey_manager = SurveyManager()
report_generator = ReportGenerator()

@app.route('/')
def index():
    return "¡La aplicación Flask está en funcionamiento!"

@app.route('/slash', methods=['POST'])
def handle_slash_command():
    data = request.form
    command = data.get('command')
    user_id = data.get('user_id')

    # Verifica si el comando es /encuesta_clima
    if command == "/encuesta_clima":
        survey_manager.send_survey(user_id)
        return jsonify({"text": "La encuesta ha sido enviada."})
    else:
        return jsonify({"text": "Comando no reconocido."})

@app.route('/interactivity', methods=['POST'])  # Ruta para manejar interactividad
def handle_interactivity():
    payload = json.loads(request.form["payload"])
    user_response = payload["actions"][0]["value"]
    user_id = payload["user"]["id"]

    # Guardar la respuesta y analizarla
    survey_manager.save_response(user_id, user_response)
    sentiment_result = sentiment_analyzer.analyze_sentiment(user_response)

    return jsonify({"text": f"Gracias por tu respuesta. Sentimiento detectado: {sentiment_result}."})

@app.route('/generate_report', methods=['POST'])
def generate_report():
    # Genera un reporte basado en las respuestas almacenadas
    report = report_generator.generate_report()
    return jsonify({"text": "Reporte generado.", "attachments": report})

if __name__ == "__main__":
    app.run(port=5000)
    print("La aplicación Flask se está ejecutando en http://127.0.0.1:5000/")
