import socket
import select
import sys
import os
import re
import threading
import queue

class serverThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.q = queue.Queue()

    def add(self, data, sock):
        print('adding data')
        self.q.put((data, sock))

    def stop(self):
        self.running = False

    def run(self):
        q = self.q
        # print('nihao')
        while self.running:
            try:
                # block for 1 second only:
                value = q.get(block=True, timeout=1)
                # print('got data')
                print(value)
                process(value[0], value[1])
            except queue.Empty:
                sys.stdout.write('.')
                sys.stdout.flush()

        if not q.empty():
            print("Elements left in the queue:")
            while not q.empty():
                print(q.get())
        # self.server(self.sock)

def process(data, sock):
    data = data.decode('utf-8')
    # print(data)
    
    request_header = data.split('\r\n')
    # print(request_header)
    if len(request_header[0]) < 1:
        return
    print(request_header[0])
    request_file = re.findall(r"GET /([A-Za-z0-9\.'%20'\-]*)", request_header[0])
    print(request_file)
    
    try:
        request_file = ' '.join(request_file[0].split('%20'))
    except:
        request_file = ''
    response_header = b''
    response_data = b''
    
    print('req: ', request_file)
    if request_file == 'index.html' or request_file == '':
        fname = os.path.join('server', 'index.html')
        f = open(fname, 'r')
        response_data = f.read()
        f.close()
        
        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                            + str(content_length) + '\r\n\r\n'

        sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
    elif request_file == 'dataset' or request_file == '/dataset':
        fname = os.path.join('server', 'dataset')

        list = os.listdir(fname)
        list.sort(key=lambda a: a.lower())
        r = []
        r.append('<!DOCTYPE HTML>')
        r.append('<html>\n<head>')
        r.append('<meta http-equiv="Content-Type" '
                'content="text/html"; charset="UTF-8">')
        r.append('<title>This is a tile</title>\n</head>' )
        r.append('<body>\n<h1>This is a tile</h1>')
        r.append('<hr>\n<ul>')
        for name in list:
            fullname = os.path.join(fname, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            r.append('<li><a href="%s">%s</a></li>'
                    % (linkname,displayname))
        r.append('</ul>\n<hr>\n</body>\n</html>\n')

        response_data = ''.join(r)
        content_length = len(response_data)
        print(response_data)
        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                            + str(content_length) + '\r\n\r\n'
        sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
    else:
        # sock.sendall(b'HTTP/1.1 404 Not found\r\n\r\n')
        filepath = find_file(request_file)
        print('fpath; ', filepath )
        if filepath is None:
            fname = os.path.join('server', '404.html')
            f = open(fname, 'rb')
            response_data = f.read()
            f.close()
            
            content_length = len(response_data)
            response_header = 'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                            + str(content_length) + '\r\n\r\n'
        else:
            fname = filepath
            f = open(fname, 'rb')
            response_data = f.read()
            f.close()
            content_length = len(response_data)

            response_header = 'HTTP/1.1 200 OK \r\nContent-Disposition: attachment; filename="' + request_file + '"\r\nContent-Type: application/octet-stream\r\n \
                Content-Length:' \
                            + str(content_length) + '\r\n\r\n'
        # print('tes ', response_header)
        sock.sendall(response_header.encode('utf-8') + response_data)
        sock.sendall(b'')
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    return

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def getPort(config):
    try:
        res = re.findall(r'Listen ([0-9]+)', config)
        return res[0]
    except:
        return None

def find_file(filename):
    for root, dirs, files in os.walk('.'):
        for f in files:
            # print(f)
            # print(filename)
            if filename == f:
                # print('test', root)
                return os.path.join(root, f)

    return None

def cleanup():
    t.stop()
    t.join()

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

t = serverThread()
t.start()

ip_address = get_ip_address()
print('ip: ', ip_address)
server_address = (ip_address, port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

while True:
    try:
        # print('tes')
        client, address = server_socket.accept()
        read_ready, write_ready, exception = select.select([client, ], [], [])
        
        if read_ready[0]:
            data = client.recv(4096)
            t.add(data, client)
        # print('wokow')
        # for sock in read_ready:
        #     print('halo')
        #     if sock == server_socket:
        #         print('hehe')
        #         client_socket, client_address = server_socket.accept()
        #         input_socket.append(client_socket)                       
            
        #     else:  
        #         # serverThread(sock)
        #         print('tus')    
        #         data = sock.recv(4096)
        #         t.add(data, sock)
        #         client_socket.shutdown(socket.SHUT_RDWR)
        #         client_socket.close()
        #         input_socket.remove(client_socket)

    except KeyboardInterrupt:        
        server_socket.close()
        cleanup()
        sys.exit(0)
        break
    except Exception as e:
        print((str(e)))
        pass
cleanup()
sys.exit(0)