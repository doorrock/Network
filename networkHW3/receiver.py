import sys
import socket
import time
import select
"Use this method to write Packet log"
def writePkt(logFile, procTime, pktNum, event):
    logFile.write('{:1.3f} pkt: {} | {}'.format(procTime, pktNum, event))

"Use this method to write ACK log"
def writeAck(logFile, procTime, ackNum, event):
    logFile.write('{:1.3f} ACK: {} | {}'.format(procTime, ackNum, event))

"Use this method to write final throughput log"
def writeEnd(logFile, throughput):
    logFile.write('File transfer is finished.')
    logFile.write('Throughput : {:.2f} pkts/sec'.format(throughput))


def fileReceiver():
    print('receiver program starts...')
    sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sckt.bind(('', 10080))

    data, sender = sckt.recvfrom(65565)
    sender = sender[0]
    num_packet = int.from_bytes(data[:4], byteorder='big')
    windowSize = int.from_bytes(data[4:8], byteorder='big')
    file_name = data[8:].decode()
    receiver_log = open(file_name + '_receiving_log.txt', 'a')
    f = open(file_name, 'wb')
    ack = False
    wanted = 0
    temp = []
    timeout = 1
    start_time = time.time()
    while wanted < num_packet:
        cnt = 0
        while cnt < windowSize:
            data = sckt.recv(65565)
            cnt = cnt + 1
            flag = int.from_bytes(data[:1], byteorder='big')
            if flag == 1:
                cnt = 1
            number = int.from_bytes(data[1:5], byteorder='big')
            writePkt(receiver_log, time.time() - start_time, number, "receive\n")

            if number == wanted:
                f.write(data[5:])
                wanted = wanted + 1

            if wanted >= num_packet:
                break
        sckt.sendto(wanted.to_bytes(4, byteorder='big'), (sender, 10080))
        writeAck(receiver_log, time.time() - start_time, wanted, "send\n")
    writeEnd(receiver_log, num_packet/(time.time()-start_time))

    # Write your Code here

    #########################



if __name__=='__main__':
    fileReceiver()
