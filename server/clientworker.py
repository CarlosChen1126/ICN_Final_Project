import base64
from RtpPacket import RtpPacket
import socket
import threading
import cv2
import os


class Clientworker:
    RTSP_VER = "RTSP/1.0"
    TRANSPORT = "RTP/UDP"

    def __init__(self):
        self.rtspSeq = 0  # rtsp request's sequence number
        self.state = "INIT"  # have four state : INIT SETUP PLAY PAUSE
        self.serveraddr = 0

    def connectToServer(self, address, port):
        # rtsp client using tcp
        self.rtspclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.rtspclient.connect((address, port))
            self.serveraddr = (address, port)
        except:
            print("Can not connect to server.")

    def sendRtspRequest(self, requestCode):
        # Send RTSP request to the server
        self.rtspSeq += 1
        if(requestCode == "SETUP"):
            self.state = "SETUP"
            # threading.Thread(target=self.recvRtspResponse).start()
            self.rtspclient.send(bytes(requestCode, 'utf-8'))
        elif(requestCode == "PLAY"):
            self.rtspclient.send(bytes(requestCode, 'utf-8'))
            # receive rtp packet and display
            if (self.state == "SETUP"):
                self.constructRTPclient()
            self.state = "PLAY"
        elif(requestCode == "PAUSE"):
            self.state = "PAUSE"
            self.rtspclient.send(bytes(requestCode, 'utf-8'))
        elif(requestCode == "TEARDOWN"):
            self.state = "INIT"
            self.rtspclient.send(bytes(requestCode, 'utf-8'))

    def recvRtspResponse(self):
        # Receive RTSP response from the server
        while True:
            response = self.rtspclient.recv(1024).decode("utf-8")
            print(response)
            # Close the RTSP socket if state is INIT
            if self.state == "INIT":
                self.rtspclient.shutdown(socket.SHUT_RDWR)
                self.rtspclient.close()
                break

    def constructRTPclient(self):
        self.rtpclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = self.serveraddr[0], self.serveraddr[1] + 1
        self.rtpclient.sendto(b'hi', address)

    def image_decode(self, image, str):
        with open(image, "wb") as writeFile:
            img = base64.decodebytes(str)
            writeFile.write(img)