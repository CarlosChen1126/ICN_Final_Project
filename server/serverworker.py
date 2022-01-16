from RtpPacket import RtpPacket


class Serverworker:
    def __init__(self):
        pass

    def createRTP(self, bytedata):
        #encode(self, Ver, P, X, CC, M, PT, SeqNum, SSI, CI, payload)
        version = 2
        padding = 0
        extension = 0
        cc = 0
        marker = 0
        pt = 26 # MJPEG type
        seqnum = 0
        ssrc = 0
        ci = 0

        rtp = RtpPacket()
        rtp.encode(version, padding, extension, cc, marker, pt, seqnum, ssrc, ci, bytedata)
        return rtp
