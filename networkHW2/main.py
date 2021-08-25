import socket
import datetime
from threading import Thread

def head(type):
    h = ''
    if type == 200:
        h = 'HTTP/1.1 200 OK\n'
    elif type == 404:
        h = 'HTTP/1.1 404 Not Found\n'
    elif type == 403:
        h = 'HTTP/1.1 403 Forbidden\n'

    return h

def start_server():
    host = ''
    port = 10080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)

    return server


def run_server(server):
    while 1:
        user, info = server.accept()
        work = Thread(target=connect, args=(user, info))
        work.start()

def connect(user, info):
    a = 0
    data = user.recv(65565)
    data_decode = data.decode('utf-8')
    data_info = data_decode.split(' ')

    method = data_info[0]
    if method == "GET" or method == "POST":
        if method == "POST":
            d = data_decode.split('\n')[-1].split('&')
            cookie_id = d[0][3:]
            cookie = "ID="+cookie_id+";"
            a = 1
            name = data_info[1][1:]
        request = data_info[1]

        if request == '/':
            name = "index.html"
        else:
            if "Cookie" in data_decode:
                name = request[1:]
                cookie_on = 1
            else:
                cookie_on = 0

        try:
            f = open(name, 'rb')
            response_content = f.read()
            f.close()
            response_head = head(200)
            print("delivering [",name,"]")
            if a == 1:
                current = datetime.datetime.now()
                t = current + datetime.timedelta(seconds=30)
                response_head += 'Set-Cookie: ' + cookie + ';'
                response_head += 'Max-Age=30;\n'
                response_head += 'Set-Cookie: ' + 'time=' + str(t.second) + ';'
                response_head += 'Max-Age=30;\n\n'

            else:
                response_head += '\n'

        except:
            if cookie_on:
                response_content = b"<html><body>404 Error: File Not Found</body></html>"
                response_head = head(404) + '\n'
            else:
                response_content = b"<html><body>403 Error: Forbidden</body></html>"
                response_head = head(403) + '\n'


        response = response_head.encode() + response_content

        user.send(response)

        user.close()

server = start_server()
run_server(server)
