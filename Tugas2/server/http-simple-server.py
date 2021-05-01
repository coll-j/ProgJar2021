import socket
import select
import sys
import os
import re

def getPort(config):
    try:
        res = re.findall(r'Listen ([0-9]+)', config)
        return res[0]
    except:
        return None

config_path = os.path.join('server', 'httpserver.conf')
with open(config_path) as config:
    config = config.read()
    port = getPort(config)
    if port:
        port = int(port)
        print('port: ', port)
    else:
        print('Port configuration not found on file: {}'.format(config_path))
        sys.exit(1)

server_address = ('127.0.0.1', port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)                       
            
            else:                
                # receive data from client, break when null received          
                data = sock.recv(4096)
                data = data.decode('utf-8')
                print(data)
                
                request_header = data.split('\r\n')
                # print(request_header)
                if len(request_header[0]) < 1:
                    continue
                request_file = request_header[0].split()[1]
                response_header = b''
                response_data = b''
                
                print(request_file)
                if request_file == 'index.html' or request_file == '/' or request_file == '/index.html':
                    fname = os.path.join('server', 'index.html')
                    f = open(fname, 'r')
                    response_data = f.read()
                    f.close()
                    
                    content_length = len(response_data)
                    response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                      + str(content_length) + '\r\n\r\n'

                    sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

                else:
                    # sock.sendall(b'HTTP/1.1 404 Not found\r\n\r\n')
                    fname = os.path.join('server', '404.html')
                    f = open(fname, 'r')
                    response_data = f.read()
                    f.close()
                    
                    content_length = len(response_data)
                    response_header = 'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                      + str(content_length) + '\r\n\r\n'

                    sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)
