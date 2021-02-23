
import socketserver
import threading


from tcp_server import CommunicationHandler
from tcp_server import RequestHandler

if __name__ == "__main__":
# set Host and Port
    HOST, PORT = "localhost", 10000
    HOSTR, PORTR = "localhost", 10001
#instantiate Server and Bind to Port and Handler
    servercom = socketserver.ThreadingTCPServer(('', PORT),CommunicationHandler)
    serverreq = socketserver.ThreadingTCPServer(('', PORTR),RequestHandler)
    print("Opened Servers")    
    serverComThread = threading.Thread(target = servercom.serve_forever, daemon=True)
    serverReqThread = threading.Thread(target = serverreq.serve_forever, daemon=True)
    serverComThread.start()
    serverReqThread.start()
#    servercom.serve_forever()
#    serverreq.serve_forever()
    print("made server permanent")
    serverComThread.join()
    serverReqThread.join()
#tell the Server to run until program end



