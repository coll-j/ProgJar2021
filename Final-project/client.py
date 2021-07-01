# Imports
import pygame
import socket
import sys
import threading
import pickle
import os

from bolonization import GameClient

def read_msg(sock_cli):
    while True:
        # terima pesan
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break

        game.updateBoard(data)

game = None
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
        data = "{}|{}".format(username, 7)
        sock_cli.send(bytes(data, "utf-8"))

        # buat thread utk membaca pesan dan jalankan threadnya
        thread_cli = threading.Thread(target=read_msg, args=(sock_cli,))
        thread_cli.start()

        game = GameClient(7, 1, sock_cli)
        while True:
            game.update()
            if not game.isRunning():
                break

    except SystemExit:
        thread_cli.join()
        sock_cli.close()
        sys.exit(0)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
