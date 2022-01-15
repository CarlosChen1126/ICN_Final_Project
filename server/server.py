import socket
import sys
import cv2
import base64
from PIL import Image
from RtpPacket import RtpPacket
from serverworker import Serverworker


def image_encode(image):
    with open(image, "rb") as imageFile:
        str = base64.encodebytes(imageFile.read())
        print(str)
    return str

    #     img = base64.decodebytes(str)
    #     writeFile.write(img)


def image_decode(image, str):
    with open(image, "wb") as writeFile:
        img = base64.decodebytes(str)
        writeFile.write(img)


# Specify the IP addr and port number
# (use "127.0.0.1" for localhost on local machine)
# Create a socket and bind the socket to the addr
# TODO start
HOST, PORT = sys.argv[1], int(sys.argv[2])
# # TODO end
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))
# server.listen(1)
while(True):
    client, address = server.recvfrom(1024)
    imgg = Image.open("test.jpg")
    imgg.save("test_c.jpg", quality=1, subsampling=0)
    bytedata = image_encode("test_c.jpg")
    serverworker = Serverworker()
    rtp = serverworker.createRTP(bytedata)
    print(len(rtp.getPayload()))
    server.sendto(rtp.getPacket(), address)
