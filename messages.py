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

class SubmitSharesStandard:
    def __init__(self,*args):

        if len(args) == 1:
            self.channel_id=parse_bytes_to_int(args[0][:4])
            self.sequence_number = parse_bytes_to_int(args[0][4:8])
            self.job_id = parse_bytes_to_int(args[0][8:12])
            self.nonce = parse_bytes_to_int(args[0][12:16])
            self.ntime = parse_bytes_to_int(args[0][16:20])
            self.version = parse_bytes_to_int(args[0][20:24])
        elif len(args) == 6:
            self.channel_id=args[0]
            self.sequence_number=args[1]
            self.job_id = args[2]
            self.nonce = args[3]
            self.ntime = args[4]
            self.version =args[5]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.channel_id)+U32(self.sequence_number)+U32(self.job_id)+U32(self.nonce)+U32(self.ntime)+U32(self.version)


class SubmitSharesExtended:
    def __init__(self, *args):

        if len(args) == 1:
            self.channel_id = parse_bytes_to_int(args[0][:4])
            self.sequence_number = parse_bytes_to_int(args[0][4:8])
            self.job_id = parse_bytes_to_int(args[0][8:12])
            self.nonce = parse_bytes_to_int(args[0][12:16])
            self.ntime = parse_bytes_to_int(args[0][16:20])
            self.version = parse_bytes_to_int(args[0][20:24])
            l = args[0][24]
            self.extranonce = args[0][25:25+l]
        elif len(args) == 7:
            self.channel_id = args[0]
            self.sequence_number = args[1]
            self.job_id = args[2]
            self.nonce = args[3]
            self.ntime = args[4]
            self.version = args[5]
            self.extranonce = args[6]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.channel_id) + U32(self.sequence_number) + U32(self.job_id) + U32(self.nonce) + U32(
            self.ntime) + U32(self.version)+B0_255(self.extranonce)


class SubmitSharesSuccess:
    def __init__(self,*args):

        if len(args) == 1:
            self.channel_id=parse_bytes_to_int(args[0][:4])
            self.last_sequence_number = parse_bytes_to_int(args[0][4:8])
            self.new_submits_accepted_count = parse_bytes_to_int(args[0][8:12])
            self.new_shares_sum = parse_bytes_to_int(args[0][12:16])

        elif len(args) == 4:
            self.channel_id=args[0]
            self.last_sequence_number=args[1]
            self.new_submits_accepted_count = args[2]
            self.new_shares_sum = args[3]

        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.channel_id)+U32(self.last_sequence_number)+U32(self.new_submits_accepted_count)+U32(self.new_shares_sum)

class SubmitSharesError:
    def __init__(self,*args):

        if len(args) == 1:
            self.channel_id=parse_bytes_to_int(args[0][:4])
            self.sequence_number = parse_bytes_to_int(args[0][4:8])
            l = args[0][8]

            self.error_code =  args[0][8:8+l]
        elif len(args) == 3:
            self.channel_id=args[0]
            self.sequence_number=args[1]
            self.error_code = args[2]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.channel_id)+U32(self.sequence_number)+STR0_255(self.error_code)

class NewMiningJob:
    def __init__(self,*args):

        if len(args) == 1:
            self.channel_id=parse_bytes_to_int(args[0][:4])
            self.job_id = parse_bytes_to_int(args[0][4:8])
            self.future_job = args[0][8]
            self.version = parse_bytes_to_int(args[0][9:13])
            self.merkle_root = args[0][13:17]
        elif len(args) == 5:
            self.channel_id=args[0]
            self.job_id=args[1]
            self.future_job = args[2]
            self.version = args[3]
            self.merkle_root = args[4]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.channel_id)+U32(self.job_id)+BOOL(self.future_job)+U32(self.version)+U32(self.merkle_root)


class NewExtendedMiningJob:
    def __init__(self):
        print("TODO SEQ0_255")
        return


