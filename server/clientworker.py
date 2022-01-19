import base64
import socket


class Clientworker:
    RTSP_VER = "RTSP/1.0"
    TRANSPORT = "RTP/UDP"

    def __init__(self):
        self.rtspSeq = 0        # rtsp request's sequence number
        self.state = "INIT"     # have four state : INIT SETUP PLAY PAUSE
        self.serveraddr = 0
        self.fileName = "./image/tt.mjpg"
        self.rtpPort = 10
        self.sessionId = 0

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
            self.state = "SETUP"
            # threading.Thread(target=self.recvRtspResponse).start()

            # Write the RTSP request to be sent.
            request = "Request: %s %s %s" % (
                requestCode, self.fileName, self.RTSP_VER)
            request += "\nTransport: %s; client_port= %d" % (
                self.TRANSPORT, self.rtpPort)
            request += "\nCSeq: %d" % self.rtspSeq

            self.rtspclient.send(bytes(request, 'utf-8'))
            self.constructRTPclient()
        elif(requestCode == "PLAY"):
            self.state = "PLAY"

            # Write the RTSP request to be sent.
            request = "Request: %s %s %s" % (
                requestCode, self.fileName, self.RTSP_VER)
            request += "\nCSeq: %d" % self.rtspSeq
            request += "\nSession: %d" % self.sessionId

            self.rtspclient.send(bytes(request, 'utf-8'))
        elif(requestCode == "PAUSE"):
            self.state = "PAUSE"

            # Write the RTSP request to be sent.
            request = "Request: %s %s %s" % (
                requestCode, self.fileName, self.RTSP_VER)
            request += "\nCSeq: %d" % self.rtspSeq
            request += "\nSession: %d" % self.sessionId

            self.rtspclient.send(bytes(request, 'utf-8'))
        elif(requestCode == "TEARDOWN"):
            self.state = "INIT"

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
            # Close the RTSP socket if state is INIT
            if self.state == "INIT":
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

    def image_decode(self, image, str):
        with open(image, "wb") as writeFile:
            img = base64.decodebytes(str)
            writeFile.write(img)
