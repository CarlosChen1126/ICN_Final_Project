import socket
import sys
import cv2
import base64
from PIL import Image
from serverworker import Serverworker
from VideoStream import VideoStream
import time
import threading


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


def playVideo(video, rtpserver):
    while(True):
        frame = video.nextFrame()
        cv2.waitKey(30)
        if frame:
            # 影片還沒播完
            # encode frame
            bytedata = base64.encodebytes(frame)
            rtp = serverworker.createRTP(bytedata)
            print(len(rtp.getPayload()))
            rtpserver.sendto(rtp.getPacket(), address)
        else:
            # 影片播完了
            rtpserver.sendto(b"", address)
            break


# Specify the IP addr and port number
# (use "127.0.0.1" for localhost on local machine)
# Create a socket and bind the socket to the addr
# TODO start
HOST, PORT = sys.argv[1], int(sys.argv[2])
# # TODO end
rtspserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rtspserver.bind((HOST, PORT))
rtspserver.listen(1)

connect_socket, client_addr = rtspserver.accept()
print(client_addr)
video = VideoStream("./image/movie.Mjpeg")
serverworker = Serverworker()
while(True):
    recevent = connect_socket.recv(1024)
    recevent = str(recevent, encoding='utf-8')
    print(recevent)
    if (recevent == "SETUP"):
        # 收到SETUP就建立rtpserver
        rtpserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rtpserver.bind((HOST, PORT + 1))
        client, address = rtpserver.recvfrom(1024)
    elif (recevent == "PLAY"):
        threading.Thread(target=playVideo(video, rtpserver)).start()
    elif(recevent == "PAUSE"):
        threading.Thread(target=playVideo(video, rtpserver)).sleep(10000)

        # while(True):
        #     frame = video.nextFrame()
        #     cv2.waitKey(30)
        #     if frame :
        #         #影片還沒播完
        #         #encode frame
        #         bytedata = base64.encodebytes(frame)
        #         rtp = serverworker.createRTP(bytedata)
        #         print(len(rtp.getPayload()))
        #         rtpserver.sendto(rtp.getPacket(), address)
        #     else:
        #         #影片播完了
        #         rtpserver.sendto(b"", address)
        #         break
connect_socket.close()
