#!/usr/bin/python


from http.server import BaseHTTPRequestHandler, HTTPServer

f = open('test.txt', 'w')
f.write('Succeeded')
f.close()
