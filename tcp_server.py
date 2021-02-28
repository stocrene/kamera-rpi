import socketserver
import json
import time

from motors import motor_xy

motor_table = motor_xy(12, 13, 50)
#motor_table.gotoposition(135,135)
# class CommunicationHandler is used for getting packages across
# and for running the motor applications 
class CommunicationHandler(socketserver.BaseRequestHandler):
    x, y = motor_table.get_positions()

    print("x_position=" +str(x) + " y_position=" +str(y))
    
    #handle a TCP-Package
    def handle(self):
    #    print("CommunicationHandler::handle()")
        self.data = self.request.recv(1024).strip() #get data
        self.data = str(self.data, 'utf-8')         #convert data
        #get motorpositions for response
        print("CommunicationHandler received:" + self.data)
        x,y = motor_table.get_positions()
        #load data as json package
        essential_load =["X", "Y", "pos"] 
        jdata = json.loads(self.data)
        error_str = ""
        for i in essential_load:
            if i not in jdata:
                error_str += "Could not find essential " + i +" in this package! "

        if error_str == "":
            if jdata["pos"] == True:    #interpret if it is a coordinates package
                motor_table.gotoposition(jdata["X"], jdata["Y"])  
            else:                       #or a speed package
                motor_table.set_speeds(jdata["X"], jdata["Y"])
            self.data = "{\"X\":" + str(x)+ ",\"Y\":"+str(y)+"}"
            self.request.sendall(self.data.encode('utf-8')) #return the current position
        #    print("Replied with:"+self.data)
        else:
            print(error_str)
            self.request.sendall(error_str.encode('utf8'))

class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
    #    print("RequestHandler::handle()")
        self.data = self.request.recv(1024).strip() #geht data
        self.data =str(self.data, 'utf-8')          #convert data
        #get motorpositions for response
        x,y = motor_table.get_positions()
        jdata =json.loads(self.data)
        if'REQUEST' in jdata:
            if jdata["REQUEST"] == "position": 
                self.data = "{\"ANSWER\":position,\"X\":" + str(round(x))+ ",\"Y\":"+str(round(y))+"}"
                self.request.sendall(self.data.encode('utf-8'))     #give back an answer
            else:
                self.request.sendall("Did not understand Request".encode('utf-8')) #return an error message  
        else:
            self.request.sendall("Package does not include a Request".encode('utf-8'))  #return an error message          

    
