import information
import socket
from dataTypes import *

class Client:

    def __init__(self,serverHostname):
        self.serverHostname=serverHostname
        self.com_socket=None

    def SetupMessage(self):
        protocol = U8(information.protocol["Mining Protocol"])
        min_version= U16(information.min_version)
        max_version = U16(information.max_version)
        flags = U32(information.flags)
        endpoint_host = STR0_255(information.endpoint_host)
        endpoint_port =U16(information.endpoint_port)
        vendor = STR0_255(information.vendor)
        hardware_version = STR0_255((information.hardware_version))
        firmware = STR0_255(information.firmware)
        device_id = STR0_255(information.device_id)

        return protocol+min_version+max_version+flags+endpoint_host+endpoint_port+vendor+hardware_version+firmware+device_id


    def SetupMiningConnection(self):


        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.serverHostname, information.endpoint_port)

        s.connect((self.serverHostname,information.endpoint_port))


        #print("tcp connection failed.")

        setupMsg = self.SetupMessage()

        print("setup msg", setupMsg)


        s.send(setupMsg)

        response = s.recv(1024)

        print("resp",response)


        s.settimeout(1)

        try:
            response = s.recv(1024)

        except socket.timeout:
            self.com_socket=s
            print("Setup ok.")



    def OpenStandardMiningChannel(self):

        if not self.com_socket:
            print("Setup connection must be done first.")
            return
        else:
            self.SetupMiningConnection()











