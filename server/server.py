import socket
import sys
import cv2
import base64
from serverworker import Serverworker, Video, Audio
from VideoStream import VideoStream
import threading

# Specify the IP addr and port number
# (use "127.0.0.1" for localhost on local machine)
# Create a socket and bind the socket to the addr
HOST, PORT = sys.argv[1], int(sys.argv[2])

rtspserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rtspserver.bind((HOST, PORT))
rtspserver.listen(1)
rtpserver_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rtpserver_video.bind((HOST, PORT + 1))

rtpserver_audio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rtpserver_audio.bind((HOST, PORT + 2))


connect_socket, client_addr = rtspserver.accept()
print(client_addr)
serverworker = Serverworker()
while(True):
    data = str(connect_socket.recv(1024), encoding='utf-8')
    print(data)
    # Get the request type
    request = data.split('\n')
    line1 = request[0].split(' ')
    requestType = line1[1]

    # Get the media file name
    filename = line1[2]

    # Get the RTSP sequence number
    if(requestType == "SETUP"):
        seqnum = request[2].split(' ')[1]
    else:
        seqnum = request[1].split(' ')[1]

    if (requestType == "SETUP"):
        try:
            videostream = VideoStream(filename)

            reply = 'RTSP/1.0 200 OK\nCSeq: ' + seqnum + '\nSession: ' + str(123)
            connect_socket.send(bytes(reply, 'utf-8'))

            # 收到SETUP就建立video
            client, address = rtpserver_video.recvfrom(1024)
            video = Video(videostream, rtpserver_video, serverworker, address)
            threading.Thread(target=video.run).start()

            # 收到SETUP就建立audio
            client, address = rtpserver_audio.recvfrom(1024)
            audio = Audio("./image/movie.wav", rtpserver_audio, serverworker, address)
            threading.Thread(target=audio.run).start()
        except IOError:
            reply = 'RTSP/1.0 404 Not Found\nCSeq: ' + seqnum + '\nSession: ' + str(123)
            connect_socket.send(bytes(reply, 'utf-8'))
    elif (requestType == "PLAY"):
        reply = 'RTSP/1.0 200 OK\nCSeq: ' + seqnum + '\nSession: ' + str(123)
        connect_socket.send(bytes(reply, 'utf-8'))
        video.resume()
        audio.resume()
    elif(requestType == "PAUSE"):
        reply = 'RTSP/1.0 200 OK\nCSeq: ' + seqnum + '\nSession: ' + str(123)
        connect_socket.send(bytes(reply, 'utf-8'))
        video.pause()
        audio.pause()
    elif(requestType == "TEARDOWN"):
        reply = 'RTSP/1.0 200 OK\nCSeq: ' + seqnum + '\nSession: ' + str(123)
        connect_socket.send(bytes(reply, 'utf-8'))
        video.stop()
        audio.stop()
        break
connect_socket.close()