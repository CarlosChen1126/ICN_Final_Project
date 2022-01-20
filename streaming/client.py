import socket
import sys
import time
import base64
from RtpPacket import RtpPacket
from clientworker import Clientworker

def temp_write(str):
    with open("t.txt", "wb") as writeFile:
        img = base64.decodestring(str)
        writeFile.write(img)


HOST, PORT = sys.argv[1], int(sys.argv[2])
#HOST, PORT = "127.0.0.1", 8888

clientworker = Clientworker()
clientworker.connectToServer(HOST, PORT)
clientworker.sendRtspRequest("SETUP")
time.sleep(0.5) #不要讓2次send合在一起
clientworker.sendRtspRequest("PLAY")
