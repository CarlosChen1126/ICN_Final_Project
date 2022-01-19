from RtpPacket import RtpPacket
import socket
import threading
import cv2
import base64
import wave


class Serverworker:
    def __init__(self):
        pass

    def startServer(self, address, port1, port2):
        # RTP/UDP
        RTPserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # RTSP/TCP
        RTSPserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        RTPserver.bind((address, port1))
        RTPserver.listen(0)
        RTSPserver.bind((address, port2))

    def createRTP(self, frameNbr, bytedata):
        #encode(self, Ver, P, X, CC, M, PT, SeqNum, SSI, CI, payload)
        version = 2
        padding = 0
        extension = 0
        cc = 0
        marker = 0
        pt = 26  # MJPEG type
        seqnum = frameNbr
        ssrc = 0
        ci = 0

        rtp = RtpPacket()
        rtp.encode(version, padding, extension, cc,
                   marker, pt, seqnum, ssrc, ci, bytedata)
        return rtp


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
                rtp = self.serverworker.createRTP(
                    self.video.frameNbr(), bytedata)
                #print(len(rtp.getPayload()))
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

class Audio(threading.Thread):
    chunk = 1024

    def __init__(self, file, rtpserver, serverworker, address):
        """ Init audio stream """ 
        self.wf = wave.open(file, 'rb')
        self.flag = threading.Event()
        self.flag.clear()
        self.running = threading.Event()
        self.running.set()
        self.rtpserver = rtpserver
        self.serverworker = serverworker
        self.address = address
        self.frameNbr = 0

    def run(self):
        while self.running.isSet():
            self.flag.wait()
            frame = self.wf.readframes(self.chunk)
            cv2.waitKey(120)
            self.frameNbr += 1
            if frame:
                # 聲音還沒播完
                # encode frame
                rtp = self.serverworker.createRTP(
                    self.frameNbr, frame)
                #print(len(rtp.getPayload()))
                self.rtpserver.sendto(rtp.getPacket(), self.address)
            else:
                # 聲音播完了
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