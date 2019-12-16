import socket
import threading
from dataTypes import *
from noiseEncryption import *


class Server:

    def __init__(self):
        self.connectionsList = []
        self.version = 2
        self.flags = 0


    def SetupConnection(self):
        return
    """

    def StartServer(self):


        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        host = socket.gethostname()

        host = "127.0.0.1"

        print(host)

        port = 6222



        serversocket.bind((host, port))



        serversocket.listen(-1)


        while True:

            print("Waiting for connections on port ", port)

            clientsocket, addr = serversocket.accept()

            print("Got a connection from %s" % str(addr))

            #self.connectionsList.append(clientsocket)

            clientSetupMsg = clientsocket.recv(1024)

            #check if it is okay or not

            min_version = clientSetupMsg[1:2]

            max_version = clientSetupMsg[3:4]



            min_version = int.from_bytes(min_version, byteorder='little')


            max_version = int.from_bytes(max_version, byteorder='little')

            if min_version<= self.version<=max_version:
                clientsocket.send(self.SetupMiningConnectionSucessMsg())
                self.connectionsList.append(clientsocket)
                print("connection started with peer")
            else:
                clientsocket.send(self.SetupMiningConnectionErrorMsg(["version"]))
                print("closing connection")
                clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,struct.pack('ii', 1, 0))

                clientsocket.close()




    def SetupMiningConnectionSucessMsg(self):
        used_version= U16(self.version)
        flags = U32(self.flags)

        return used_version+flags


    def SetupMiningConnectionErrorMsg(self,flagsList):

        flags = 0b0

        error = "not able to set up the connection due an error:\n"

        for flag in flagsList:
            if flag == "cli_flags":
                flags = flags | 0b1
                error = error+"\t-unsupported-feature-flags"

            if flag == "protocol":
                flags = flags | 0b10
                error = error + "\t-unsupported-protocol"

            if flag == "version":
                flags = flags | 0b100
                error = error + "\t-protocol-version-mismatch"

        #print(flags)

        flags = int(flags)

        #print(flags)


        flags = U32(flags)
        error_code= STR0_255(error)

        return flags+error_code"""

