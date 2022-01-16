import base64
from RtpPacket import RtpPacket
import socket
import cv2
import os


class Clientworker:
    def __init__(self):
        pass

    def connectToServer(self, address, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.client.connect((address, port))
        except:
            print("Can not connect to server.")

    def image_decode(self, image, str):
        with open(image, "wb") as writeFile:
            img = base64.decodebytes(str)
            writeFile.write(img)

    def run(self):
        self.bytedata = b''
        self.seqnum = 1
        self.client.send(b'hi')
        while(True):
            response = self.client.recv(65535)
            rtp = RtpPacket()
            rtp.decode(response)
            print(len(rtp.getPayload()))
            if(rtp.getPayload()):
                self.seqnum = rtp.seqNum()
                self.bytedata = rtp.getPayload()
                cache_name = "test_res.jpg"
                self.image_decode(cache_name, self.bytedata)
                img = cv2.imread(cache_name)
                cv2.imshow('My Image', img)
            else:
                break
            if cv2.waitKey(1) == ord('q'):
                break
        #刪除cache的檔案
        os.remove(cache_name)
        cv2.destroyAllWindows()
            
