import socket
import threading
import pickle
import os
import sys

from bolonization import GameServer

def read_msg(sock_cli, addr_cli, username_cli):
    while True:
        # terima pesan
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break

        # parsing pesannya
        parsed_data = pickle.loads(data)
        room = rooms[players[username_cli]['room_key']]
        if room.updateBoard(parsed_data):
            new_board = pickle.dumps(room.getBoard())
            for player in room.getPlayer():
                players[player]['socket'].send(new_board)
        print("parsed: ", parsed_data)
    sock_cli.close()
    print("Connection closed", addr_cli)

# buat dictionary utk menyimpan informasi ttg klien
players = {} # {'username': (sock_cli, addr_cli, thread_cli)}
rooms = {} # {room_number: room_object}

if __name__ == '__main__':
    threads = []
    try:
        # buat object socket server
        sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # buat object socket server
        sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # binding object socket ke alamat IP dan port tertentu
        sock_server.bind(("0.0.0.0", 6666))

        # listen for an incoming connection
        sock_server.listen(5)

        while True:
            # accept connection dari klien
            sock_cli, addr_cli = sock_server.accept()

            # baca username klien
            username_cli, num_box = sock_cli.recv(65535).decode("utf-8").split('|')
            print(username_cli, " joined")

            # buat thread baru untuk membaca pesan dan jalankan threadnya
            thread_cli = threading.Thread(target=read_msg, args=(sock_cli, addr_cli, username_cli))
            thread_cli.start()
            threads.append(thread_cli)

            # testing
            players[username_cli] = {'socket': sock_cli, 'address': addr_cli, 'thread': thread_cli}

            if len(rooms) == 0:
                # Create room
                print("room created")
                rooms[username_cli] = GameServer(int(num_box))
                rooms[username_cli].addPlayer(username_cli)
                players[username_cli]['room_key'] = username_cli
            else:
                # Join room
                avail_room = list(rooms.keys())[0]
                print("{} joining room {}".format(username_cli, avail_room))
                r = rooms[avail_room].addPlayer(username_cli)
                players[username_cli]['room_key'] = avail_room
    except:
        sock_server.close()
        for p in players:
            players[p]['socket'].close()
        for t in threads:
            t.join()
        sys.exit(0)