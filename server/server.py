import socket
import sys
import cv2
import base64
from serverworker import Serverworker
from VideoStream import VideoStream
import threading


class Video(threading.Thread):
    def __init__(self, video, rtpserver, serverworker, address):
        super(Video, self).__init__()
        self.flag = threading.Event()
        self.flag.clear()
        self.running = threading.Event()
        self.running.set()
        self.video = video
        self.rtpserver = rtpserver
        self.serverworker = serverworker
        self.address = address

    def run(self):
        while self.running.isSet():
            self.flag.wait()
            frame = self.video.nextFrame()
            cv2.waitKey(30)
            if frame:
                # 影片還沒播完
                # encode frame
                bytedata = base64.encodebytes(frame)
                rtp = self.serverworker.createRTP(self.video.frameNbr(), bytedata)
                print(len(rtp.getPayload()))
                self.rtpserver.sendto(rtp.getPacket(), self.address)
            else:
                # 影片播完了
                self.rtpserver.sendto(b"", self.address)
                self.flag.clear()
                break

    def pause(self):
        self.flag.clear()
    def resume(self):
        self.flag.set()
    def stop(self):
        self.flag.set() 
        self.running.clear() 

# Specify the IP addr and port number
# (use "127.0.0.1" for localhost on local machine)
# Create a socket and bind the socket to the addr
HOST, PORT = sys.argv[1], int(sys.argv[2])

rtspserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rtspserver.bind((HOST, PORT))
rtspserver.listen(1)
rtpserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rtpserver.bind((HOST, PORT + 1))

connect_socket, client_addr = rtspserver.accept()
print(client_addr)
serverworker = Serverworker()
while(True):
    data = str(connect_socket.recv(1024), encoding='utf-8')
    print(data)
    # Get the request type
    request = data.split('\n')
    line1 = request[0].split(' ')
    requestType = line1[1]

    # Get the media file name
    filename = line1[2]

    # Get the RTSP sequence number
    seqnum = request[1].split(' ')[1]
    if (requestType == "SETUP"):
        # 收到SETUP就建立video
        videostream = VideoStream(filename)
        client, address = rtpserver.recvfrom(1024)
        video = Video(videostream, rtpserver, serverworker, address)
        threading.Thread(target=video.run).start()
    elif (requestType == "PLAY"):
        video.resume()
    elif(requestType == "PAUSE"):
        video.pause()
    elif(requestType == "TEARDOWN"):
        video.stop()
        break
connect_socket.close()