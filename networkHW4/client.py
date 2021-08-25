import sys
import socket
import time
import threading
serverIP = '10.0.0.3'
serverPort = 10080
clientPort = 10081

def keepMSG(socket, clientLIST):
    msg = "@alive " + clientID
    socket.sendto(msg.encode(), (serverIP, serverPort))
    while True:
        time.sleep(10)
        if clientID in clientLIST:
            socket.sendto(msg.encode(), (serverIP, serverPort))
        else:
            sys.exit()

def sendMSG(socket, clientLIST):
    while True:
        message = input("")
        splited_message = message.split(' ')
        check = splited_message[0]
        if check == "@show_list": # to server
            msg = check + " " + clientID
            socket.sendto(msg.encode(), (serverIP, serverPort))

        elif check == "@exit": # to server
            msg = check + " " + clientID
            socket.sendto(msg.encode(), (serverIP, serverPort))
            sys.exit()

        elif check == "@chat": # to user
            TO = splited_message[1]
            FROM = clientID
            if TO in clientLIST: # if not, do not send
                content = ' '.join(splited_message[2:])
                data = "1" + FROM + " " + content
                socket.sendto(data.encode(), clientLIST[TO])



def recvMSG(socket, clientLIST):
    while True:
        message, addr = socket.recvfrom(1024)
        message = message.decode()
        if message[0] == "0": # from server
            if message[1] == "0": # show_list
                print(message[2:])

            elif message[1] == "1": # information of registered clients
                message = message[2:]
                splited_message = message.split('\n')
                for i in splited_message:
                    if i == "":
                        continue
                    temp = i.split('\t')
                    ID = temp[0]
                    addr = eval(temp[1])
                    clientLIST[ID] = addr # make clients set

            elif message[1] == "2": # someone is registered
                splited_message = message[2:].split('\t')
                clientLIST[splited_message[0]] = eval(splited_message[1])

            elif message[1] == "3": # someone is deregistered
                del(clientLIST[message[2:]])

            elif message[1] == "4": # this user is exited or disappeared
                sys.exit()
        
        else: # from user
            splited_message = message[1:].split(' ')
            FROM = splited_message[0]
            content = ' '.join(splited_message[1:])
            print("From " + FROM + " [" + content + "]")


def client(serverIP, serverPort, clientID):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', clientPort))
    data = "@enter " + clientID
    s.sendto(data.encode(), (serverIP, serverPort))
    
    clientLIST = {}
    sending = threading.Thread(target=sendMSG, args=(s, clientLIST))
    recving = threading.Thread(target=recvMSG, args=(s, clientLIST))
    keeping = threading.Thread(target=keepMSG, args=(s, clientLIST))
    
    sending.start()
    recving.start()
    keeping.start()


"""
Don't touch the code below!
"""
if  __name__ == '__main__':
    clientID = input("")
    client(serverIP, serverPort, clientID)


