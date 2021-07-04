import socket
import threading
import pickle
import os
import sys

from bolonization import GameServer

def read_msg(sock_cli, addr_cli, username_cli):
    try:
        while True:
            # terima pesan
            data = sock_cli.recv(65535)
            if len(data) == 0:
                break

            # parsing pesannya
            parsed_data = pickle.loads(data)
            if "room" in parsed_data:
                if parsed_data["room"] == "new":
                    room = username_cli
                    rooms[room] = GameServer(parsed_data['num_box'])
                else:
                    room = parsed_data["room"]

                if room in rooms:
                    rooms[room].addPlayer(username_cli)
                    data = {}
                    data['num_box'] = rooms[room].num_box
                    data['player_num'] = len(rooms[room].getScores())
                    players[username_cli]['room_key'] = room
                    sock_cli.send(pickle.dumps(data))

                continue

            if "ready" in parsed_data:
                room = players[username_cli]['room_key']
                scores = rooms[room].getScores()
                data = {'scores': scores}

                for player in rooms[room].getPlayer():
                    players[player]['socket'].send(pickle.dumps(data))

                continue

            room = rooms[players[username_cli]['room_key']]
            if room.updateBoard(parsed_data):
                data = room.getBoard()
                room.turn = room.turn + 1
                data['turn'] = room.turn
                data['scores'] = room.getScores()
                for player in room.getPlayer():
                    players[player]['socket'].send(pickle.dumps(data))
        sock_cli.close()
        print("Connection closed", addr_cli)
    except:
        room = players[username_cli]['room_key']
        rooms[room].removePlayer(username_cli)
        scores = rooms[room].getScores()
        data = {'scores': scores}
        for player in rooms[room].getPlayer():
            players[player]['socket'].send(pickle.dumps(data))

        if len(rooms[room].getPlayer()) < 1:
            del rooms[room]

def start_server_game():
    try:
        threads = []
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
            username_cli = sock_cli.recv(65535).decode("utf-8")
            print(username_cli, " joined")

            # buat thread baru untuk membaca pesan dan jalankan threadnya
            thread_cli = threading.Thread(target=read_msg, args=(sock_cli, addr_cli, username_cli))
            thread_cli.start()
            threads.append(thread_cli)

            # testing
            players[username_cli] = {'socket': sock_cli, 'address': addr_cli, 'thread': thread_cli}

    except:
        for p in players:
            players[p]['socket'].close()
        sock_server.close()
        for t in threads:
            t.join()
        sys.exit(0)
# buat dictionary utk menyimpan informasi ttg klien
players = {} # {'username': (sock_cli, addr_cli, thread_cli)}
rooms = {} # {room_number: room_object}

def start_chat():
    print(5)
    
def start_app():
    thread_game = threading.Thread(target=start_server_game, args=())
    thread_game.start()
    thread_chat = threading.Thread(target=start_chat, args=())
    thread_chat.start()

if __name__ == '__main__':
    start_app()