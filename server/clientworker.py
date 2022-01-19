import base64
import socket
import threading
import pyaudio
from RtpPacket import RtpPacket


class Clientworker:
    RTSP_VER = "RTSP/1.0"
    TRANSPORT = "RTP/UDP"

    def __init__(self, input_file):
        self.rtspSeq = 0        # rtsp request's sequence number
        self.state = "INIT"     # have five state : INIT SETUP PLAY PAUSE "OFF"
        self.serveraddr = 0
        self.fileName = "./image/"+input_file
        self.rtpPort = 10
        self.sessionId = 0
        self.requestSent = 0
        self.p = pyaudio.PyAudio()
        self.stream = 0

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
        if(requestCode == "SETUP" and self.state == "INIT"):
            self.requestSent = "SETUP"
            threading.Thread(target=self.recvRtspResponse).start()

            # Write the RTSP request to be sent.
            request = "Request: %s %s %s" % (
                requestCode, self.fileName, self.RTSP_VER)
            request += "\nTransport: %s; client_port= %d" % (
                self.TRANSPORT, self.rtpPort)
            request += "\nCSeq: %d" % self.rtspSeq

            self.rtspclient.send(bytes(request, 'utf-8'))
        elif(requestCode == "PLAY" and self.state != "OFF"):
            self.requestSent = "PLAY"

            # Write the RTSP request to be sent.
            request = "Request: %s %s %s" % (
                requestCode, self.fileName, self.RTSP_VER)
            request += "\nCSeq: %d" % self.rtspSeq
            request += "\nSession: %d" % self.sessionId

            self.rtspclient.send(bytes(request, 'utf-8'))
        elif(requestCode == "PAUSE" and self.state != "OFF"):
            self.requestSent = "PAUSE"

            # Write the RTSP request to be sent.
            request = "Request: %s %s %s" % (
                requestCode, self.fileName, self.RTSP_VER)
            request += "\nCSeq: %d" % self.rtspSeq
            request += "\nSession: %d" % self.sessionId

            self.rtspclient.send(bytes(request, 'utf-8'))
        elif(requestCode == "TEARDOWN"):
            self.requestSent = "TEARDOWN"

            # Write the RTSP request to be sent.
            request = "Request: %s %s %s" % (
                requestCode, self.fileName, self.RTSP_VER)
            request += "\nCSeq: %d" % self.rtspSeq
            request += "\nSession: %d" % self.sessionId

            self.rtspclient.send(bytes(request, 'utf-8'))

    def recvRtspResponse(self):
        # Receive RTSP response from the server
        while True:
            response = self.rtspclient.recv(1024).decode("utf-8")
            print(response)
            lines = response.split('\n')
            seqNum = int(lines[1].split(' ')[1])
            # only handle right sequence number
            if(self.rtspSeq == seqNum):
                # Close the RTSP socket if state is INIT
                if self.requestSent == "SETUP":
                    self.state = "SETUP"
                    format = int(lines[3].split(' ')[1])
                    channel = int(lines[4].split(' ')[1])
                    rate = int(lines[5].split(' ')[1])
                    self.stream = self.p.open(
                        format = format,
                        channels = channel,
                        rate = rate,
                        output = True
                    )
                    self.constructRTPclient()
                    threading.Thread(target=self.play_audio).start()
                elif self.requestSent == "PLAY":
                    self.state = "PLAY"
                elif self.requestSent == "PAUSE":
                    self.state = "PAUSE"
                elif self.requestSent == "TEARDOWN":
                    self.state = "INIT"
                    self.rtspclient.shutdown(socket.SHUT_RDWR)
                    self.rtspclient.close()
                    break

    def constructRTPclient(self):
        # handle video transmission
        self.rtpclient_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = self.serveraddr[0], self.serveraddr[1] + 1
        self.rtpclient_video.sendto(b'hi', address)

        # handle audio transmission
        self.rtpclient_audio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = self.serveraddr[0], self.serveraddr[1] + 2
        self.rtpclient_audio.sendto(b'hi', address)

    def play_audio(self):
        while(True):
            if (self.state == "PLAY"):
                audio = self.rtpclient_audio.recv(65535)
                if audio:
                    #聲音還沒播完
                    rtp = RtpPacket()
                    rtp.decode(audio)
                    #print('payload: ', len(rtp.getPayload()))
                    bytedata = rtp.getPayload()
                    self.stream.write(bytedata)
                else:
                    #聲音播完了
                    """ Graceful shutdown """ 
                    self.stream.close()
                    self.p.terminate()
                    break
            elif(self.state == "INIT"):
                break

    def image_decode(self, image, str):
        with open(image, "wb") as writeFile:
            img = base64.decodebytes(str)
            writeFile.write(img)
