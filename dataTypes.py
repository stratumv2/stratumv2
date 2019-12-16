import array
import binascii
import ctypes
import struct

def BOOL(bool):

    if bool:
        bool=True
    else:
        bool=False

    s = struct.Struct("<" + ' ?')

    b = ctypes.create_string_buffer(1)

    s.pack_into(b, 0, bool)
    #print(b.raw)
    #print(s.size())

    return b.raw

def U8(inter):

    assert(type(inter) is int), "not integer"

    if inter >= 2**8:
        raise Exception("Overflow")

    return (inter).to_bytes(1, byteorder='little')

def U16(inter):

    assert(type(inter) is int), "not integer"

    if inter >= 2**16:
        raise Exception("Overflow")

    return (inter).to_bytes(2, byteorder='little')

def U24(inter):

    assert(type(inter) is int), "not integer"

    if inter >= 2**24:
        raise Exception("Overflow")

    return (inter).to_bytes(3, byteorder='little')

def U32(inter):

    assert(type(inter) is int), "not integer"

    if inter >= 2**32:
        raise Exception("Overflow")

    return (inter).to_bytes(4, byteorder='little')

def U256(inter):

    assert(type(inter) is int), "not integer"

    if inter >= 2**256:
        raise Exception("Overflow")

    return (inter).to_bytes(32, byteorder='little')

def STR0_255(string):

    assert (type(string) is str), "not string"

    length = string.__len__()

    if length not in range(0,2**8):
        raise Exception("Overflow")

    s = struct.Struct("<" + ' '+str(length)+'s')

    b = ctypes.create_string_buffer(length)

    s.pack_into(b, 0, string.encode('utf-8'))

    return U8(length)+b.raw

def B0_255(_bytes):
    assert (type(_bytes) is bytes), "not bytes"

    length = _bytes.__len__()

    if length not in range(0, 2 ** 8):
        raise Exception("Overflow")

    return U8(length)+_bytes

def B0_64K(_bytes):
    assert (type(_bytes) is bytes), "not bytes"

    length = _bytes.__len__()

    if length not in range(0, 2 ** 16):
        raise Exception("Overflow")

    return U16(length)+_bytes

def B0_16M(_bytes):
    assert (type(_bytes) is bytes), "not bytes"

    length = _bytes.__len__()

    if length not in range(0, 2 ** 24):
        raise Exception("Overflow")

    return U24(length)+_bytes

def BYTES(_bytes):
    assert (type(_bytes) is bytes), "not bytes"

    return _bytes

def PUBKEY(pubKey):
    return

def SEQ0_255():
    return

def SEQ0_64K():
    return

def msgTypesConverter(message_type,channel_msg_bit):
    #just to make the task easier (copy from spec)

    assert (channel_msg_bit==0 or channel_msg_bit==1)
    if channel_msg_bit == 1:
        channel_msg_bit = 0b10000000

    result = message_type | channel_msg_bit

    return result

def FRAME(extension_type,msg_type,payload):
    #extension_type = 0x0ABC
    #extension_type = 0x8ABC
    extension_type = 0

    msg_type_list = {"SetupConnection":[0x00,0],
                     "SetupConnection.Success":[0x01,0],
                     "SetupConnection.Error":[0x02,0],
                     "ChannelEndpointChanged":[0x03,1],
                     "OpenStandardMiningChannel":[0x10,0],
                     "OpenStandardMiningChannel.Success":[0x11,0],
                     "OpenStandardMiningChannel.Error":[0x12,0],
                     "OpenExtendedMiningChannel":[0x13,0],
                     "OpenExtendedMiningChannel.Success":[0x14,0],
                     "OpenExtendedMiningChannel.Error":[0x15,0],
                     "UpdateChannel":[0x16,1],
                     "UpdateChannel.Error":[0x17,1],
                     "CloseChannel":[0x18,1],
                     "SetExtranoncePrefix":[0x19,1],
                     "SubmitSharesStandard":[0x1a,1],
                     "SubmitSharesExtended":[0x1b,1],
                     "SubmitShares.Success":[0x1c,1],
                     "SubmitShares.Error":[0x1d,1],
                     "NewMiningJob":[0x1e,1],
                     "NewExtendedMiningJob":[0x1f,1],
                     "SetNewPrevHash":[0x20,1],
                     "SetTarget":[0x21,1],
                     "SetCustomMiningJob":[0x22,0],
                     "SetCustomMiningJob.Success":[0x23,0],
                     "SetCustomMiningJob.Error":[0x24,0],
                     "Reconnect":[0x25,0],
                     "SetGroupChannel":[0x26,0],
                     "AllocateMiningJobToken":[0x50,0],
                     "AllocateMiningJobToken.Success":[0x51,0],
                     "AllocateMiningJobToken.Error":[0x52,0],
                     "IdentifyTransactions":[0x53,0],
                     "IdentifyTransactions.Success":[0x54,0],
                     "ProvideMissingTransactions":[0x55,0],
                     "ProvideMissingTransactions.Success":[0x56,0],
                     "CoinbaseOutputDataSize":[0x70,0],
                     "NewTemplate":[0x71,0],
                     "SetNewPrevHashTDP":[0x72,0],
                     "RequestTransactionData":[0x73,0],
                     "RequestTransactionData.Success":[0x74,0],
                     "RequestTransactionData.Error":[0x75,0],
                     "SubmitSolution":[0x76,0]

                     }
    msg_type_pair = msg_type_list[msg_type]

    msg_type = msgTypesConverter(msg_type_pair[0],msg_type_pair[1])

    msg_length = payload.__len__()

    return U8(extension_type)+U8(msg_type)+U24(msg_length)+BYTES(payload)






