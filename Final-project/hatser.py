##Python codes to do server-side part of chat room.
import socket
import threading
import os
import sys

clients=[]

def recv_msg(sock_ser):
    while True:
        msg = sock_ser.recv(32768)
        send_to_all_msg(msg, sock_ser)

def send_to_all_msg(msg,con):
    for client in clients:
        client.send(msg)
        # client.send(bytes(msg, "utf-8"))
        # client.send(msg.encode('ascii'))
         
def send_to_all_img(msg,con):
    for client in clients:
        client.send(msg)
        # client.send(bytes(msg, "utf-8"))
        # client.send(msg.encode('ascii')) 

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