#!/usr/bin/env python
# encoding: utf-8
from app import server
from gevent.pywsgi import WSGIServer


http_server = WSGIServer(('localhost', 5001), server)
http_server.serve_forever()
