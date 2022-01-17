import socket
import sys
import base64
from RtpPacket import RtpPacket
from clientworker import Clientworker


def image_decode(image, str):
    with open(image, "wb") as writeFile:
        img = base64.decodebytes(str)
        writeFile.write(img)


def temp_write(str):
    with open("t.txt", "wb") as writeFile:
        img = base64.decodestring(str)
        writeFile.write(img)


HOST, PORT1, PORT2 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
print(HOST)
print(PORT1)
#HOST, PORT = "127.0.0.1", 8888
#HOST, PORT = "140.112.42.108", 7777
clientworker = Clientworker()
clientworker.connectToServer(HOST, PORT1, PORT2)
clientworker.run()
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect((HOST, PORT))
# a = b''
# while(True):
#     response = client.recv(1000000)
#     rtp = RtpPacket()
#     rtp.decode(response)
#     # print(rtp.getPayload())
#     #bytedata = response.getPayload()
#     print("len")
#     print(len(rtp.getPayload()))
#     b = rtp.getPayload()
#     a = a+b
#     image_decode("t.jpg", a)
#     # client.send(response.encode())
