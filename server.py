import socket
import threading
from dataTypes import *
from noiseEncryption import *

import noiseEncryption
import hashlib
import time
import random


class Server:

    def __init__(self):

        self.version = 2
        self.min_target = 30000
        self.target = 40000
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
        #print(msg_type)
        if msg_type == 0x00:
            self.SetupConnection(frame)
        if msg_type == 0x10:
            self.OpenStandardMiningChannel(frame)
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
            flags=0 #still to define
            error_code = "protocol-version-mismatch"

            payload = U32(flags)+STR0_255(error_code)

            frame_error = FRAME(0,"SetupConnection.Error",payload)

            self.server.sendNoiseFrame(frame_error)
            print("setup error")
            self.server.closeNoiseConnection()

    def OpenStandardMiningChannel(self,frame):

        #length = int.from_bytes(frame[11], byteorder='little')
        length = frame[10]

        #print(length)
        user_identity = frame[11:11+length]

        #print(frame)

        #print("username:",user_identity)

        nominal_hash_rate = int.from_bytes(frame[11+length:15+length], byteorder='little')

        #print(nominal_hash_rate)

        max_target = int.from_bytes(frame[15+length:47+length], byteorder='little')
        #print(max_target)

        request_id = parse_bytes_to_int(frame,6,10)
        #print(request_id)

        if max_target > self.min_target:
            unique = str(time.time())+str(random.random())
            unique = hashlib.sha256(unique.encode()).hexdigest()
            channel_id = int(unique[:8],16)

            payload = U32(request_id)+U32(channel_id)+U256(self.target)+B0_255(b'0')+U32(0)

            self.server.sendNoiseFrame(FRAME(0,"OpenStandardMiningChannel.Success", payload))
            print("channel created. Channel id:",channel_id)
        else:
            payload = U32(request_id)+STR0_255("max-target-out-of-range")
            self.server.sendNoiseFrame(FRAME(0,"OpenStandardMiningChannel.Error",payload))


