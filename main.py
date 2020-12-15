
import socketserver

from tcp_server import TCPSocketHandler

if __name__ == "__main__":
# set Host and Port
    HOST, PORT = "localhost", 10000
#instantiate Server and Bynd to Port and Handler
    server = socketserver.TCPServer(('',PORT),TCPSocketHandler)
    print("Opened Server")
#tell the Server to run until program end
    server.serve_forever()

