import sys
import socket
import threading
from time import sleep

serverPort = 10080

def timer(socket, clientTIME, clientLIST):
    while True:
        sleep(1)
        #print(clientTIME)
        for i in list(clientTIME):
            clientTIME[i] += 1
            if clientTIME[i] > 30:
                print(i + " is disappeared." + "\t" + str(clientLIST[i]))

                msg = "03" + i # someone is deregistered
                for c in clientLIST.values(): # send to all
                    socket.sendto(msg.encode(), c)

                msg = "04" # this user is disappeared
                socket.sendto(msg.encode(), clientLIST[i])

                del(clientTIME[i])
                del(clientLIST[i])


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', serverPort))
    clientLIST = {}
    clientTIME = {}

    t = threading.Thread(target=timer, args=(s, clientTIME, clientLIST))
    t.start()

    while True:
        data, addr = s.recvfrom(1024)
        data = data.decode()
        splited_data = data.split(' ')

        if splited_data[0] == "@alive": # make clientTIME set
            clientTIME[splited_data[1]] = 0

        elif splited_data[0] == "@show_list":
            msg = "00" # show_list
            for key in clientLIST:
                msg = msg + key + "\t" + str(clientLIST[key]) + "\n"
            s.sendto(msg.encode(), clientLIST[splited_data[1]])

        elif splited_data[0] == "@exit":
            print(splited_data[1] + " is deregistered." + "\t" + str(addr))
            
            msg = "03" + splited_data[1] # someone is deregistered
            for i in clientLIST.values(): # send to all
                s.sendto(msg.encode(), i)

            msg = "04" # this user is exited
            s.sendto(msg.encode(), addr)

            del(clientTIME[splited_data[1]])
            del(clientLIST[splited_data[1]])


        elif splited_data[0] == "@enter":
            clientID = splited_data[1]
            print(clientID + " is registered." + "\t" + str(addr))
            clientLIST[clientID] = addr

            msg = "01" # information of clientLIST
            for key in clientLIST:
                msg = msg + key + "\t" + str(clientLIST[key]) + "\n"
            s.sendto(msg.encode(), addr)
            
            msg = "02" + clientID + "\t" + str(addr) # someone is registered
            for i in clientLIST.values(): # send to all
                s.sendto(msg.encode(), i)
     
        else:
            continue

    pass


"""
Don't touch the code below
"""
if  __name__ == '__main__':
    server()


