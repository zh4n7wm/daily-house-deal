#!/usr/bin/env python
# encoding: utf-8
from server import server
from app import app
from gevent.pywsgi import WSGIServer


http_server = WSGIServer(('localhost', 5001), server)
http_server.serve_forever()
