#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        data = self.data.decode('utf-8')
        self.dataArray = data.split()

        if self.dataArray !=[]:
            if self.dataArray[0] == 'GET':
                
                self.path = 'www' + self.dataArray[1]
                

                if '.html' not in self.dataArray[1] and '.css' not in self.dataArray[1]:
                    if self.dataArray[1][-1] != '/':

                        try:
                            open('www' + self.dataArray[1] + '/index.html')
                            updateURI = 'HTTP/1.1 301 Not Found!\r\nLocation:' + self.dataArray[1] + '/\r\n\r\n'
                            self.request.send(bytearray(updateURI, 'utf-8'))
                        except Exception as e:
                            self.send404()
                            print(e)
                            

                    elif  self.dataArray[1][-1] == '/':
                        newPath = 'www' + self.dataArray[1] + 'index.html'
                        self.sendIndex(newPath)

                    else: 
                        self.send404()

                elif '.html' in self.dataArray[1] :
                    try: 
                        open(self.path)
                        self.sendIndex(self.path)
                    except Exception as e:
                        self.send404()
                        print(e)
                elif '.css' in self.dataArray[1]:
                    # if self.dataArray[26] != 'Referer:':

                    #     self.request.send(b'HTTP/1.1 405 Method Not Allowed\r\n\r\n')
                    #     self.request.send(b'<!DOCTYPE html>\r\n<html> HTTP 405 Method Not Allowed</h1></body>\r\n')
                    
                    # else:
                    try:
                        open(self.path)
                        self.sendCSS(self.path)
                    except Exception as e:
                        self.send404()
                        print(e)
                    
                    
                else: 
                    self.request.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
                    self.request.send(b'<!DOCTYPE html>\r\n<html> HTTP 404 Error Not Found </h1></body>\r\n')

            elif self.dataArray[0] == 'HEAD':
                pass #Do something in when they say HEAD, not sure what yet
            else: 
                self.send405()
        else: 
            pass

    def send404(self):
        self.request.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
        self.request.send(b'<!DOCTYPE html>\r\n<html> HTTP 404 Not Found</h1></body>\r\n\r\n')
    
    def send405(self):
        self.request.send(b'HTTP/1.1 405 Method Not Allowed\r\n\r\n')
        self.request.send(b'<!DOCTYPE html>\r\n<html> HTTP 405 Method Not Allowed</h1></body>\r\n\r\n')
    
    def sendIndex(self, path):
        html= open(path, 'rb')
        html.seek(0,2)
        htmlSize = html.tell()
        html.seek(0)

        headers = b"HTTP/1.1 200 OK\r\n"
        headers += b"Content-Type: text/html; charset=UTF-8\r\n"
        headers += b"Content-Length: " + str(htmlSize).encode() + b"\r\n\n\n"
        self.request.send(headers)
        self.request.sendfile(html)
        self.request.send(b'\r\n\r\n')
        html.close()
        
    def sendCSS(self,path):
        css = open(path,'rb')
        css.seek(0,2)
        cssSize = css.tell()
        css.seek(0)
        
        headers = b"HTTP/1.1 200 OK\r\n"
        headers += b"Content-Type: text/css; charset=UTF-8\r\n"
        headers += b"Content-Length: " + str(cssSize).encode() + b"\r\n\n\n"
        self.request.send(headers)
        self.request.sendfile(css)
        self.request.send(b'\r\n\r\n')
        css.close()
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
