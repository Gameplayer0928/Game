# coding=utf-8
'''
    create time : 上午12:37:37
    anthor : gq-gameplayer0928
'''

import socket
import threading

HOST = ''
PORT = 51423

# sok = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # tcp

sok = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

sok.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
sok.bind((HOST,PORT))


class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.message = None
        self.fromaddr = None
     
     
    def run(self):
        while 1:
            self.message,self.fromaddr = sok.recvfrom(2048)
     
    def get_result(self):
        return self.message


t1 = myThread()
t1.setDaemon(1)
t1.start()

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('1.1.1.1', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

