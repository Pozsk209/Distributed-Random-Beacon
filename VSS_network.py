import socket
import threading
import VSS_net
from tkinter import *


# 1.实现接收消息
def recvDate():
    while True:
        recvInfo = udpSocket.recvfrom(1024)
        print("\r\n>>%s:%s" % (str(recvInfo[1]), recvInfo[0].decode("UTF-8")))
        # print("<<")
        recvstr = recvInfo[0].decode("UTF-8")
        if recvstr[0: 8] == "getvalue":
            print("sendvalue")
            udpSocket.sendto(("sendvalue:" + VSS_personal.sendvalue()).encode("UTF-8"), (destIp, destPort))
        if recvstr[0: 9] == "sendvalue":
            sendstr, a, b, c, d, e = recvstr.split(":")
            print(sendstr)
            print(a)
            print(b)
            print(c)
            print(d)
            print(e)

# 2.实现发送消息
def sendDate():
    while True:
        # 用按钮实现，这里是控制台所以直接用命令输入
        sendInfo = input("<<")
        udpSocket.sendto(sendInfo.encode("UTF-8"), (destIp, destPort))


udpSocket = None
destIp = ""
destPort = 0
destuid = 0


def main():
    # 改变全局变量时才加global
    global udpSocket
    global destIp
    global destPort
    global destuid

    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # user_id = input("请输入用户id:")
    # VSS_personal = VSS.VSS(5, 3, user_id, 4)
    # VSS_personal.generate()

    destIp = input("请输入目的ip:")
    destPort = int(input("请输入目的端口:"))
    destuid = int(input("请输入目的uid:"))
    localPort = int(input("请输入本程序的端口号:"))
    udpSocket.bind(("", localPort))  # 绑定端口号
    re = threading.Thread(target=recvDate)  # 线程1
    rh = threading.Thread(target=sendDate)  # 线程2

    re.start()
    rh.start()

    re.join()  # 等待至线程中止
    rh.join()


if __name__ == "__main__":
    user_id = input("请输入用户id:")
    VSS_personal = VSS.VSS(5, 3, user_id, 4)
    VSS_personal.generate()
    main()
