
"""
	REST JSON API for designing transformation files

	Based on:
	* https://mafayyaz.wordpress.com/2013/02/08/writing-simple-http-server-in-python-with-rest-and-json/
"""

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from re import search
from socketserver import ThreadingMixIn
from sys import stdout
from os.path import join
from misc import BASE_DIR


def get_args(url):
	"""
		:return: action, argument, rest
	"""
	match = search(r'/([^/]+)/([^/]+)/?(.*)', url)
	if match is not None:
		return match.groups()
	match = search(r'/([^/]+)/?', url)
	if match is not None:
		return match.groups()[0], None, ''
	return None, None, url[1:]


def serve_file(self, path, content_type):
	self.send_response(200)
	self.send_header('Content-Type', content_type)
	self.end_headers()
	with open(join(BASE_DIR, 'view', path), 'rb') as fh:
		self.wfile.write(fh.read())


class HTTPRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		# http://www.freefavicon.com/freefavicons/objects/iconinfo/red-highlighter-152-190158.html
		print('GET', self.path)
		action, argument, rest = get_args(self.path)
		if action is None:
			serve_file(self, 'index.html', 'text/html')
		elif action == 'favicon.png':
			serve_file(self, 'favicon.png', 'image/png')
		elif action == 'None':
			pass
		else:
			self.send_response(200)
			self.end_headers()
		return
		self.send_response(200)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()
		self.wfile.write('hello there!')

	def do_POST(self):
		raise NotImplementedError()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	allow_reuse_address = True

	def shutdown(self):
		self.socket.close()
		HTTPServer.shutdown(self)


class SimpleHttpServer():
	def __init__(self, ip, port):
		self.server = ThreadedHTTPServer((ip,port), HTTPRequestHandler)

	def start(self):
		self.server_thread = threading.Thread(target = self.server.serve_forever)
		self.server_thread.daemon = True
		self.server_thread.start()

	def wait_for_thread(self):
		self.server_thread.join()

	def stop(self):
		self.server.shutdown()
		self.wait_for_thread()


def run_server(host = 'localhost', port = 7199):
	server = SimpleHttpServer(host, port)
	stdout.write('Server running at\n\nhttp://{0:s}:{1:d}/\n\n'.format(host, port))
	stdout.write('Open it in your browser to use the interface\nSend a keyboard interrupt to stop (usually ctrl+C).')
	server.start()
	try:
		server.wait_for_thread()
	except KeyboardInterrupt:
		print('Server stopped')


