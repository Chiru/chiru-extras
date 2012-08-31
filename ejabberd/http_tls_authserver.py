# Simple json auth server example

import BaseHTTPServer, SimpleHTTPServer
import ssl, json

users = { "user":"password", "seconduser":"secret" }

class AuthRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def check_password(self, username, password):
        if username in users:
            return users.get(username) == password
        return False

    def do_POST(self):
        if self.path != '/authenticate':
            self.send_response(404)
            self.end_headers()
            self.wfile.write('POST only to /authenticate.\n')
            return
        cl = self.headers.get('content-length')
        badness = None
        if cl:
            post_data = self.rfile.read(int(cl))
        else:
            post_data = self.rfile.read()
        
        try:
            authreq = json.loads(post_data)
        except ValueError, what:
            badness = 'Malformed JSON: %s' % what
            print 'postdata', repr(post_data)
        else:
            t = authreq.get('req-type')
            u = authreq.get('username')
            p = authreq.get('password')
            if not (t and u and p):
                badness = 'key missings or in JSON message, need: req-type, username, password'
            
        if badness:
            self.send_response(400)
            self.end_headers()
            self.wfile.write('error: ' + badness + '\n')
            return


        if self.check_password(u, p):
            rd = dict(status="allow")
        else:
            rd = dict(status="deny")
        self.send_json_response(rd)

    def send_json_response(self, data):
        self.send_response(200)
        json_data = json.dumps(data) + "\n"
        self.send_header('Content-Length', str(len(json_data)))
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json_data)
        self.wfile.flush()

httpd = BaseHTTPServer.HTTPServer(('localhost', 4443), AuthRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='localhost.crt', keyfile='localhost.key', server_side=True)
print httpd.socket
httpd.serve_forever()

