# import required module
import socket
import select
import sys 
import os
def server_side():
    server_socket = server_start()
    try : 
        server_run(server_socket)
    # when user press CTRL + C (in Linux), close socket server and exit
    except KeyboardInterrupt:
        server_socket.close()
        sys.exit(0)

def server_start():
    # creating socket server object, bind, and listen
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5003))
    server_socket.listen(5)
    return server_socket



def server_run(server_socket):
    # list to store accepted client
    input_list = [server_socket]
    while 1:
        # serving multiple client alternately; one socket in a time
        input, output, exception = select.select(input_list, [], [])
    
        for socket in input:
            # accept client and add it to list input
            if socket == server_socket:            
                client_socket, client_address = server_socket.accept()
                input_list.append(client_socket)
                print("Accepted client: ", client_address)                           
            
            # handle sending and receiving message    
            else:                                        
                message = socket.recv(1024)
                if message:
                    print("Message received: ", message.decode('utf-8'))
                    filename = message.decode("utf-8").split(' ')[1]    
                    filepath = find_file(filename)
                    if filepath is None:
                        print("File not found")
                        break
                    print("File found at: ", filepath)              
                    file = open(filepath)
                    file.seek(0, os.SEEK_END)
                    message_to_send = "file-name: "+ message.decode("utf-8")+ ",\nfile_size: "+ str(file.tell())+ ",\n\n\n"
                    socket.send(message_to_send.encode('utf-8'))
                    file.close()
                    file = open(filepath, 'rb')
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        socket.send(data)
                    socket.send(b'')
                    print("File is sended to ",client_address)
                    socket.close()
                    input_list.remove(socket)
                else:                    
                    socket.close()                    
                    input_list.remove(socket)

def find_file(filename):
    for root, dirs, files in os.walk('.'):
        for f in files:
            if filename == f:
                return os.path.join(root, f)

    return None

if __name__ == '__main__':
    server_side()