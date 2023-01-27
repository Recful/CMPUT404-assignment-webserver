#  coding: utf-8 
import socketserver
import os
import datetime
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
        # print ("Got a request of: %s\n" % self.data)
        self.decode_data = self.data.decode('utf-8').split()
        # print("Decoded request:\n",self.decode_data)

        self.method = self.decode_data[0]
        self.path = self.decode_data[1]
        # print("method:\n", self.method)
        # print("path:\n", self.path)

        self.base_path = './www'
        self.file_path = self.base_path + self.path
        # print("New Path:\n", self.file_path)

        self.status_code = ''
        if(self.method == 'GET'):
            self.status_code = self.status(self.file_path)
            # print("status_code: ", self.status_code)
            self.request.sendall(bytearray(self.status_code, 'utf-8'))
        else:
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n" + "Date: " + datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT') + '\r\n\r\n', 'utf-8'))
    def status(self, file_path):
        content_type = self.decode_data[1].split('.')
        paths = self.decode_data[1].split('/')
        last_char = paths[-1]
        # print("paths: \n", paths)


        if '../' in file_path: # check if contains../ 
            response = "HTTP/1.1 404 Not Found\r\n" + "Date: " + datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT') + '\r\n\r\n'
            return response

        if os.path.exists(file_path):
            if self.path[-1] != '/' and '.' not in last_char:
                response = "HTTP/1.1 301 Moved Permanently\r\nLocation: " + self.path + '/\r\n' + "Date: " + datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT') + '\r\n\r\n'
                return response

        if os.path.exists(file_path): # if file exist
            try:
                if content_type[1] == "css" or content_type[1] == "html":
                    target_file = open(file_path, 'r')
                    file_content = target_file.read()
                    response = "HTTP/1.1 200 OK\r\n" + 'Content-type: text/' + content_type[1] + '\r\n' + "Date: " + datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT') + '\r\n\r\n' + file_content + '\r\n'
                    target_file.close()
                    return response
            except:
                target_file = open(file_path + 'index.html', 'r')
                file_content = target_file.read()
                response = response = "HTTP/1.1 200 OK\r\n" + 'Content-type: text/html'  + '\r\n' + "Date: " + datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT') + '\r\n\r\n' + file_content + '\r\n'
                target_file.close()
                return response
        else: # if path not exist
            response = "HTTP/1.1 404 Not Found\r\n" + "Date: " + datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
            return response
        
        


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
