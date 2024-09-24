import os

class Config:
  TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
  TRELLO_TOKEN = os.getenv('TRELLO_TOKEN')
  TRELLO_BOARD_ID = os.getenv('TRELLO_BOARD_ID')
  SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')
  SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')