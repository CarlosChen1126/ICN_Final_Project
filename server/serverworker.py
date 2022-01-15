from RtpPacket import RtpPacket


class Serverworker:
    def __init__(self):
        pass

    def createRTP(self, bytedata):
        #encode(self, Ver, P, X, CC, M, PT, SeqNum, SSI, CI, payload)
        rtp = RtpPacket()
        rtp.encode(2, 1, 1, 1, 1, 1, 1, 1, 1, bytedata)
        return rtp
