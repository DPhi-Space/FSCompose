import time
import struct
import socket

UART_READ_TIMEOUT           =   0.001
TCP_READ_TIMEOUT            =   0.001
FILE_PKT_CHUNK_SIZE         =   220
MAX_PKT_SIZE                =   512
START_WORD                  =   b'\xde\xad\xbe\xef'
START_WORD_SIZE             =   4         # bytes
CHECKSUM_SIZE               =   4         # bytes
METADATA_SIZE               =   4         # bytes (source, dest, size)
PACKET_ID_SIZE              =   1
HEADER_SIZE                 =   START_WORD_SIZE + PACKET_ID_SIZE + METADATA_SIZE    # bytes
ACK_PKT_SIZE                =   4
MAX_UNACKED_PKTS            =   20
UNACKED_PKTS_TIMEOUT        =   1
UNACKED_PKTS_MAX_RESEND_CNT =   10 
MESSAGE_CORRUPTION_RATE     =   0.05    # Probability of corrupting a message
BYTE_CORRUPTION_RATE        =   0.01    # Probability of corrupting a byte within a message

ABSOLUTE_TIME_CMD = 0
RELATIVE_TIME_CMD = 1

STATES = {
    'IDLE'                  :   0x00,
    'EXECUTING_CMDS'        :   0x01,
    'WAITING_FOR_DATA'      :   0x02,
    'DUMMY_SEND'            :   0x03,
    'WAITING_DOWNLINK'      :   0x04,
    'EXIT'                  :   0xFF,
}

CURRENT_STATE = STATES['IDLE']

NODES = {
    'MPU':0xaa,
    'MCU':0xbb,
    'FPGA':0xcc,
    'GPU':0xdd,
    'OTV':0xee,
    'GDS':0xff, 
    'NONE':0x00,
}

TARGET_NODE  = NODES['MPU']

PKT_TYPE = {
    'FW_PACKET_COMMAND'         : 0x00, 
    'FW_PACKET_TELEM'           : 0x01,
    'FW_PACKET_LOG'             : 0x02,
    'FW_PACKET_FILE'            : 0x03,
    'FW_PACKET_PACKETIZED_TLM'  : 0x04,
    'FW_PACKET_DP'              : 0x05,
    'FW_PACKET_IDLE'            : 0x06,
    'FW_PACKET_ACK'             : 0xAC,
    'FW_PACKET_RET_OK'          : 0xAD,
    'FW_PACKET_RET_ERROR'       : 0xAE,
    'FW_PACKET_UNKNOWN'         : 0xFF,
}

FILE_PKT_TYPE = {
    'START_PKT'                 : 0x00,
    'DATA_PKT'                  : 0x01,
    'END_PKT'                   : 0x02,
    'CANCEL_PKT'                : 0x03,
}

EXPECTING_FILE_PKT = FILE_PKT_TYPE['START_PKT']

INCOMING_FILE_MAX_SEQID = 0
INCOMING_FILE_PKT_CNT = 0
INCOMING_FILE_PKT_SEQID_LIST = []


OTV_CMD_OPCODES = {
    'SEND_FILE'             :   0x5010,
}

""" 
List to keep track of the packets we sent and have not been ack yet.
"""
unacked_pkts = []
packetID = 0


"""
Send queue list, keeping track of already framed packets to send to the 
MCU. The target node is specified in the framing. 
"""
send_queue = []



