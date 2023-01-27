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

file_dir = "./www"
CODE200 = "HTTP/1.1 200 OK\r\n"
CODE301 = "HTTP/1.1 301 Moved Permanently\r\n"
CODE404 = "HTTP/1.1 404 NOT FOUND\r\n"
CODE405 = "HTTP/1.1 405 Method Not Allowed\r\n"
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'



class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.msg = self.data.decode("utf-8").split()
        #print(self.msg)
        method_type = self.msg[0]
        if(method_type == 'GET'):
            self.code = self.check_path(file_dir + self.msg[1])
            self.request.sendall(self.code)
        else:
            self.request.sendall(bytearray(CODE405 + "Date: " + datetime.datetime.utcnow().strftime(GMT_FORMAT),'utf-8'))

        

    def check_path(self,path):
        content_type = self.msg[1].split('.')
        path_list = self.msg[1].split('/')
        get_path = path_list[-1]

        if not os.path.exists(path):
            #print("4041")
            return bytearray(CODE404 + "Date: " + datetime.datetime.utcnow().strftime(GMT_FORMAT) + "\r\n",'utf-8')
        if ".." in path_list:
            #print("4042")
            return bytearray(CODE404 + "Date: " + datetime.datetime.utcnow().strftime(GMT_FORMAT) + "\r\n",'utf-8')
        if os.path.isdir(path) and ".." not in get_path:
            if self.msg[1][-1] != "/" and "." not in get_path:
                str = "HTTP/1.1 301 Moved Permanently\r\nLocation: " + self.msg[1] + "/\r\n" + "Date:" + datetime.datetime.utcnow().strftime(GMT_FORMAT) + "\r\n"
                #print("here")
                ret_code = bytearray(str,'utf-8')
                return ret_code
            #print("2001")
            f = open(path + "index.html",'r')
            content = f.read()
            str = "Content-Type: text/html\r\n" + "Date: " + datetime.datetime.utcnow().strftime(GMT_FORMAT) + "\r\n\r\n" + content + "\r\n"
            ret_code = bytearray("HTTP/1.1 200 OK\r\n" + str,'utf-8')
            f.close()
            return ret_code

        if content_type[1] == "css" or content_type[1] == "html" and os.path.isfile(path):
            #print("2002")
            f = open(path,'r')
            content = f.read()
            str = "Content-Type: text/" + content_type[1] + "\r\n" + "Date: " + datetime.datetime.utcnow().strftime(GMT_FORMAT) + "\r\n\r\n" + content + "\r\n"
            ret_code = bytearray("HTTP/1.1 200 OK\r\n" + str,'utf-8')
            f.close()
            return ret_code


        
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()