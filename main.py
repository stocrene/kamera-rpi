
import socketserver

from tcp_server import CommunicationHandler
from tcp_server import RequestHandler

if __name__ == "__main__":
# set Host and Port
    HOST, PORT = "localhost", 10000
    HOSTR, PORTR = "localhost", 10001
#instantiate Server and Bynd to Port and Handler
    servercom = socketserver.TCPServer(('',PORT),CommunicationHandler)
    serverreq = socketserver.TCPServer(('',PORTR),RequestHandler)
    print("Opened Servers")
#tell the Server to run until program end
    servercom.serve_forever()
    serverreq.serve_forever()