class SetNewPrevHash:
    def __init__(self,*args):

        if len(args) == 1:
            self.channel_id=parse_bytes_to_int(args[0][:4])
            self.job_id = parse_bytes_to_int(args[0][4:8])
            self.prev_hash = parse_bytes_to_int(args[0][8:40])
            self.min_ntime = parse_bytes_to_int(args[0][40:44])
            self.nbits = parse_bytes_to_int(args[0][44:48])
        elif len(args) == 5:
            self.channel_id=args[0]
            self.job_id=args[1]
            self.prev_hash = args[2]
            self.min_ntime = args[3]
            self.nbits = args[4]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.channel_id)+U32(self.job_id)+U256(self.prev_hash)+U32(self.min_ntime)+U32(self.nbits)

class SetCustomMiningJob:
    def __init__(self):
        print("TODO SEQ0_255")
        return

class SetCustomMiningJobSuccess:
    def __init__(self, *args):

        if len(args) == 1:
            self.channel_id = parse_bytes_to_int(args[0][:4])
            self.request_id = parse_bytes_to_int(args[0][4:8])
            self.job_id = parse_bytes_to_int(args[0][8:12])
            l1= args[0][12]

            self.coinbase_tx_prefix = args[0][13:13+l1]
            l2 = args[0][13+l1]
            self.coinbase_tx_sufix = args[0][14+l1:14+l1+l2]
        elif len(args) == 5:
            self.channel_id = args[0]
            self.request_id = args[1]
            self.job_id = args[2]
            self.coinbase_tx_prefix = args[3]
            self.coinbase_tx_sufix = args[4]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.channel_id) + U32(self.request_id)+U32(self.job_id)+B0_64K(self.coinbase_tx_prefix)+B0_64K(self.coinbase_tx_sufix)

class SetCustomMiningJobError:
    def __init__(self,*args):

        if len(args) == 1:
            self.channel_id=parse_bytes_to_int(args[0][:4])
            self.request_id = parse_bytes_to_int(args[0][4:8])
            l = args[0][8]

            self.error_code =  args[0][8:8+l]
        elif len(args) == 3:
            self.channel_id=args[0]
            self.request_id=args[1]
            self.error_code = args[2]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.channel_id)+U32(self.request_id)+STR0_255(self.error_code)

class SetTarget:
    def __init__(self,*args):

        if len(args) == 1:
            self.channel_id=parse_bytes_to_int(args[0][:4])
            self.maximum_target = parse_bytes_to_int(args[0][4:36])

        elif len(args) == 2:
            self.channel_id=args[0]
            self.maximum_target=args[1]

        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.channel_id)+U256(self.maximum_target)

class Reconnect:
    def __init__(self,*args):

        if len(args) == 1:
            l = args[0][0]
            self.new_host=args[0][1:1+l]
            self.new_port = parse_bytes_to_int(args[0][1+l:3+l])

        elif len(args) == 2:
            self.new_host=args[0]
            self.new_port=args[1]

        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return STR0_255(self.new_host)+U16(self.new_port)

class SetGroupChannel:
    def __init__(self):
        print("TODO SEQ0_255")
        return

class AllocateMiningJobToken:
    def __init__(self, *args):

        if len(args) == 1:
            l = args[0][0]
            self.user_identifier = args[0][1:1 + l]
            self.request_id = parse_bytes_to_int(args[0][1 + l:5 + l])

        elif len(args) == 2:
            self.user_identifier = args[0]
            self.request_id = args[1]

        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return STR0_255(self.user_identifier) + U32(self.request_id)

class AllocateMiningJobTokenSuccess:
    def __init__(self, *args):

        if len(args) == 1:

            self.request_id = parse_bytes_to_int(args[0][:4])
            l = args[0][4]
            self.mining_job_token = args[0][5:5+l]
            self.coinbase_output_max_additional_size = parse_bytes_to_int(args[0][5+l:9+l])
            self.async_mining_allowed = args[0][9+l]

        elif len(args) == 4:
            self.request_id = args[0]
            self.mining_job_token = args[1]
            self.coinbase_output_max_additional_size = args[2]
            self.async_mining_allowed = args[3]

        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.request_id)+B0_255(self.mining_job_token)+U32(self.coinbase_output_max_additional_size)+BOOL(self.async_mining_allowed)

class CommitMiningJob:
    def __init__(self):
        print("TODO SEQ0_255")
        return

