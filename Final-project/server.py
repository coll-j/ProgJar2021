import socket
import threading
import os
from bolonization import GameServer

def read_msg(clients, sock_cli, addr_cli, username_cli):
    while True:
        # terima pesan
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break

        # parsing pesannya
    sock_cli.close()
    print("Connection closed", addr_cli)

if __name__ == '__main__':
# buat object socket server
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # buat object socket server
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # binding object socket ke alamat IP dan port tertentu
    sock_server.bind(("0.0.0.0", 6666))

    # listen for an incoming connection
    sock_server.listen(5)

    # buat dictionary utk menyimpan informasi ttg klien
    players = {} # {'username': (sock_cli, addr_cli, thread_cli)}
    rooms = {} # {room_number: room_object}

    while True:
        # accept connection dari klien
        sock_cli, addr_cli = sock_server.accept()

        # baca username klien
        username_cli, num_box = sock_cli.recv(65535).decode("utf-8").split('|')
        print(username_cli, " joined")

        # buat thread baru untuk membaca pesan dan jalankan threadnya
        thread_cli = threading.Thread(target=read_msg, args=(players, sock_cli, addr_cli, username_cli))
        thread_cli.start()

        # testing
        players[username_cli] = (sock_cli, addr_cli, thread_cli)
        if len(rooms) == 0:
            print("room created")
            rooms[username_cli] = GameServer(int(num_box))
        else:
            avail_room = list(rooms.keys())[0]
            print("{} joining room {}".format(username_cli, avail_room))
            r = rooms[avail_room].addPlayer(username_cli)