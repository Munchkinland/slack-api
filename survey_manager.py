import os
import requests

class SurveyManager:
    def __init__(self):
        self.responses = {}

    def send_survey(self, user_id):
        survey_message = {
            "channel": user_id,
            "text": "¿Cómo te sientes hoy?",
            "attachments": [
                {
                    "text": "Selecciona una opción:",
                    "fallback": "No puedes responder esta encuesta",
                    "callback_id": "survey_response",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                        {"name": "response", "text": "Feliz", "type": "button", "value": "feliz"},
                        {"name": "response", "text": "Neutral", "type": "button", "value": "neutral"},
                        {"name": "response", "text": "Triste", "type": "button", "value": "triste"},
                    ]
                }
            ]
        }
        
        self._send_message(survey_message)

    def save_response(self, user_id, response):
        if user_id not in self.responses:
            self.responses[user_id] = []
        self.responses[user_id].append(response)

    def _send_message(self, message):
        slack_url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {os.environ['SLACK_BOT_TOKEN']}",
            "Content-Type": "application/json"
        }
        requests.post(slack_url, headers=headers, json=message)
