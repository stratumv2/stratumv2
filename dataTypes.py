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

def FRAME(extension_type,msg_type,msg_length,payload):

    #msg_length=payload.__len__()
    return




