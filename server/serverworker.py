from RtpPacket import RtpPacket
import socket


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
