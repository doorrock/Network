import time
from threading import Thread

f = open("log.txt", 'a')
now_time = float(time.time())


def copy(a, b):
    file1 = open(a, 'rb')
    file2 = open(b, 'wb')

    start_time = float(time.time()) - now_time
    f.write(str("%.2f" % start_time) + " Start copying " + str(a) + " to " + str(b) + "\n")
    f.flush()

    data = file1.read(10000)
    while data:
        file2.write(data)
        data = file1.read(10000)

    finish_time = float(time.time()) - now_time
    f.write(str("%.2f" % finish_time) + " " + str(b) + " is copied completely\n")
    f.flush()

    file1.close()
    file2.close()


while 1:
    file_name = input("Input the file name : ")
    if file_name == "exit":
        break
    new_name = input("Input the new name : ")
    print("\n")

    work = Thread(target=copy, args=(file_name, new_name))
    work.start()

f.close()
