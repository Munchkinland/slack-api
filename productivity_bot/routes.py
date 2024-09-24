from flask import request, jsonify, abort
from services.trello_client import TrelloClient
from services.task_manager import TaskManager
from services.time_tracker import TimeTracker
from services.personal_assistant import PersonalAssistant
from services.wellness_manager import WellnessManager
from services.pomodoro_timer import PomodoroTimer
from config import Config
import hashlib
import hmac
import time
import os

def verify_slack_request(request):
  # Verificar la firma de Slack para asegurar que la solicitud es legítima
  slack_signing_secret = os.getenv('SLACK_SIGNING_SECRET')
  timestamp = request.headers.get('X-Slack-Request-Timestamp')
  if abs(time.time() - int(timestamp)) > 60 * 5:
      return False

  sig_basestring = f"v0:{timestamp}:{request.get_data(as_text=True)}"
  my_signature = 'v0=' + hmac.new(
      slack_signing_secret.encode(),
      sig_basestring.encode(),
      hashlib.sha256
  ).hexdigest()

  slack_signature = request.headers.get('X-Slack-Signature')
  return hmac.compare_digest(my_signature, slack_signature)

def configure_routes(app):
  # Inicialización de servicios
  trello_client = TrelloClient(Config.TRELLO_API_KEY, Config.TRELLO_TOKEN)
  task_manager = TaskManager(trello_client, Config.TRELLO_BOARD_ID)
  time_tracker = TimeTracker()
  personal_assistant = PersonalAssistant()
  wellness_manager = WellnessManager()
  pomodoro_timer = PomodoroTimer()

  @app.route('/slack/events', methods=['POST'])
  def slack_events():
      if not verify_slack_request(request):
          abort(400, description="Invalid Slack signature")

      data = request.form
      command = data.get('command')
      text = data.get('text')

      try:
          if command == '/create_task':
              response = task_manager.create_task(list_id='your_list_id', name=text)
              return jsonify(response)

          elif command == '/start_timer':
              time_tracker.start_timer()
              return jsonify(text="Timer started!")

          elif command == '/stop_timer':
              elapsed_time = time_tracker.stop_timer()
              return jsonify(text=f"Timer stopped! Elapsed time: {elapsed_time} seconds")

          elif command == '/get_tip':
              tip = personal_assistant.provide_tip()
              return jsonify(text=tip)

          elif command == '/break_reminder':
              reminder = wellness_manager.send_break_reminder()
              return jsonify(text=reminder)

          elif command == '/start_pomodoro':
              pomodoro_timer.start_pomodoro()
              return jsonify(text="Pomodoro session started!")

          else:
              return jsonify(text="Unknown command")

      except Exception as e:
          return jsonify(text=f"An error occurred: {str(e)}"), 500