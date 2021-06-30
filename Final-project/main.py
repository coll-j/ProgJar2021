# Imports
import pygame
from bolonization import Bolonization
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game = Bolonization(7, 2)
    print_hi('PyCharm')
    while True:
        game.update()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
