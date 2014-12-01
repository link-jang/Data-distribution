#!/usr/bin/env python
#coding=utf-8

'''
Author: Gu Zhou, guzhou@xunlei.com

基于HTTP的脚本代理。
'''


import BaseHTTPServer 
import SimpleHTTPServer
import SocketServer
import subprocess
import threading
from urlparse import urlparse
from urlparse import parse_qs
from urllib import urlencode
from urllib import unquote
import httplib
import socket
import time
import fcntl
import os


import sys
sys.path.append('../conf/')
import config


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        qs = self.rfile.readline(content_length)
        query = parse_qs(qs)
        self.dispatch(self.path, query)

    def do_GET(self):
        req = urlparse(self.path)
        query = parse_qs(req.query)
        self.dispatch(req.path, query)

    def dispatch(self, path, query):
        if path == '/runsh.do':
            self.do_runsh(query)
        else:
            pass


    def do_runsh(self, query):
        status = 200
        res = ''
        try:
            blocking = unquote(query['blocking'][0])
            cmd = []
            cmd.append(unquote(query['sh'][0]))
            if 'args' in query: cmd.extend(unquote(query['args'][0]).split())
            if blocking == 'yes':
                pipe = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                ret = pipe.wait()
                if ret != 0: status = 500
                res = pipe.stdout.read() + pipe.stderr.read()
            else:
                subprocess.call(cmd)
        except KeyError, e:
            status = 400
            res = 'request parameter error\n'
        self.send_response(status)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(res)


class ThreadedHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        BaseHTTPServer.HTTPServer.__init__(self, server_address, RequestHandlerClass)
        flags = fcntl.fcntl(self.socket.fileno(), fcntl.F_GETFD)
        flags |= fcntl.FD_CLOEXEC
        fcntl.fcntl(self.socket.fileno(), fcntl.F_SETFD, flags)


if __name__ == '__main__':
    try:
        httpd = ThreadedHTTPServer(config.server_address, RequestHandler)
        httpd.serve_forever()
    except:
        pass
    sys.exit(-1)