########################################
#           Misc
########################################
def crc32_noxor(data: bytes, crc_value = 0xFFFFFFFF) -> int:
    crc32_table = [0, 1996959894, 3993919788, 2567524794, 124634137, 1886057615, 3915621685, 2657392035, 249268274, 2044508324, 3772115230, 2547177864, 162941995, 2125561021, 3887607047, 2428444049, 498536548, 1789927666, 4089016648, 2227061214, 450548861, 1843258603, 4107580753, 2211677639, 325883990, 1684777152, 4251122042, 2321926636, 335633487, 1661365465, 4195302755, 2366115317, 997073096, 1281953886, 3579855332, 2724688242, 1006888145, 1258607687, 3524101629, 2768942443, 901097722, 1119000684, 3686517206, 2898065728, 853044451, 1172266101, 3705015759, 2882616665, 651767980, 1373503546, 3369554304, 3218104598, 565507253, 1454621731, 3485111705, 3099436303, 671266974, 1594198024, 3322730930, 2970347812, 795835527, 1483230225, 3244367275, 3060149565, 1994146192, 31158534, 2563907772, 4023717930, 1907459465, 112637215, 2680153253, 3904427059, 2013776290, 251722036, 2517215374, 3775830040, 2137656763, 141376813, 2439277719, 3865271297, 1802195444, 476864866, 2238001368, 4066508878, 1812370925, 453092731, 2181625025, 4111451223, 1706088902, 314042704, 2344532202, 4240017532, 1658658271, 366619977, 2362670323, 4224994405, 1303535960, 984961486, 2747007092, 3569037538, 1256170817, 1037604311, 2765210733, 3554079995, 1131014506, 879679996, 2909243462, 3663771856, 1141124467, 855842277, 2852801631, 3708648649, 1342533948, 654459306, 3188396048, 3373015174, 1466479909, 544179635, 3110523913, 3462522015, 1591671054, 702138776, 2966460450, 3352799412, 1504918807, 783551873, 3082640443, 3233442989, 3988292384, 2596254646, 62317068, 1957810842, 3939845945, 2647816111, 81470997, 1943803523, 3814918930, 2489596804, 225274430, 2053790376, 3826175755, 2466906013, 167816743, 2097651377, 4027552580, 2265490386, 503444072, 1762050814, 4150417245, 2154129355, 426522225, 1852507879, 4275313526, 2312317920, 282753626, 1742555852, 4189708143, 2394877945, 397917763, 1622183637, 3604390888, 2714866558, 953729732, 1340076626, 3518719985, 2797360999, 1068828381, 1219638859, 3624741850, 2936675148, 906185462, 1090812512, 3747672003, 2825379669, 829329135, 1181335161, 3412177804, 3160834842, 628085408, 1382605366, 3423369109, 3138078467, 570562233, 1426400815, 3317316542, 2998733608, 733239954, 1555261956, 3268935591, 3050360625, 752459403, 1541320221, 2607071920, 3965973030, 1969922972, 40735498, 2617837225, 3943577151, 1913087877, 83908371, 2512341634, 3803740692, 2075208622, 213261112, 2463272603, 3855990285, 2094854071, 198958881, 2262029012, 4057260610, 1759359992, 534414190, 2176718541, 4139329115, 1873836001, 414664567, 2282248934, 4279200368, 1711684554, 285281116, 2405801727, 4167216745, 1634467795, 376229701, 2685067896, 3608007406, 1308918612, 956543938, 2808555105, 3495958263, 1231636301, 1047427035, 2932959818, 3654703836, 1088359270, 936918000, 2847714899, 3736837829, 1202900863, 817233897, 3183342108, 3401237130, 1404277552, 615818150, 3134207493, 3453421203, 1423857449, 601450431, 3009837614, 3294710456, 1567103746, 711928724, 3020668471, 3272380065, 1510334235, 755167117]

    for byte in data:
        crc_value = (crc_value >> 8) ^ crc32_table[(crc_value ^ byte) & 0xFF]
    return crc_value

def log(*args, sep=' ', end='\n'):
    print(*args, sep=sep, end=end)
    

########################################
#           Commands Management
########################################

