#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import threading
import time

import bottle
import raven

import webhook


def main():
  collections = os.environ.get('COLLECTIONS', '')
  s3_url = os.environ.get('S3', '')
  webhook_url = os.environ.get('WEBHOOK', '')
  sentry_url = os.environ.get('SENTRY', '')

  r = raven.Client(sentry_url)
  w = webhook.Webhook(webhook_url, s3_url)

  collections = collections.split(',')
  docs = {}

  while True:
    try:

      for collection in collections:
        doc = w.get(collection)
        docs[collection] = doc

      w.send(docs)

    except Exception as e:
      print e
      r.captureException()

    time.sleep(30*60) # 30 min.
  

@bottle.route('/')
def index():
  return ''

if __name__ == '__main__':
  reload(sys)
  sys.setdefaultencoding('utf-8')
  port = os.environ.get('PORT', 8888)

  if port == 8888:
    main()
  else:
    threading.Thread(target=main).start()
    bottle.run(host='0.0.0.0', port=port)
  
