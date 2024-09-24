import requests

class TrelloClient:
  def __init__(self, api_key, token):
      self.api_key = api_key
      self.token = token
      self.base_url = "https://api.trello.com/1"

  def create_card(self, list_id, name, desc=""):
      url = f"{self.base_url}/cards"
      query = {
          'key': self.api_key,
          'token': self.token,
          'idList': list_id,
          'name': name,
          'desc': desc
      }
      response = requests.post(url, params=query)
      return response.json()

  def update_card(self, card_id, name=None, desc=None):
      url = f"{self.base_url}/cards/{card_id}"
      query = {
          'key': self.api_key,
          'token': self.token
      }
      if name:
          query['name'] = name
      if desc:
          query['desc'] = desc
      response = requests.put(url, params=query)
      return response.json()

  def list_cards(self, board_id):
      url = f"{self.base_url}/boards/{board_id}/cards"
      query = {
          'key': self.api_key,
          'token': self.token
      }
      response = requests.get(url, params=query)
      return response.json()