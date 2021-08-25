import sys
import socket
import select
import os
import time

"Use this method to write Packet log"
def writePkt(logFile, procTime, pktNum, event):
    logFile.write('{:1.3f} pkt: {} | {}'.format(procTime, pktNum, event))

"Use this method to write ACK log"
def writeAck(logFile, procTime, ackNum, event):
    logFile.write('{:1.3f} ACK: {} | {}'.format(procTime, ackNum, event))

"Use this method to write final throughput log"
def writeEnd(logFile, throughput, avgRTT):
    logFile.write('File transfer is finished.')
    logFile.write('Throughput : {:.2f} pkts/sec'.format(throughput))
    logFile.write('Average RTT : {:.1f} ms'.format(avgRTT))


def fileSender():
    print('sender program starts...')
    srcFile = open(srcFilename, 'rb')
    sender_log = open(srcFilename + '_sending_log.txt', 'a')
    packet_list = []
    data = srcFile.read(1400)
    while data:
        packet_list.append(data)
        data = srcFile.read(1400)
    num_packets = len(packet_list)

    sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sckt.bind(('', 10080))

    en_dstFilenamedst = dstFilename.encode()
    sckt.sendto((num_packets.to_bytes(4, byteorder='big') + windowSize.to_bytes(4, byteorder='big') + en_dstFilenamedst), (recvAddr, 10080))

    base = 0
    send_num = 0
    rtt = 0
    timeout = 1
    start_time = time.time()
    flag = 0
    while base < num_packets:
        send_num = base
        while send_num < base + windowSize:
            sckt.sendto((flag.to_bytes(1, byteorder='big') + send_num.to_bytes(4, byteorder='big') + packet_list[send_num]), (recvAddr, 10080))
            flag = 0
            go_time = time.time() - start_time
            writePkt(sender_log, go_time, send_num, "send\n")
            send_num = send_num + 1
            if send_num >= num_packets:
                break

        ready = select.select([sckt], [], [], timeout)
        if ready[0]:
            ack = sckt.recv(65565)
        else:
            flag = 1
            writeAck(sender_log, go_time, base, "timeout\n")
            continue

        ack = int.from_bytes(ack, byteorder='big')
        base = ack
        arr_time = time.time() - start_time
        writeAck(sender_log, arr_time, base, "received\n")
        rtt += arr_time - go_time
    rtt = rtt * 1000 /(num_packets/windowSize)
    writeEnd(sender_log,  num_packets/(time.time()-start_time), rtt)

if __name__=='__main__':
    recvAddr = sys.argv[1]  #receiver IP address
    windowSize = int(sys.argv[2])   #window size
    srcFilename = sys.argv[3]   #source file name
    dstFilename = sys.argv[4]   #result file name

    fileSender()
