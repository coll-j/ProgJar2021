# Imports
import pygame
import socket
import sys
import threading
import pickle
import os

from bolonization import GameClient
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Expected Username as command line argument')
        exit()

    # buat object socket
    sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect ke server
    sock_cli.connect(("127.0.0.1", 6666))

    # kirim username ke server
    username = sys.argv[1]
    data = "{}|{}".format(username, 7)
    sock_cli.send(bytes(data, "utf-8"))

    game = GameClient(7, 2)
    print_hi('PyCharm')
    while True:
        game.update()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
