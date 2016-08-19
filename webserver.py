from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


class webserverHandler(BaseHTTPRequestHandler):
    # handles all get requests our server receives
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                # send message back to client
                self.wfile.write(output)
                print output 
                # exit if statement
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>Hola!</body></html>"
                # send message back to client
                self.wfile.write(output)
                print output
                # exit if statement
                return
                

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
	        # parses html form header into main value and dict of params

            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
	        # is this form data?
            
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
	            # get value of field and store in array
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output
        except:
            pass


def main():

    try:
        port = 8000
        # webserverhandler is made up name
        server = HTTPServer(('', port), webserverHandler)
        # create print statement to know sever is running
        print "web server running on port %s" % port
        server.serve_forever()
    # exception
    except KeyboardInterrupt:  # ctrl+c
        # when ^C entered, server stopped
        print "^C entered, stopping web server..."
        server.socket.close()

# instantiate our server and specify what port it will listen on
if __name__ == '__main__':
    main()
