import requests
import json
from config import import CB_USER, CB_KEY

NICK = "anna"

class Cleverbot(object):
    def create(self):
        res = requests.post('https://cleverbot.io/1.0/create', json={'user': CB_USER, 'key': CB_KEY, 'nick': NICK})
    def ask(self, text):
        res = requests.post('https://cleverbot.io/1.0/ask', json={'user': CB_USER, 'key': CB_KEY, 'nick': NICK, 'text': text})
        if res.status_code == 200:
            return json.loads(res.text)['response']
        else:
            raise CleverbotError(res.text)

class CleverbotError(Exception):
    pass
