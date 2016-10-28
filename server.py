import socket
import os


os.system('arp -s 10.0.0.2 00:00:00:00:00:02')

listenAddress = ('10.0.0.1', 9270)
socketServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketServer.bind(listenAddress)

while True:
    data, clintAddress = socketServer.recvfrom(2048)
    print "received:", data, "from", clintAddress
    responseAddress = (clintAddress[0], 9271)
    socketResponse = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    response = str(data).split("#")[0]
    print "response:", response
    socketResponse.sendto(response, responseAddress)
    socketResponse.close()

socketServer.close()
