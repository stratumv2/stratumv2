from dataTypes import *
import messages

#integer = msgTypesConverter(0x00,1)

#print(integer)


testNumber = [0x1,0x2,0x3]

data = parse_bytes_to_int(testNumber)
#print(data)




"""m1 = messages.SetupConnectionError(4,"chepa")

m2 = messages.SetupConnectionError(m1.raw())

print(m2.error_code)

m3 = messages.ChannelEndpointChanged(34)

m4 = messages.ChannelEndpointChanged(m3.raw())

print(m4.channel_id)

m5 = messages.OpenStandardMningChannel(1,"sthiagolg",50000,312000)

m6 = messages.OpenStandardMningChannel(m5.raw())

print(m6.max_target)

m7 = messages.OpenStandardMningChannelSuccess(2,3,4,b'seila',5)

m8 = messages.OpenStandardMningChannelSuccess(m7.raw())

print(m8.raw())


m9 = messages.OpenExtendedMiningChannelSuccess(1,2,3,4,b'vamo')

m10 = messages.OpenExtendedMiningChannelSuccess(m9.raw())

print(m10.request_id)"""

setupMsg = messages.SetupConnection(0,2,3,0,"127.0.0.1",6222,"bitman","s9i","swtwo","deviceID")

print(setupMsg.device_id)
print("len",setupMsg.raw().__len__())

print(setupMsg.raw())

setup2 = messages.SetupConnection(setupMsg.raw())





setupFrameRaw = messages.FRAME(setupMsg).raw()

#print(type(setupFrameRaw))

decodeFrame = messages.FRAME(setupFrameRaw)

print(decodeFrame.payload.vendor)

#print(decodeFrame.raw())

#print(decodeFrame.payload)

#decodeFrame = messages.FRAME(setupFrameRaw)