def decode_data(pkt):
    global unacked_pkts, file_name, CURRENT_STATE, EXPECTING_FILE_PKT, INCOMING_FILE_MAX_SEQID, INCOMING_FILE_PKT_CNT, INCOMING_FILE_PKT_SEQID_LIST

    source      = pkt[4]
    dest        = pkt[5]
    size        = int.from_bytes(pkt[6:8], "big")
    id          = pkt[8]
    pkt_type    = int.from_bytes(pkt[9:13], "big")
    pkt_data    = pkt[13:-4]
    checksum    = int.from_bytes(pkt[-4:], "big")
    
    cmd =  {'source':source, 'dest':dest, 'size':size, 'packetID':id,
            'pkt_type':pkt_type, 'data':pkt_data, 'checksum':checksum, 
            'bytestream':pkt}                
    
    calculated_checksum = crc32_noxor(pkt[0:-4])^0xFFFFFFFF
    
    if calculated_checksum == checksum:
        
        if cmd['dest'] == NODES['MCU']:
            log("     Forwarding Command to ", cmd['dest'])
            send_pkt(cmd['bytestream'])
            
        elif cmd['dest'] == NODES['OTV'] or cmd['dest'] == NODES['GDS'] or cmd['dest'] == NODES['MPU']:
            
            if cmd['pkt_type'] == PKT_TYPE['FW_PACKET_COMMAND']:
                log("     Executing Command")
                send_ack(id, source)
                execute_cmd(cmd['data'])
            
            elif cmd['pkt_type'] == PKT_TYPE['FW_PACKET_RET_OK']:
                log("       CMD RET_OK")
                send_ack(id, source)
                if CURRENT_STATE == STATES['WAITING_DOWNLINK']:
                    #CURRENT_STATE = STATES['EXIT']
                    CURRENT_STATE = STATES['IDLE']
                
            elif cmd['pkt_type'] == PKT_TYPE['FW_PACKET_RET_ERROR']:
                log("       CMD RET_ERROR")
                send_ack(id, source)
                if CURRENT_STATE == STATES['WAITING_DOWNLINK']:
                    CURRENT_STATE = STATES['EXIT']
                    #CURRENT_STATE = STATES['IDLE']

            elif cmd['pkt_type'] == PKT_TYPE['FW_PACKET_FILE']:
                
                seqID = int.from_bytes(cmd['data'][1:5], "big")
                
                if cmd['data'][0] == FILE_PKT_TYPE['START_PKT']:
                    if EXPECTING_FILE_PKT == FILE_PKT_TYPE['START_PKT']:
                        EXPECTING_FILE_PKT = FILE_PKT_TYPE['DATA_PKT']
                        # decode filename from packet
                        print("                 CMD 5:9 ", cmd['data'][5:9])
                        file_size = int.from_bytes(cmd['data'][5:9], "big")
                        src_file_name_size = cmd['data'][9]
                        src_file_name = cmd['data'][10:10+src_file_name_size]
                        
                        dst_file_name_size = cmd['data'][10+src_file_name_size]
                        dst_file_name = cmd['data'][11+src_file_name_size:11+src_file_name_size+dst_file_name_size]
                        file_name = str(dst_file_name, 'UTF-8')
                        
                        INCOMING_FILE_MAX_SEQID = file_size // FILE_PKT_CHUNK_SIZE + 2
                        INCOMING_FILE_PKT_SEQID_LIST = list(range(1, INCOMING_FILE_MAX_SEQID + 1))
                        log("     Received File Start Pkt seqID ", seqID, dst_file_name, "size", file_size)
                        send_ack(id, source)    
                        
                        # Need to create an empty file with the size of the expected one, so that
                        # we can seek and write the data packets to the correct offset if they come out of order
                        with open(file_name, 'wb') as f:
                            f.write(b'\0' * file_size)
                    
                    else:
                        log ("      Not expecting FILE START PKT ", seqID)   
                    
                    # TODO check this
                    # the issue is that when writing the second data packet, the offset wont be 0, but the file
                    # is only as big as the first data packet
                    
                elif cmd['data'][0] == FILE_PKT_TYPE['DATA_PKT']:
                    if EXPECTING_FILE_PKT == FILE_PKT_TYPE['DATA_PKT']:
                    
                        file_offset = int.from_bytes(cmd['data'][5:9], "big")
                        file_data_size = int.from_bytes(cmd['data'][9:11], "big")
                        file_data = cmd['data'][11:12+file_data_size]
                        
                        with open(file_name, 'r+b') as file:
                            file.seek(file_offset)
                            file.write(file_data)
                        
                        log("     Received File Data Pkt seqID ", seqID, "offset at ", file_offset, "pkt size", file_data_size)
                        send_ack(id, source)
                        
                        # check if the next seqID is supposed to be the endpacket
                        # TODO actually we need to count the amount of seqID we receive, because
                        # we can get packets out of order (i.e. the last data packet can arrive before the 
                        # other ones before it)
                        try:
                            if seqID in INCOMING_FILE_PKT_SEQID_LIST:
                                INCOMING_FILE_PKT_SEQID_LIST.remove(seqID)
                                INCOMING_FILE_PKT_CNT += 1
                        except ValueError:
                            print(f"Data Pkt seqID {seqID} not found in INCOMING_FILE_PKT_SEQID_LIST")

                        # check if the SEQID list tracker is empty, meaninig we received all the expected seqIDs
                        if len(INCOMING_FILE_PKT_SEQID_LIST) == 1 and INCOMING_FILE_PKT_SEQID_LIST[0] == INCOMING_FILE_MAX_SEQID:
                            print(f"        All expected Data Pkts received. Waiting for End Pkt...")
                            EXPECTING_FILE_PKT = FILE_PKT_TYPE['END_PKT']
                
                    else:
                        log ("          Not expecting FILE DATA PKT", seqID)   
                    
                elif cmd['data'][0] == FILE_PKT_TYPE['END_PKT']:
                    
                    if EXPECTING_FILE_PKT == FILE_PKT_TYPE['END_PKT']:
                        if seqID == INCOMING_FILE_MAX_SEQID and seqID == INCOMING_FILE_PKT_SEQID_LIST[0]:
                            print("Received File ", file_name)
                            INCOMING_FILE_PKT_CNT = 0
                            INCOMING_FILE_MAX_SEQID = 0
                            EXPECTING_FILE_PKT = FILE_PKT_TYPE['START_PKT']
                            INCOMING_FILE_PKT_SEQID_LIST = []
                            log("     Received File End Pkt seqID ", seqID)
                            send_ack(id, source)
                        else:
                            print(f"    Received File End Pkt with incorrect seqID ", seqID)
                    else:
                        log ("          Not expecting FILE END PKT", seqID)   
                                    
            elif cmd['pkt_type'] == PKT_TYPE['FW_PACKET_ACK']:
                log('     Received ACK for packetID ', cmd['packetID'])
                unacked_pkts = [p for p in unacked_pkts if p['packetID'] != cmd['packetID']]

        else:
            log('    Destination not found ', cmd['dest']) 
            
    else:
        log('       CHECKSUM Failed')
            
