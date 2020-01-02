from dataTypes import *

integer = msgTypesConverter(0x00,1)

#print(integer)


testNumber = [0x1,0x2,0x3]

data = parse_bytes_to_int(testNumber)
#print(data)
