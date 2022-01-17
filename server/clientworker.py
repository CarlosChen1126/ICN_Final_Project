import base64
from RtpPacket import RtpPacket
import socket
import threading
import cv2
import os


class Clientworker:
    SETUP = 0
    PAUSE = 1
    STOP = 2
    TEARDOWN = 3
    self.state = "INIT"

    def __init__(self):
        pass

    def connectToServer(self, address, port1, port2):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.RTSPclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((address, port1))
            self.RTSPclient.connect((address, port2))
        except:
            print("Can not connect to server.")

    def image_decode(self, image, str):
        with open(image, "wb") as writeFile:
            img = base64.decodebytes(str)
            writeFile.write(img)

    def sendRTSP(self, inst):
        if inst == self.SETUP and self.state == "INIT":
            request_msg = "SETUP"
            self.state = "SETUP"
        elif inst == self.PLAY and self.state == "SETUP":
            t = threading.Thread(target=self.recvRTSP)
            request_msg = "PLAY"
            self.state = "PLAY"
        elif inst == self.PAUSE and self.state == "PLAY":
            request_msg = "PAUSE"
            self.state = "PAUSE"
        elif inst == self.TEARDOWN and not self.state == "INIT":
            request_msg = "TEARDOWN"
            self.state = "TEARDOWN"

        self.RTSPclient.send(request_msg)

    def recvRTSP(self):

    def recvRTP(self):
        bytedata = b''
        self.seqnum = 1
        while(True):
            response = self.client.recv(65535)
            rtp = RtpPacket()
            rtp.decode(response)
            print(len(rtp.getPayload()))
            if(rtp.getPayload()):
                self.seqnum = rtp.seqNum()
                bytedata = rtp.getPayload()
                cache_name = "test_res.jpg"
                self.image_decode(cache_name, bytedata)
                img = cv2.imread(cache_name)
                cv2.imshow('My Image', img)
            else:
                break
            if cv2.waitKey(1) == ord('q'):
                break
        # 刪除cache的檔案
        os.remove(cache_name)
        cv2.destroyAllWindows()

    def run(self):
        # bytedata = b''
        # self.seqnum = 1
        # while(True):
        #     response = self.client.recv(65535)
        #     rtp = RtpPacket()
        #     rtp.decode(response)
        #     print(len(rtp.getPayload()))
        #     if(rtp.getPayload()):
        #         self.seqnum = rtp.seqNum()
        #         bytedata = rtp.getPayload()
        #         cache_name = "test_res.jpg"
        #         self.image_decode(cache_name, bytedata)
        #         img = cv2.imread(cache_name)
        #         cv2.imshow('My Image', img)
        #     else:
        #         break
        #     if cv2.waitKey(1) == ord('q'):
        #         break
        # # 刪除cache的檔案
        # os.remove(cache_name)
        # cv2.destroyAllWindows()
