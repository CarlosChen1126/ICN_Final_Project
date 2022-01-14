import socket
import sys
# Specify the IP addr and port number
# (use "127.0.0.1" for localhost on local machine)
# Create a socket and bind the socket to the addr
# TODO start
HOST, PORT = sys.argv[1], int(sys.argv[2])
# # TODO end

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
while(True):
    # Listen for any request
    # TODO start
    # TODO end
    print("The Server is working...")

    while(True):
        # Accept a new request and admit the connection
        # TODO start
        client, address = server.accept()
        # TODO end
        print(str(address)+" connected")
        try:
            while (True):
                client.send(
                    b"Welcome to the streaming server.\n")
                # Receive the data from the client and send the answer back to the client
                # Ask if the client want to terminate the process
                # Terminate the process or continue
                # TODO start
                end = False
                while(end == False):
                    response = client.recv(1000).decode("utf-8")
                    print("response")
                    print(response)
                    answer = calculator(response)
                    answer = str(answer)
                    res = "Receive server message:\n" + \
                        "The answer is %s\n" % answer + \
                        "Do you have any question?(Y/N)\n"
                    client.send(
                        res.encode("utf-8")
                    )
                    res2 = client.recv(1000).decode("utf-8")
                    print("res2")
                    print(res2)
                    if(res2 == "n" or res2 == "N"):
                        end = True
                        client.send(b"Bye Bye\n")
                        break
                    elif(res2 == "y" or res2 == "Y"):
                        end = False
                        break
                    else:
                        client.send(b"Wrong response\n")
                        break
                if(end == True):
                    client.close()
                # TODO end
        except socket.error:
            print("except")
            print(socket.error)
