import socket
import threading
from dataTypes import *
from noiseEncryption import *

import noiseEncryption


class Server:

    def __init__(self):

        self.version = 2
        self.server = noiseEncryption.Noise()
        self.server.HandleNoiseConnection()

    def functionSelecter(self):
        frame = self.server.receiveNoiseFrame()
        #extension_type = frame[0:1]
        msg_type = frame[2]
        #protocol = frame[6]
        #min_version = frame[7:8]
        #max_version = frame[9:10]
        #print(frame)
        print(msg_type)
        if msg_type == 0x00:
            self.SetupConnection(frame)
        #print((msg_type).from_bytes(1, byteorder='little'))
        #print((protocol).from_bytes(1, byteorder='little'))
        #print(min_version)
        #print(max_version)
        #print(int.from_bytes(version, byteorder='little'))



    def SetupConnection(self,frame):
        min_version = int.from_bytes(frame[7:8], byteorder='little')
        max_version = int.from_bytes(frame[9:10], byteorder='little')

        #by now, it only checks if the version are matched
        if min_version <= self.version <= max_version:
            flags = 0 #still to define
            payload = U16(self.version)+U32(flags)
            frame_success = FRAME(0,"SetupConnection.Success",payload)
            self.server.sendNoiseFrame(frame_success)
            print("setup success")
        else:
            flags=0 #still do define
            error_code = "protocol-version-mismatch"

            payload = U32(flags)+STR0_255(error_code)

            frame_error = FRAME(0,"SetupConnection.Error",payload)

            self.server.sendNoiseFrame(frame_error)
            print("setup error")
            self.server.closeNoiseConnection()


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