class CommitMiningJobSuccess:
    def __init__(self,*args):
        if len(args) == 1:

            self.request_id = parse_bytes_to_int(args[0][:4])
            l = args[0][4]
            self.new_mining_job_token = args[0][5:5 + l]


        elif len(args) == 2:
            self.request_id = args[0]
            self.new_mining_job_token = args[1]


        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.request_id)+B0_255(self.new_mining_job_token)

class CommitMiningJobError:
    def __init__(self,*args):
        if len(args) == 1:

            self.request_id = parse_bytes_to_int(args[0][:4])
            l1 = args[0][4]
            self.error_code = args[0][5:5 + l1]
            l2 = args[0][5+l1]
            self.error_details = args[0][6+l1:6+l1+l2]


        elif len(args) == 3:
            self.request_id = args[0]
            self.error_code = args[1]
            self.error_details = args[2]


        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.request_id)+STR0_255(self.error_code)+B0_64K(self.error_details)

class IdentifyTransactions:
    def __init__(self,*args):
        if len(args) == 1:
            if type(args[0])==int:
                self.request_id=args[0]
            else:
                self.request_id=parse_bytes_to_int(args[0])

        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.request_id)


class IdentifyTransactionsSuccess:
    def __init__(self):
        print("TODO SEQ0_255")
        return

class ProvideMissingTransactions:
    def __init__(self):
        print("TODO SEQ0_255")
        return

class ProvideMissingTransactionsSucess:
    def __init__(self):
        print("TODO SEQ0_255")
        return


class CoinbaseOutputDataSize:
    def __init__(self,*args):
        if len(args) == 1:
            if type(args[0])==int:
                self.coinbase_output_max_additional_size=args[0]
            else:
                self.coinbase_output_max_additional_size=parse_bytes_to_int(args[0])

        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.coinbase_output_max_additional_size)


class NewTemplate:
    def __init__(self):
        print("TODO SEQ0_255")
        return

class SetNewPrevHashTDP:
    def __init__(self,*args):

        if len(args) == 1:
            self.template_id=parse_bytes_to_int(args[0][:8])
            self.prev_hash = parse_bytes_to_int(args[0][8:40])
            self.header_timestamp = parse_bytes_to_int(args[0][40:44])
            self.nbits = parse_bytes_to_int(args[0][44:48])
            self.target = parse_bytes_to_int(args[0][48:80])
        elif len(args) == 5:
            self.template_id=args[0]
            self.prev_hash=args[1]
            self.header_timestamp = args[2]
            self.nbits = args[3]
            self.target = args[4]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U64(self.template_id)+U256(self.prev_hash)+U32(self.header_timestamp)+U32(self.nbits)+U256(self.target)


class RequestTransactionData:
    def __init__(self,*args):
        if len(args) == 1:
            if type(args[0])==int:
                self.template_id=args[0]
            else:
                self.template_id=parse_bytes_to_int(args[0])

        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U64(self.template_id)


class RequestTransactionDataSuccess:
    def __init__(self):
        print("TODO SEQ0_255")
        return

class RequestTransactionDataError:
    def __init__(self,*args):

        if len(args) == 1:
            self.template_id=parse_bytes_to_int(args[0][:8])
            l=args[0][8]

            self.error_code = args[0][9:9+l]

        elif len(args) == 2:
            self.template_id=args[0]
            self.error_code=args[1]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U64(self.template_id)+STR0_255(self.error_code)

class SubmitSolution:
    def __init__(self,*args):

        if len(args) == 1:
            self.template_id=parse_bytes_to_int(args[0][:4])
            self.version = parse_bytes_to_int(args[0][4:8])
            self.header_timestamp = parse_bytes_to_int(args[0][8:12])
            self.header_nonce = parse_bytes_to_int(args[0][12:16])
            l = args[0][16]
            self.coinbase_tx = args[0][17:17+l]
        elif len(args) == 5:
            self.template_id=args[0]
            self.version=args[1]
            self.header_timestamp = args[2]
            self.header_nonce = args[3]
            self.coinbase_tx = args[4]
        else:
            raise Exception("wrong number of arguments")

    def raw(self):
        return U32(self.template_id)+U32(self.version)+U32(self.header_timestamp)+U32(self.header_nonce)+B0_64K(self.coinbase_tx)
    
