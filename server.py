from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import ssl
import os

class S(BaseHTTPRequestHandler):
    ran_script_file = 'js.check'

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if not os.path.isfile(self.ran_script_file):
            if ".html" in self.path:
                site = open(self.path[1:], 'r')
            else:
                site = open("index.html", 'r')
            content = ""
            for line in site.readlines():
                content += line
            site.close()
            self._set_headers()
            self.wfile.write(content)
        else:
            self.wfile.write("<html><body>ran javascript</body></html>")
            os.remove(self.ran_script_file)

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print "Post request recieved: " + post_data # <-- Print post data
        #token = file(self.ran_script_file, 'w')
        #token.close()
        #self._set_headers()
        #self.wfile.write("<html><body><h1>POST!</h1><pre>" + post_data + "</pre></body></html>")


def run(server_class=HTTPServer, handler_class=S, port=80, use_ssl = False):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    if use_ssl:
        httpd.socket = ssl.wrap_socket (httpd.socket, certfile='server.pem', server_side=True)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(use_ssl=bool(argv[1]))
    else:
        run()
