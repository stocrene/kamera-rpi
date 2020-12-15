import socketserver
import json

from servo_hw import servomotor

class TCPSocketHandler(socketserver.BaseRequestHandler):
    # Request Handler class for the Server.
    sx = servomotor(12, 50)
    sy = servomotor(13, 50)
    sx.initialize()
    sy.initialize()
    def handle(self):
        print("TCPSocketHandler::handle()")
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        #converting data (which is byte) to string
        data = str(self.data,'utf-8')
        print(data)
        self.request.sendall(self.data.upper())
        jdata = json.loads(data)
        print(str(jdata["X"]) + " " + str(jdata["Y"]))
        self.sx.gotoPos(jdata["X"]+0.0, 30)
        self.sy.gotoPos(jdata["Y"]+0.0, 30)



    