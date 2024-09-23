import os
from dotenv import load_dotenv
from slack_bolt import App
from github import Github
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext
from office365.onedrive.drive import Drive

load_dotenv()

# Esta clase verifica la conexion a las APIs
class ConnectionVerifier:
  def __init__(self):
      self.slack_token = os.getenv("SLACK_TOKEN")
      self.github_token = os.getenv("GITHUB_TOKEN")
      self.office_client_id = os.getenv("OFFICE_CLIENT_ID")
      self.office_client_secret = os.getenv("OFFICE_CLIENT_SECRET")
      self.office_tenant_id = os.getenv("OFFICE_TENANT_ID")

      self.slack_app = None
      self.github_client = None
      self.office_client = None

  def verify_slack(self):
      try:
          self.slack_app = App(token=self.slack_token)
          self.slack_app.client.auth_test()
          print("Conexión a Slack exitosa")
          return True
      except Exception as e:
          print(f"Error en la conexión a Slack: {str(e)}")
          return False

  def verify_github(self):
      try:
          self.github_client = Github(self.github_token)
          self.github_client.get_user().login
          print("Conexión a GitHub exitosa")
          return True
      except Exception as e:
          print(f"Error en la conexión a GitHub: {str(e)}")
          return False

  def verify_office365(self):
      try:
          self.office_client = ClientContext.connect_with_client_credentials(
              f"https://{self.office_tenant_id}.sharepoint.com",
              ClientCredential(self.office_client_id, self.office_client_secret)
          )
          self.office_client.load(self.office_client.web)
          self.office_client.execute_query()
          print("Conexión a Office 365 exitosa")
          return True
      except Exception as e:
          print(f"Error en la conexión a Office 365: {str(e)}")
          return False

  def verify_all_connections(self):
      slack_ok = self.verify_slack()
      github_ok = self.verify_github()
      office_ok = self.verify_office365()

      return all([slack_ok, github_ok, office_ok])

# Esta clase maneja la lógica y las funciones del bot
class IntegratedSlackBot:

  def __init__(self, verifier):
      self.bot_name = "slackbot  # Nombre del bot
      self.slack_app = verifier.slack_app
      self.github_client = verifier.github_client
      self.office_client = verifier.office_client
      self.onedrive = Drive(self.office_client)

  def get_unread_emails(self, limit=5):
      messages = self.office_client.mail.my_messages.filter("IsRead eq false").get().execute_query()
      return [f"De: {msg.sender.email_address}, Asunto: {msg.subject}" for msg in messages[:limit]]

  def search_github_issues(self, repo_name, query):
      repo = self.github_client.get_repo(repo_name)
      issues = repo.get_issues(state='open', sort='created', direction='desc')
      return [f"#{issue.number}: {issue.title}" for issue in issues if query.lower() in issue.title.lower()][:5]

  def list_onedrive_files(self, folder_path):
      folder = self.onedrive.root.get_by_path(folder_path)
      items = folder.children.get().execute_query()
      return [item.name for item in items]

  def create_word_document(self, name, content):
      doc = self.office_client.word.create_document(name)
      doc.body.insert_paragraph(content)
      doc.save()
      return f"Documento '{name}' creado exitosamente."

  def handle_command(self, command, channel):
      try:
          if command.startswith('emails'):
              emails = self.get_unread_emails()
              response = "Correos no leídos:\n" + "\n".join(emails)
          elif command.startswith('github'):
              _, repo, query = command.split(' ', 2)
              issues = self.search_github_issues(repo, query)
              response = f"Issues de GitHub en {repo} que coinciden con '{query}':\n" + "\n".join(issues)
          elif command.startswith('files'):
              _, folder = command.split(' ', 1)
              files = self.list_onedrive_files(folder)
              response = f"Archivos en la carpeta de OneDrive '{folder}':\n" + "\n".join(files)
          elif command.startswith('create doc'):
              _, name, content = command.split(' ', 2)
              response = self.create_word_document(name, content)
          else:
              response = "Lo siento, no entendí ese comando."
      except Exception as e:
          response = f"Ocurrió un error al procesar el comando: {str(e)}"
      
      self.slack_app.client.chat_postMessage(channel=channel, text=response)

  def start(self):
      @self.slack_app.event("app_mention")
      def handle_mentions(body, say):
          event = body["event"]
          text = event["text"]
          channel = event["channel"]
          
          command = text.split("> ", 1)[1] if "> " in text else text
          
          self.handle_command(command, channel)

      print("Bot iniciado y escuchando eventos...")
      self.slack_app.start(port=3000)

if __name__ == "__main__":
  verifier = ConnectionVerifier()
  if verifier.verify_all_connections():
      bot = IntegratedSlackBot(verifier)
      bot.start()
  else:
      print("No se pudo iniciar el bot debido a errores de conexión.")

# Archivos creados/modificados durante la ejecución:
print("No se crearon ni modificaron archivos durante esta ejecución de código.")