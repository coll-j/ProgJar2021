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

#-------------------------------------------

def read_msg_chat(clients, friends, sock_cli, addr_cli, username_cli):
    while True:
        # terima pesan
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break
        
        # parsing pesannya
        act = data.decode("utf - 8").split("|")[0]

        if act == 'get_user':
            send_user_list(clients, sock_cli)
        elif act == 'add':
            _, user_1, user_2 = data.decode("utf - 8").split("|")
            if user_2 in clients:
                add_friend(friends, user_1, user_2)
                send_msg(sock_cli, '{} added as friend'.format(user_2))
            else:
                send_msg(sock_cli, '{} not found'.format(user_2))

        elif act == 'chat':
            act, sender, dest, msg = data.decode("utf - 8").split("|")
            msg = "<{}>: {}".format(username_cli, msg)

            #terusankan psan ke semua klien
            if dest =="bcast":
                send_broadcast(clients, friends, '[bcast] ' + msg, addr_cli, sender)
            else:
                if dest in clients:
                    if dest in friends[sender]:
                        dest_sock_cli = clients[dest][0]
                        send_msg(dest_sock_cli, msg)
                    else:
                        send_msg(sock_cli, '{} is not a friend yet'.format(dest))
                else:
                    send_broadcast(clients, friends, '[bcast] ' + msg, addr_cli, sender)
            print(data)
        elif act == 'file':
            act, sender, dest, msg = data.decode("utf - 8").split("|")
            filename = msg
            server_recieve_file(sock_cli,filename)
            # terusankan file ke semua klien
            if dest =="bcast":
                send_broadcast(clients, friends,"file" , addr_cli, sender)
                send_file_broadcast(clients, friends,filename , addr_cli, sender)
            else:
                if dest in clients:
                    if dest in friends[sender]:
                        dest_sock_cli = clients[dest][0]
                        send_msg(dest_sock_cli, "file")
                        server_send_file(dest_sock_cli, filename)
                    else:
                        send_msg(sock_cli, '{} is not a friend yet'.format(dest))
                else:
                    send_broadcast(clients, friends, "file" , addr_cli, sender)
                    send_file_broadcast(clients, friends,filename, addr_cli, sender)
            print(data)
            os.remove(filename)
    sock_cli.close()
    print("Connection closed", addr_cli)

# kirim ke semua klien
def send_broadcast(clients, friends, data, sender_addr_cli, sender_uname):
    for uname in friends[sender_uname]:
        sock_cli, addr_cli, _ = clients[uname]
        if not (sender_addr_cli[0] == addr_cli[0] and sender_addr_cli[1] == addr_cli[1]):
            send_msg(sock_cli, data)

def send_msg(sock_cli, data):
    sock_cli.send(bytes(data, "utf-8"))

def send_user_list(clients, sock_cli):
    send_msg(sock_cli, ', '.join(clients.keys()))

def add_friend(friends, username_cli, username_friend):
    friends[username_cli].append(username_friend)

def server_recieve_file(server_socket,filename):

    size = server_socket.recv(65535)
    size = size.decode('utf-8')
    size = int(float(size))
    size += 1
    file = open(filename, 'wb')
    while size > 0:
        data = server_socket.recv(65535)
        file.write(data)
        size -= 1
    file.close()

def server_send_file(server_socket,filename):
    server_socket.send(bytes(filename,"utf-8"))

    file = open(filename)
    file.seek(0, os.SEEK_END)
    filesize =str(file.tell()/65535)
    server_socket.send(bytes(filesize,"utf-8"))
    file.close()

    file = open(filename,'rb')
    while True:
        data = file.read(65535)
        if not data:
            file.close()
            break
        server_socket.send(data)

def send_file_broadcast(clients, friends, filename, sender_addr_cli, sender_uname):
    for uname in friends[sender_uname]:
        sock_cli, addr_cli, _ = clients[uname]
        if not (sender_addr_cli[0] == addr_cli[0] and sender_addr_cli[1] == addr_cli[1]):
            server_send_file(sock_cli, filename)

def start_chat():
    try:
        # buat object socket server
        sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # buat object socket server
        sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # binding object socket ke alamat IP dan port tertentu
        sock_server.bind(("0.0.0.0", 6667))

        # listen for an incoming connection
        sock_server.listen(5)

        # buat dictionary utk menyimpan informasi ttg klien
        clients = {}
        friends = {}

        while True:
            # accept connection dari klien
            sock_cli, addr_cli = sock_server.accept()

            # baca username klien
            username_cli = sock_cli.recv(65535).decode("utf-8")
            print(username_cli, " joined")

            # buat thread baru untuk membaca pesan dan jalankan threadnya
            thread_cli = threading.Thread(target=read_msg_chat, args=(clients, friends, sock_cli, addr_cli, username_cli))
            thread_cli.start()

            # simpan informasi ttg klien ke dictionary
            clients[username_cli] = (sock_cli, addr_cli, thread_cli)
            friends[username_cli] = []
    except:
        pass



# buat dictionary utk menyimpan informasi ttg klien
players = {} # {'username': (sock_cli, addr_cli, thread_cli)}
rooms = {} # {room_number: room_object}


def start_app():
    thread_game = threading.Thread(target=start_server_game, args=())
    thread_game.start()
    thread_chat = threading.Thread(target=start_chat, args=())
    thread_chat.start()

if __name__ == '__main__':
    start_app()