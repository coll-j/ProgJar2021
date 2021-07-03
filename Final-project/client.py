# Imports
import pygame
import socket
import sys
import threading
import pickle
import os

from bolonization import GameClient

global game
game = None

def read_msg(sock_cli):
    try:
        while True:
            # terima pesan
            data = sock_cli.recv(65535)
            if len(data) == 0:
                break

            parsed_data = pickle.loads(data)

            if 'scores' in parsed_data:
                if game is not None:
                    game.scores = parsed_data['scores']

            if game is not None:
                game.updateBoard(parsed_data)
    except:
        pass


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Expected Username as command line argument')
        exit()

    try:
        # buat object socket
        sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect ke server
        sock_cli.connect(("127.0.0.1", 6666))

        # kirim username ke server
        username = sys.argv[1]
        data = "{}".format(username)
        sock_cli.send(bytes(data, "utf-8"))


        # response = sock_cli.recv(655535).decode("utf-8")
        # num_box, player_num = response.split("|")


        data = {}
        room = input('Ketik nama room untuk bergabung atau ketik "new" untuk membuat room baru: ')
        if room == 'new':
            data['room'] = room
            num_box = int(input("Masukkan jumlah kotak: "))
            data['num_box'] = num_box
        else:
            data['room'] = room

        sock_cli.send(pickle.dumps(data))
        data = sock_cli.recv(65535)
        parsed_data = pickle.loads(data)

        game = GameClient(parsed_data['num_box'], parsed_data['player_num'])
        data = {"ready": True}
        sock_cli.send(pickle.dumps(data))

        # buat thread utk membaca pesan dan jalankan threadnya
        thread_cli = threading.Thread(target=read_msg, args=(sock_cli,))
        thread_cli.start()
        while True:
            game.update()
            if not game.isRunning():
                exit()
                break

            if game.hasMoved():
                data = game.getMove()
                sock_cli.send(data)
                game.setMoved(False)

    except:
        sock_cli.close()
        # try:
        #     thread_cli.join()
        # finally:
        sys.exit(-1)

    sys.exit(0)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
