# import socket module
import socket 
import sys
import os

def client_side(filename):
    client_socket = client_start()
    # send message
    client_send_message(client_socket,filename)
    # get message
    if client_recieve_message(client_socket):
        # get file
        client_recieve_file(client_socket,filename)
    # close socket client 
    client_socket.close()
    print('Selesai')

def client_start():
    # creating socket client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # connect to server in defined address and port
    client_socket.connect(('localhost', 5003))

    return client_socket
def client_send_message(client_socket,filename):
    # send message to server
    filename = "unduh " + filename
    client_socket.send(filename.encode('utf-8'))

def client_recieve_message(client_socket):
    # receive message from server, 1024 is buffer size in bytes
    message = client_socket.recv(1024)
    if message.decode('utf-8') == "File not found":
        return False
    # print message
    print ("From server: " + message.decode("utf-8"))
    return True

def client_recieve_file(client_socket,filename):
    file = open(os.path.basename(filename), 'wb')
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        file.write(data)
    file.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Expected filename as command line argument')
        exit()
    client_side(sys.argv[1])
    
    