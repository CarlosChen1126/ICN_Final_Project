# ICN_Final_Project
This is the final project of the 110-1 ICN course.
***

## Program Structure
```sh
.
├── client
├── server
│   └── test_res.jpg
└── streaming
    ├── RtpPacket.py
    ├── VideoStream.py
    ├── clientworker.py
    ├── player_window.py
    ├── server.py
    ├── serverworker.py
    └── video
        ├── video1.mjpeg
        ├── video1.wav
        ├── video2.mjpeg
        └── video2.wav

4 directories, 11 files
```
***
### Usage
```py
#Server side
python3 server.py <ip address> <port>
#Client side
python3 player_window.py <ip address> <port>
```
