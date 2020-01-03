from dataTypes import *

class SetupConnection:

    MINING_PROTOCOL=0
    JOB_NEGOTIATION_PROTOCOL = 1
    TEMPLATE_DISTRIBUTION_PROTOCOL = 2
    JOB_DISTRIBUTION_PROTOCOL = 3



    def __init__(self,*args):

        #print(args[0])
        if len(args)==1:
            self.protocol=args[0][0]
            #print(self.protocol)
            self.min_version = parse_bytes_to_int(args[0][1:2])
            #print(self.min_version)
            self.max_version = parse_bytes_to_int(args[0][3:4])
            #print(self.max_version)
            self.flags = parse_bytes_to_int(args[0][5:8])
            #print(self.flags)
            l1 = args[0][9]

            self.endpoint_host = args[0][10:10+l1]
            #print(self.endpoint_host)
            self.endpoint_port = parse_bytes_to_int(args[0][10+l1:12+l1])
            #print(self.endpoint_port)
            l2 = args[0][12+l1]

            self.vendor = args[0][13+l1:13+l1+l2]
            #print(self.vendor)
            l3 = args[0][13+l1+l2]
            #print(l3)
            self.hardware_version = args[0][14+l1+l2:14+l1+l2+l3]
            #print(self.hardware_version)
            l4 = args[0][14+l1+l2+l3]
            self.firmware = args[0][15+l1+l2+l3:15+l1+l2+l3+l4]
            #print(self.firmware)
            l5 = args[0][16+l1+l2+l3+l4]
            self.device_id = args[0][16+l1+l2+l3+l4:16+l1+l2+l3+l4+l5]
        elif len(args)==10:
            self.protocol = args[0]
            self.min_version = args[1]
            self.max_version = args[2]
            self.flags = args[3]

            self.endpoint_host = args[4]
            self.endpoint_port = args[5]

            self.vendor = args[6]

            self.hardware_version = args[7]

            self.firmware = args[8]

            self.device_id = args[9]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U8(self.protocol)+U16(self.min_version)+U16(self.max_version)+U32(self.flags)+STR0_255(self.endpoint_host)+U16(self.endpoint_port)+STR0_255(self.vendor)+STR0_255(self.hardware_version)+STR0_255(self.firmware)+STR0_255(self.device_id)


class SetupConnectionSuccess:

    def __init__(self,*args):
        if len(args) == 1:
            self.used_version = parse_bytes_to_int(args[0][:2])
            self.flags = parse_bytes_to_int(args[0][2:6])

        elif len(args) == 2:
            self.used_version = args[0]
            self.flags = args[1]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U16(self.used_version)+U32(self.flags)

class SetupConnectionError:
    def __init__(self,*args):
        #print(args[0])
        if len(args) == 1:
            self.flags=parse_bytes_to_int(args[0][:4])
            l=args[0][4]
            #print(l)
            self.error_code = args[0][5:5+l]
            #print(self.error_code)
        elif len(args) == 2:
            self.flags=args[0]
            self.error_code=args[1]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.flags)+STR0_255(self.error_code)


class ChannelEndpointChanged:
    def __init__(self,*args):
        if len(args) == 1:
            if type(args[0])==int:
                self.channel_id=args[0]
            else:
                self.channel_id=parse_bytes_to_int(args[0])

        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.channel_id)

class OpenStandardMningChannel:
    def __init__(self,*args):

        if len(args) == 1:
            self.request_id=parse_bytes_to_int(args[0][:4])
            l=args[0][4]

            self.user_identity = args[0][5:5+l]
            self.nominal_hash_rate = parse_bytes_to_int(args[0][5+l:9+l])
            self.max_target = parse_bytes_to_int(args[0][9+l:9+l+32])
        elif len(args) == 4:
            self.request_id=args[0]
            self.user_identity=args[1]
            self.nominal_hash_rate =args[2]
            self.max_target = args[3]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.request_id)+STR0_255(self.user_identity)+U32(self.nominal_hash_rate)+U256(self.max_target)

