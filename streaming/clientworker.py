import base64
import socket
import threading
import pyaudio
from RtpPacket import RtpPacket


class Clientworker:
    RTSP_VER = "RTSP/1.0"
    TRANSPORT = "RTP/UDP"

    def __init__(self):
        self.rtspSeq = 0        # rtsp request's sequence number
        self.state = "INIT"     # have five state : INIT SETUP PLAY PAUSE OFF
        self.serveraddr = 0
        self.rtpPort = 10
        self.sessionId = 0
        self.requestSent = 0
        self.p = pyaudio.PyAudio()
        self.stream = 0
        self.videobuffer = [0 for i in range(200)]
        self.videoframe = 1
        self.videorecordframe = 0
        self.audiobuffer = [0 for i in range(200)]
        self.audioframe = 1
        self.audiorecordframe = 0
        self.flag = threading.Event()
        self.flag.clear()
        self.running = threading.Event()
        self.running.set()

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
            session = int(lines[2].split(' ')[1])
            # only handle right sequence number
            if(self.rtspSeq == seqNum):
                # Close the RTSP socket if state is INIT
                if self.sessionId == 0:
                    self.sessionId = session
                if self.requestSent == "SETUP":
                    if(int(lines[0].split(' ')[1]) == 200):
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
                        threading.Thread(target=self.write_video).start()
                        threading.Thread(target=self.write_audio).start()
                        threading.Thread(target=self.play_audio).start()
                    else:
                        #file not found
                        input_file = input('File not found. Try anothor file: ')
                        self.fileName = "./video/"+input_file
                        self.sendRtspRequest("SETUP")

                elif self.requestSent == "PLAY":
                    self.state = "PLAY"
                    self.flag.set()
                elif self.requestSent == "PAUSE":
                    self.state = "PAUSE"
                    self.flag.clear()
                elif self.requestSent == "TEARDOWN":
                    self.state = "INIT"
                    self.rtspclient.shutdown(socket.SHUT_RDWR)
                    self.rtspclient.close()
                    self.flag.set()
                    self.running.clear()
                    break

    def constructRTPclient(self):
        # handle video transmission
        self.rtpclient_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Set the timeout value of the socket to 0.5sec
        self.rtpclient_video.settimeout(0.5)
        address = self.serveraddr[0], self.serveraddr[1] + 1
        self.rtpclient_video.sendto(b'hi', address)

        # handle audio transmission
        self.rtpclient_audio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = self.serveraddr[0], self.serveraddr[1] + 2
        self.rtpclient_audio.sendto(b'hi', address)

    def write_video(self):
        while self.running.isSet():
            self.flag.wait()
            if (self.state == "PLAY"):
                try:
                    video = self.rtpclient_video.recv(65535)
                    if video:
                        #影片還沒播完
                        rtp = RtpPacket()
                        rtp.decode(video)
                        #print('payload: ', len(rtp.getPayload()))
                        bytedata = rtp.getPayload()
                        self.videorecordframe = rtp.seqNum()
                        self.videobuffer[rtp.seqNum()%200] = bytedata
                    else:
                        #影片播完了
                        """ Graceful shutdown """ 
                        break
                except Exception as e:
                    print(e)
                    if self.state == "PLAY":
                        #影片播完了
                        self.state = "OFF"
                        break
            elif(self.state == "INIT" or self.state == "OFF"):
                break

    def write_audio(self):
        while self.running.isSet():
            self.flag.wait()
            if (self.state == "PLAY"):
                audio = self.rtpclient_audio.recv(65535)
                if audio:
                    #聲音還沒播完
                    rtp = RtpPacket()
                    rtp.decode(audio)
                    #print('payload: ', len(rtp.getPayload()))
                    bytedata = rtp.getPayload()
                    self.audiorecordframe = rtp.seqNum()
                    self.audiobuffer[rtp.seqNum()%200] = bytedata
                else:
                    #聲音播完了
                    """ Graceful shutdown """ 
                    break
            elif(self.state == "INIT" or self.state == "OFF"):
                break
    def play_audio(self):
        while self.running.isSet():
            self.flag.wait()
            if (self.state == "PLAY"):
                if(self.audiobuffer[self.audioframe%200] != 0 and self.audioframe <= self.audiorecordframe):
                    try:
                        self.stream.write(self.audiobuffer[self.audioframe%200])
                        self.audioframe += 1
                    except:
                        self.stream.close()
                        self.p.terminate()
                        self.running.clear()
            elif(self.state == "INIT" or self.state == "OFF"):
                self.running.clear()

    def image_decode(self, image, str):
        with open(image, "wb") as writeFile:
            img = base64.decodebytes(str)
            writeFile.write(img)
