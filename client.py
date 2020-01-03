import information
import socket
from dataTypes import *
from noiseEncryption import *
import hashlib
import time

class Client:

    def __init__(self,serverHostname):
        self.serverHostname=serverHostname
        self.com_socket=None


        self.client = Noise()

        self.client.connectToNoise("localhost", 6222)


    def SetupConnection(self):
        protocol = U8(information.protocol["Mining Protocol"])
        min_version = U16(information.min_version)
        max_version = U16(information.max_version)
        flags = U32(information.flags)
        endpoint_host = STR0_255(information.endpoint_host)
        endpoint_port = U16(information.endpoint_port)
        vendor = STR0_255(information.vendor)
        hardware_version = STR0_255((information.hardware_version))
        firmware = STR0_255(information.firmware)
        device_id = STR0_255(information.device_id)

        payload = protocol+min_version+max_version+flags+endpoint_host+endpoint_port+vendor+hardware_version+firmware+device_id
        frame = FRAME(0x0abc,"SetupConnection",payload)

        self.client.sendNoiseFrame(frame)

        frame = self.client.receiveNoiseFrame()
        msg_type = frame[2]

        if msg_type == 0x01:
            print("setup success")
            return True
        elif msg_type ==0x02:
            print("setup error")
            self.client.closeNoiseConnection()
            return False
        else:
            print("bad msg type")

    def OpenStandartMiningChannel(self):

        unique = str(time.time())
        unique = hashlib.sha256(unique.encode()).hexdigest()
        request_id = U32(int(unique[:8],16))

        #print(int(unique[:8],16))

        #print(request_id)

        user_identity = STR0_255(information.username)

        nominal_hash_rate = U32(information.hash_rate)

        max_target = U256(information.max_target)

        payload = request_id+user_identity+nominal_hash_rate+max_target

        frame = FRAME(0,"OpenStandardMiningChannel",payload)

        self.client.sendNoiseFrame(frame)

        frame_server = self.client.receiveNoiseFrame()

        msg_type = frame_server[2]

        if msg_type == 0x11:


            request_id_server = parse_bytes_to_int(frame_server,6,10)
            #print(request_id_server)

            channel_id = int(parse_bytes_to_int(frame_server,10,14))
            #print(channel_id)

            print("open standard channel success. Channel id:", channel_id)

            return channel_id
        elif msg_type == 0x12:
            length = frame_server[11]
            error_code = frame_server[11:12+length]
            print("open standard channel error: "+error_code.decode())

            return
        else:
            print("bad msg type")







    def MiningProtocolSetup(self):
        setup = self.SetupConnection()
        if setup:
            channel_id = self.OpenStandartMiningChannel()

            if channel_id:

                pass





        """s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            self.SetupMiningConnection()"""