class OpenStandardMningChannelSuccess:
    def __init__(self,*args):

        if len(args) == 1:
            self.request_id=parse_bytes_to_int(args[0][:4])


            self.channel_id = parse_bytes_to_int(args[0][5:9])
            self.target = parse_bytes_to_int(args[0][9:9+31])
            l = args[0][9+31]
            self.extranonce_prefix = args[0][41:41+l]
            self.group_channel_id = parse_bytes_to_int(args[0][41+l:46+l])

        elif len(args) == 5:
            self.request_id=args[0]
            self.channel_id=args[1]
            self.target =args[2]
            self.extranonce_prefix = args[3]
            self.group_channel_id = args[4]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.request_id)+U32(self.channel_id)+U256(self.target)+B0_255(self.extranonce_prefix)+U32(self.group_channel_id)


class OpenExtendedMiningChannel:
    def __init__(self,*args):

        if len(args) == 1:
            self.request_id=parse_bytes_to_int(args[0][:4])
            l=args[0][4]

            self.user_identity = args[0][5:5+l]
            self.nominal_hash_rate = parse_bytes_to_int(args[0][5+l:9+l])
            self.max_target = parse_bytes_to_int(args[0][9+l:9+l+32])
            self.min_extranonce_size = parse_bytes_to_int(args[0][9+l+32:9+l+32+4])

        elif len(args) == 5:
            self.request_id=args[0]
            self.user_identity=args[1]
            self.nominal_hash_rate =args[2]
            self.max_target = args[3]
            self.min_extranonce_size = args[4]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.request_id)+STR0_255(self.user_identity)+U32(self.nominal_hash_rate)+U256(self.max_target)+U32(self.min_extranonce_size)


class OpenExtendedMiningChannelSuccess:
    def __init__(self,*args):

        if len(args) == 1:
            self.request_id=parse_bytes_to_int(args[0][:4])


            self.channel_id = parse_bytes_to_int(args[0][5:9])
            self.target = parse_bytes_to_int(args[0][9:9+31])

            self.extranonce_size = parse_bytes_to_int(args[0][40:42])
            l = args[0][42]
            self.extranonce_prefix = args[0][43:43+l]

        elif len(args) == 5:
            self.request_id=args[0]
            self.channel_id=args[1]
            self.target =args[2]
            self.extranonce_size = args[3]
            self.extranonce_prefix = args[4]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.request_id)+U32(self.channel_id)+U256(self.target)+U16(self.extranonce_size)+B0_255(self.extranonce_prefix)



class OpenMiningChannelError:
    def __init__(self, *args):
        # print(args[0])
        if len(args) == 1:
            self.flags = parse_bytes_to_int(args[0][:4])
            l = args[0][4]
            # print(l)
            self.error_code = args[0][5:5 + l]
            # print(self.error_code)
        elif len(args) == 2:
            self.flags = args[0]
            self.error_code = args[1]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.flags) + STR0_255(self.error_code)

class UpdateChannel:
    def __init__(self,*args):

        if len(args) == 1:
            self.channel_id=parse_bytes_to_int(args[0][:4])

            self.nominal_hash_rate = parse_bytes_to_int(args[0][4:8])
            self.maximum_target = parse_bytes_to_int(args[0][8:40])
        elif len(args) == 3:
            self.channel_id=args[0]

            self.nominal_hash_rate =args[1]
            self.maximum_target = args[2]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.channel_id)+ U32(self.nominal_hash_rate)+U256(self.maximum_target)

class UpdateChannelError:
    def __init__(self,*args):
        #print(args[0])
        if len(args) == 1:
            self.channel_id=parse_bytes_to_int(args[0][:4])
            l=args[0][4]
            #print(l)
            self.error_code = args[0][5:5+l]
            #print(self.error_code)
        elif len(args) == 2:
            self.channel_id=args[0]
            self.error_code=args[1]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.channel_id)+STR0_255(self.error_code)

class CloseChannel:
    def __init__(self,*args):
        #print(args[0])
        if len(args) == 1:
            self.channel_id=parse_bytes_to_int(args[0][:4])
            l=args[0][4]
            #print(l)
            self.reason_code = args[0][5:5+l]
            #print(self.error_code)
        elif len(args) == 2:
            self.channel_id=args[0]
            self.reason_code=args[1]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.channel_id)+STR0_255(self.reason_code)

class SetExtranoncePrefix:
    def __init__(self,*args):

        if len(args) == 1:
            self.channel_id=parse_bytes_to_int(args[0][:4])
            l=args[0][4]

            self.extranonce_prefix = args[0][5:5+l]

        elif len(args) == 2:
            self.channel_id=args[0]
            self.extranonce_prefix=args[1]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.channel_id)+B0_255(self.extranonce_prefix)