"""
    Execute cmd from an already decoded CmdPacket
    therefore, do not send the Packet Type with it
"""
def execute_cmd(cmd):    
    opcode = int.from_bytes(cmd['data'][0:4], "big")
    
    if opcode == OTV_CMD_OPCODES['SEND_FILE']:
        filename_size = int.from_bytes(cmd['data'][4:6], "big")
        filename = str(cmd['data'][6:6+filename_size], 'UTF-8')
        return send_file(filename)
        
    elif opcode == 0x00000500:
        log('     Executing NO-OP')
    
    else :
        log('     Forwarding CMD to ', TARGET_NODE)
        data = START_WORD
        data += struct.pack(">BBH", NODES['OTV'], TARGET_NODE, len(cmd['data']) + 4)
        data += struct.pack(">B", get_packetID_and_increment())
        data += struct.pack(">I", PKT_TYPE['FW_PACKET_COMMAND'])
        data += cmd['data']
        data += struct.pack(">I", crc32_noxor(data)^0xFFFFFFFF)
        send_pkt(data)
        
    return True
        


##################################################################
#                   File transfer function and helpers
##################################################################

def min_val(a, b):
    return a if a < b else b

def add_byte_at_offset(hash_val, byte, offset):
    if offset > 4:
        raise Exception("Default_Handler triggered")
    addend = byte << (8 * (3 - offset))
    hash_val += addend
    hash_val &= 0xFFFFFFFF  # Ensure hash_val remains within 4 bytes
    return hash_val

def add_word_aligned(hash_val, word):
    for i in range(4):
        hash_val = add_byte_at_offset(hash_val, word[i], i)
    return hash_val

def add_word_unaligned(hash_val, word, position, length):
    if length > 4:
        raise Exception("Default_Handler triggered")
    offset = position % 4
    for i in range(length):
        hash_val = add_byte_at_offset(hash_val, word[i], offset)
        offset += 1
        if offset == 4:
            offset = 0
    return hash_val

def update_cfdp(hash_val, data, offset, length):
    index = 0
    offset_mod_4 = offset % 4

    if offset_mod_4 != 0:
        word_len = min_val(length, 4 - offset_mod_4)
        hash_val = add_word_unaligned(hash_val, data[index:], offset + index, word_len)
        index += word_len

    while index + 4 <= length:
        hash_val = add_word_aligned(hash_val, data[index:index+4])
        index += 4

    if index < length:
        word_length = length - index
        hash_val = add_word_unaligned(hash_val, data[index:], offset + index, word_length)

    return hash_val

