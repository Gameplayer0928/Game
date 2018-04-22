#coding=utf-8
'''
    create time : 上午1:13:01
    anthor : gq-gameplayer0928
'''



import socket,sys
import tty, termios

NC_EXIT = 'q'

def outword():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

print("inport HOST ip: ",end='')
host = input()
print("input PORT : ",end='')
port = int(input())
print("connect ",end="")
print((host,port))
print("press '"+ NC_EXIT + "' to exit")

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect((host,port))

while 1:
    ipt = outword()
#     ipt = os.system("wait")
    if ipt != NC_EXIT:
        s.sendall((ipt).encode("utf-8"))
    else:
        s.sendall((NC_EXIT).encode("utf-8"))
        sys.exit()