##Python codes to do server-side part of chat room.
import socket
import threading
import os
import sys

clients=[]

def recv_msg(sock_ser):
    while True:
        msg = sock_ser.recv(32768)
        if msg.decode('utf-8') == "msg":
            send_to_all_msg(msg, sock_ser)
        if msg.decode('utf-8') == "img":
            send_to_all_img(msg, sock_ser)

def server_recieve_file(server_socket,filename):

    size = server_socket.recv(32768)
    size = size.decode('utf-8')
    size = int(float(size))
    size += 1
    file = open(filename, 'wb')
    while size > 0:
        data = server_socket.recv(32768)
        file.write(data)
        size -= 1
    file.close()

def server_send_file(server_socket,filename):
    file = open(filename)
    file.seek(0, os.SEEK_END)
    filesize =str(file.tell()/32768)
    server_socket.send(bytes(filesize,"utf-8"))
    file.close()

    file = open(filename,'rb')
    while True:
        data = file.read(32768)
        if not data:
            break
        server_socket.send(data)
    file.close()

def send_to_all_msg(msg,con):
    for client in clients:
        client.send(msg)

    msg = con.recv(32768)
    for client in clients:
        client.send(msg)
         
def send_to_all_img(msg,con):
    for client in clients:
        client.send(msg)
        
    msg = con.recv(32768)
    for client in clients:
        client.send(msg)

    server_recieve_file(con, msg.decode('utf-8'))
    for client in clients:
        server_send_file(client, msg.decode('utf-8'))
        
    # for client in clients:
    #     client.send(msg)


def window_start():
    try:
        # buat object socket server
        sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # binding object socket ke alamat IP dan port tertentu
        sock_server.bind(("0.0.0.0", 6669))

        # listen for an incoming connection
        sock_server.listen(10)

        while True:
            # accept connection dari klien
            sock_cli, _ = sock_server.accept()
            clients.append(sock_cli)
            
            # buat thread baru untuk membaca pesan dan jalankan threadnya
            thread_cli = threading.Thread(target=recv_msg, args=(sock_cli,))
            thread_cli.start()

    except:
        # for p in players:
        #     players[p]['socket'].close()
        # sock_server.close()
        # for t in threads:
        #     t.join()
        sys.exit(0)