def get_file_size_and_hash(f, file_path):
    log('     Getting file size and hash...')
    size = 0
    hash = 0
    try:
        while True:
            chunk = f.read(2048)  
            if not chunk:
                break
            hash = update_cfdp(hash, chunk, size, len(chunk))
            size += len(chunk)
        log('     Resetting file pointer')
        log('     File Size', size)
        f.seek(0)
    except FileNotFoundError:
        log("File not found: ", file_path)
        return -1
    except IOError:
        log("Could not read file: ", file_path)
        return -1
    return size, hash


    
def send_file(filename):
    global file_seq_id, file_max_id, file_hash, file_offset, unacked_pkts
    
    if len(unacked_pkts) < MAX_UNACKED_PKTS:
        if file_seq_id == 0:
            with open(filename, 'rb') as f:

                # read the file data to get it's total size
                file_size, file_hash = get_file_size_and_hash(f, filename)
                
                # first we send the start    packet
                log('         Sending START PKT', filename, file_seq_id, "max SeqID ", file_max_id)
                start_data = struct.pack(">IBIIB", PKT_TYPE['FW_PACKET_FILE'], FILE_PKT_TYPE['START_PKT'], file_seq_id, file_size, len(filename))
                start_data += bytes(filename, 'ascii')
                start_data += struct.pack(">B", len(filename))
                start_data += bytes(filename, 'ascii')
                
                start_pkt = START_WORD + struct.pack(">BBHB", NODES['OTV'], NODES['MPU'], len(start_data), get_packetID_and_increment()) +  start_data 
                start_pkt += struct.pack(">I", crc32_noxor(start_pkt) ^0xFFFFFFFF)
                
                send_pkt(start_pkt)
                file_seq_id += 1
                
                # takes into account the end packet( start packet is 0 anyways)
                file_max_id = file_size // FILE_PKT_CHUNK_SIZE + 2
                
        elif file_seq_id > 0 and file_seq_id < file_max_id:
            with open(filename, 'rb') as f:
                f.seek(file_offset)
                data = f.read(FILE_PKT_CHUNK_SIZE)
                log('         Sending DATA PKT ', file_seq_id, 'len of data read', len(data), ' max file pkt id seq ', file_max_id)
                if data:
                    data_data = struct.pack(">IBIIH", PKT_TYPE['FW_PACKET_FILE'], FILE_PKT_TYPE['DATA_PKT'], file_seq_id, file_offset, len(data)) + data
                    
                    file_offset += len(data)
                    
                    data_pkt = START_WORD + struct.pack(">BBHB", NODES['OTV'], NODES['MPU'], len(data_data), get_packetID_and_increment()) + data_data
                    data_pkt += struct.pack(">I", crc32_noxor(data_pkt)^0xFFFFFFFF)
                    send_pkt(data_pkt)
                    file_seq_id += 1
                else:
                    # TODO probably an error, as we should already be sending the END packet
                    log("         ERROR Reading File")
                    
        
        elif file_seq_id == file_max_id and len(unacked_pkts) == 0 and len(send_queue) == 0:
            
            log('         Sending END PKT ', file_seq_id, "hash", file_hash, type(file_hash))
            end_data = struct.pack(">IBII", PKT_TYPE['FW_PACKET_FILE'],  FILE_PKT_TYPE['END_PKT'], file_seq_id, file_hash)
            end_pkt = START_WORD + struct.pack(">BBHB", NODES['OTV'], NODES['MPU'], len(end_data), get_packetID_and_increment()) + end_data
            end_pkt +=  struct.pack(">I", crc32_noxor(end_pkt)^0xFFFFFFFF)           
            send_pkt(end_pkt, True)
            # reset params
            file_offset = 0
            file_hash  = 0
            file_max_id = 0
            file_seq_id = 0
            
            return True
        
    # The only case that returns true, i.e. finished sending file, is when we send the end_pkt
    return False
        
        


########################################
#           Ack Management
########################################

