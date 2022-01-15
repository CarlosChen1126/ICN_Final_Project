import base64
from RtpPacket import RtpPacket
import socket


class Clientworker:
    def __init__(self):
        pass

    def connectToServer(self, address, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        while(True):
            response = self.client.recv(1000000)
            self.rtp = RtpPacket()
            self.rtp.decode(response)
            print(len(self.rtp.getPayload()))
            self.seqnum = self.rtp.seqNum()
            self.bytedata = self.rtp.getPayload()
            self.image_decode("test_res.jpg", self.bytedata)
