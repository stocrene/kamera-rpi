import socketserver
import json
import time

from motors import motor_xy

# class TCPSocketHandler is used for getting packages across
# and for running the motor applications 
class TCPSocketHandler(socketserver.BaseRequestHandler):
    # create a motorcontroller class
    motor_table = motor_xy(12, 13, 50)
    motor_table.gotoposition(135,135)
#    for x in range(10):
#        motor_table.set_speeds(100,100)
#        time.sleep(0.1)
#    for x in range(60):
#        motor_table.set_speeds(-10,-50)
#        time.sleep(0.1)
    x, y = motor_table.get_positions()

    print("x_position=" +str(x) + " y_position=" +str(y))
    
    #handle a TCP-Package
    def handle(self):
        print("TCPSocketHandler::handle()")
        self.data = self.request.recv(1024).strip()     #get data
        self.data = str(self.data, 'utf-8')
        print("{} wrote:".format(self.client_address[0])+ self.data)
        #converting data (which is byte) to string

        #get motorpositions for response
        x,y = self.motor_table.get_positions()
 #       print(data)
  #      self.request.sendall(self.data.upper())
        #load data as json package
        jdata = json.loads(self.data)
        if 'Request' in jdata:      #if a request has been sent
            if jdata["Request"] == "position": 
                self.data = "{\"Answer\":position,\"x\"=" + str(x)+ "\"y\":"+str(y)+"}"
                self.request.sendall(self.data.encode('utf-8'))     #give back an answer
            else:
                self.request.sendall("Did not understand Request".encode('utf-8')) #give back an error message
        if 'pos' in jdata:          #if a movement command has been sent
            if jdata["pos"] == True:    #interpret if it is a coordinates package
                self.motor_table.gotoposition(jdata["X"], jdata["Y"])  
            else:                       #or a speed package
                self.motor_table.set_speeds(jdata["X"], jdata["Y"])
            self.data = "{\"X\"=" + str(x)+ "\"Y\":"+str(y)+"}"
            self.request.sendall(self.data.encode('utf-8')) #return the current position




    