"""
Adds pkt to send_queue and also to the unaked_pkts
"""
def send_pkt(pkt, end_pkt=False):
    global send_queue, file_max_id, file_seq_id
    unacked_pkts.append({
                    'packetID'  : pkt[8],
                    'time_sent' : time.time(),
                    'data'      : pkt,
                    'end_pkt'   : end_pkt,
                    'resend_cnt': 0
                })
    
    # Rational: we dont' want to send the end_pkt before all the file data pkts were sent
    if (end_pkt == False) or (end_pkt == True and file_seq_id == file_max_id) :
        send_queue.append(pkt)
    

def send_ack(id, source):
    global send_queue
    
    data = START_WORD
    data += struct.pack(">BBH", NODES['OTV'], source, ACK_PKT_SIZE)
    data += struct.pack(">B", id)
    data += struct.pack(">I", PKT_TYPE['FW_PACKET_ACK'])
    data += struct.pack(">I", crc32_noxor(data)^0xFFFFFFFF)
    send_queue.append(data)
    
    log("Sending ACK ", id)    

def resend_unacked():
    global unacked_pkts, send_queue, UNACKED_PKTS_TIMEOUT, file_seq_id, file_max_id, UNACKED_PKTS_MAX_RESEND_CNT
    
    current_time = time.time()
    i = 0
    while i < len(unacked_pkts):
        pkt = unacked_pkts[i]
        if current_time >= pkt['time_sent'] + UNACKED_PKTS_TIMEOUT:
            if (not pkt['end_pkt']) or (pkt['end_pkt'] and file_seq_id == file_max_id):
                if pkt['resend_cnt'] >= UNACKED_PKTS_MAX_RESEND_CNT:
                    log('Dropping UNACKED PKT', pkt['packetID'])
                    del unacked_pkts[i]
                    continue  # Skip incrementing i to avoid skipping the next element
                else:
                    log('Resending UNACKED PKT', pkt['packetID'])
                    send_queue.append(pkt['data'])
                    pkt['time_sent'] = current_time
                    pkt['resend_cnt'] += 1        
        i += 1  # Increment i only if no element was removed


def get_packetID_and_increment():
    global packetID, unacked_pkts
    packetID += 1
    if not unacked_pkts:
        return packetID

    while True:
        for unacked_pkt in unacked_pkts:
            if unacked_pkt['packetID'] == packetID:
                packetID += 1
        if packetID >= 0xFE:
            packetID = 0
        else:
            return packetID

#######################################
#       ReadWrite Interface
#######################################

def send(data):
    global conn, driver
    conn.sendall(data)

def read():
    global conn
    try:
        conn.settimeout(TCP_READ_TIMEOUT)
        data = conn.recv(48)
        return data
    except socket.timeout:
        return b''
        


def process_buffer(buffer):
    global MAX_PKT_SIZE
    processed_bytes = 0
    print(f"buffer data : {''.join(f'{x:02x}' for x in buffer)}")
    
    while processed_bytes < len(buffer):
        # Look for START_WORD
        start_index = buffer.find(START_WORD, processed_bytes)
        if start_index == -1:
            # No complete START_WORD found, but there might be a partial one at the end
            for i in range(1, len(START_WORD)):
                if buffer.endswith(START_WORD[:i]):
                    print("     Incomplete start word")
                    return buffer[-(i):]
            # No START_WORD found, discard processed bytes and exit
            return bytearray()
        
        # Check if we have enough bytes for a complete header
        if len(buffer) - start_index < HEADER_SIZE:
            # Incomplete header, keep the remaining buffer and exit
            print("     Incomplete header")
            return buffer[start_index:]
        
        # Extract header information
        source = buffer[start_index + 4]
        dest = buffer[start_index + 5]
        size = int.from_bytes(buffer[start_index + 6:start_index + 8], "big")
        packet_id = buffer[start_index + 8]
        
        full_packet_size = HEADER_SIZE + size + CHECKSUM_SIZE
        
        # Check if the packet size is too big
        if full_packet_size >= MAX_PKT_SIZE:
            print("     Packet Size too big, probably data size got corrupted")
            processed_bytes = start_index + len(START_WORD)  # Move past this START_WORD
            continue
        elif len(buffer) - start_index < full_packet_size:
            # Incomplete packet, keep the remaining buffer and exit
            print(f"     Incomplete packet, missing {full_packet_size - (len(buffer) - start_index)} bytes")
            return buffer[start_index:]
        
        # Extract packet and checksum
        packet = buffer[start_index:start_index + full_packet_size]
        print(f"    packet data : {''.join(f'{x:02x}' for x in packet)}")
        checksum_received = int.from_bytes(packet[-CHECKSUM_SIZE:], "big")
        data_to_check = packet[:-CHECKSUM_SIZE]
        
        # Calculate expected checksum
        calculated_checksum = crc32_noxor(data_to_check) ^ 0xFFFFFFFF
        
        if checksum_received != calculated_checksum:
            print(f"Checksum verification failed at index {start_index}, skipping this packet")
            processed_bytes = start_index + len(START_WORD)  # Move past this START_WORD
            continue
        
        # Process valid packet
        try:
            decode_data(packet)
        except Exception as e:
            print(f"Error processing packet at index {start_index}: {e}")
        
        processed_bytes = start_index + full_packet_size
    
    # All data processed
    return bytearray()


