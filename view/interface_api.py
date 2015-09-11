
"""
	REST JSON API for designing transformation files

	Based on:
	* https://mafayyaz.wordpress.com/2013/02/08/writing-simple-http-server-in-python-with-rest-and-json/
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import argparse
import re
import cgi



class HTTPRequestHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		if None != re.search('/api/v1/addrecord/*', self.path):
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
		if ctype == 'application/json':
			length = int(self.headers.getheader('content-length'))
			data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
			recordID = self.path.split('/')[-1]
			LocalData.records[recordID] = data
			print "record %s is added successfully" % recordID
		else:
			data = {}

			self.send_response(200)
			self.end_headers()
		else:
			self.send_response(403)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()

			return

	def do_GET(self):
		if None != re.search('/api/v1/getrecord/*', self.path):
			recordID = self.path.split('/')[-1]
		if LocalData.records.has_key(recordID):
			self.send_response(200)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
			self.wfile.write(LocalData.records[recordID])
		else:
			self.send_response(400, 'Bad Request: record does not exist')
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
		else:
			self.send_response(403)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
		return
