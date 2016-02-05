import requests
import json

class Webhook(object):
  def __init__(self, webhook_url, s3_url):
    self.webhook_url = webhook_url
    self.s3_url = s3_url

  def get(self, collection):
    query = '?limit=20'
    url = self.webhook_url + '/' + collection + query
    r = requests.get(url)

    if not r.status_code / 100 == 2:
      return

    json_list = json.loads(r.text)
    return json_list

  def send(self, docs):
    docs = json.dumps(docs)
    
    headers = {
      'Content-Type': 'application/octet-stream'
    }
    params = {
      'name': 'index.json'
    }

    r = requests.put(self.s3_url, data=docs, params=params, headers=headers)
    
    if not r.status_code / 100 == 2:
      print r.status_code
      return

    return r.text