#######################################
#           Main
#######################################

# need these to be global 
file_seq_id = 0
file_max_id = 0
file_hash = None
file_name = ''
file_offset = 0
payload = None
conn, addr = (None, None)

        



def set_current_state(state):
    global CURRENT_STATE
    CURRENT_STATE = state
    
def get_current_state():
    global CURRENT_STATE
    return CURRENT_STATE
    

def fs_interface(cmd_file):
    global send_queue, conn, CURRENT_STATE
    
    TCP_IP = '0.0.0.0'
    TCP_PORT = 50054
    
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((TCP_IP, TCP_PORT))
    
    except socket.timeout:
        print("Timeout: failed to connect to FS. Have you ran ./run.sh ? ")
        return
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to connect to FS. Have you ran ./run.sh ? ")
        return

    
    with open(cmd_file, 'rb') as f:
        cmd_seq_data = f.read()
        
    log('Cmd seq len ', len(cmd_seq_data))

    file_size = int.from_bytes(cmd_seq_data[0:4], "big")
    nb_records = int.from_bytes(cmd_seq_data[4:8], "big")
    time_base = cmd_seq_data[8:10]
    context = cmd_seq_data[10]
    offset = 11 

    record_index = 0   
    buffer = bytearray()

    cmd_ok = True
    current_time = time.time()
    start_time = time.time()

    
    try:
        while CURRENT_STATE != STATES['EXIT']:
            data = read()
            if data:
                buffer.extend(data)
                buffer = process_buffer(buffer)
                
            if len(send_queue) > 0:
                for p in send_queue:
                    send(p)
                send_queue = []
            else:
                resend_unacked()

            if CURRENT_STATE == STATES['IDLE']:
                pass
                
            elif CURRENT_STATE == STATES['EXECUTING_CMDS']:
                
                if cmd_ok:
                    current_time = time.time()
                    cmd_ok = False
                
                if record_index < nb_records:
                    descriptor = cmd_seq_data[offset]
                    record_time = cmd_seq_data[offset+1:offset+9]
                    record_seconds = int.from_bytes(record_time[:4], "big")
                    record_milli = int.from_bytes(record_time[4:], "big")
                    record_exec_time_seconds = record_seconds + record_milli / 1000
                    exec_time_relative = current_time + record_exec_time_seconds
                    
                    if (descriptor == 0 and time.time() > record_exec_time_seconds) or (descriptor == 1 and time.time() > exec_time_relative):
                        record_size = int.from_bytes(cmd_seq_data[offset+9:offset+13], "big")
                        buffer_cmd = cmd_seq_data[offset+17:offset+13+record_size]

                        # do not go to the next cmd unless there are no more unacked pkts
                        # so as to not overload the system if it is still processing stuff before
                        #if len(unacked_pkts) == 0:
                        
                        cmd = {'data': buffer_cmd}
                        cmd_ok = execute_cmd(cmd)

                        if cmd_ok:
                            offset += record_size + 13
                            record_index += 1                
                
                else:
                    CURRENT_STATE = STATES['WAITING_DOWNLINK']
                    record_index = 0
                    offset = 11 
                    
            elif CURRENT_STATE == STATES['EXIT']:
                log('Exiting FS Interface...')
                break
            
            #resend_unacked()
    except KeyboardInterrupt:
        if conn:
            conn.close()
                    
    
            
if __name__ == "__main__":
    fs_interface('cmds-clients.bin')
    
    