import pickle

import pygame
import math

class GameServer():
    def __init__(self, num_box):
        self.players = []
        self.num_box = num_box

        self.boardh = [[0 for x in range(self.num_box)] for y in range(self.num_box + 1)]
        self.boardv = [[0 for x in range(self.num_box + 1)] for y in range(self.num_box)]
        pass

    def addPlayer(self, username):
        self.players.append(username)

class GameClient():
    def __init__(self, num_box, player_num, socket):
        pygame.init()
        self.socket = socket
        self.player_num = player_num
        self.num_box = num_box
        self.boxSize = 60
        self.boxWidth = 4
        self.innerSize = self.boxSize - (2 * self.boxWidth)
        self.gap = self.boxWidth * 2

        width = 42 + (self.num_box * self.innerSize) + (self.num_box * self.boxWidth)
        height = width + 50

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bolonization")

        self.clock = pygame.time.Clock()

        self.boardh = [[0 for x in range(self.num_box)] for y in range(self.num_box + 1)]
        self.boardv = [[0 for x in range(self.num_box + 1)] for y in range(self.num_box)]

        # testing
        # self.boardh[4][5] = 1
        # self.boardv[6][1] = 2

        self.colorWheel = [(50, 50, 50), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 0, 255)]

    def update(self):
        # sleep to make the game 60 fps
        self.clock.tick(60)

        # clear the screen
        self.screen.fill(0)
        self.drawBoard()

        for event in pygame.event.get():
            # quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()

        # update the screen
        pygame.display.flip()

    def sendMoveInfo(self, data):
        self.socket.send(data)
        pass

    def move(self, is_horizontal, xpos, ypos):
        moved = False
        if is_horizontal and self.boardh[ypos][xpos] == 0:
            moved = True
            self.boardh[ypos][xpos] = self.player_num

            # Check upper part
            if (ypos > 0) and (xpos < self.num_box) and \
                    self.boardh[ypos-1][xpos] == self.player_num and \
                    self.boardv[ypos-1][xpos] == self.player_num and \
                    self.boardv[ypos-1][xpos+1] == self.player_num:
                print("colonized")

            #Check lower part
            if (xpos < self.num_box) and (ypos < self.num_box) and \
                    self.boardh[ypos+1][xpos] == self.player_num and \
                    self.boardv[ypos][xpos] == self.player_num and \
                    self.boardv[ypos][xpos+1] == self.player_num:
                print("colonized")
        elif not is_horizontal and self.boardv[ypos][xpos] == 0:
            moved = True
            self.boardv[ypos][xpos] = self.player_num


            # Check left part
            if (xpos > 0) and (ypos < self.num_box) and \
                    self.boardv[ypos][xpos-1] == self.player_num and \
                    self.boardh[ypos][xpos-1] == self.player_num and \
                    self.boardh[ypos + 1][xpos - 1] == self.player_num:
                print("colonized")

            # Check right part
            if (xpos < self.num_box) and (ypos < self.num_box) and \
                    self.boardv[ypos][xpos+1] == self.player_num and \
                    self.boardh[ypos][xpos] == self.player_num and \
                    self.boardh[ypos+1][xpos] == self.player_num:
                print("colonized")

        # TO DO: Send to server
        if moved:
            moveDict = {'is_horizontal': is_horizontal, 'xpos': xpos, 'ypos': ypos}
            self.sendMoveInfo(pickle.dumps(moveDict))
    def drawBoard(self):
        # Get mouse position
        mouse = pygame.mouse.get_pos()
        xpos = int(math.ceil((mouse[0] - 10 - (3 * self.boxWidth) - self.innerSize)/(self.boxWidth + self.innerSize)))
        ypos = int(math.ceil((mouse[1] - 10 - (2 * self.boxWidth) - self.innerSize)/(self.boxWidth + self.innerSize)))
        is_horizontal = abs(mouse[1] - (20 + (ypos * self.innerSize) + ((ypos-1) * self.boxWidth))) \
                        <  \
                        abs(mouse[0] - (20 + (xpos * self.innerSize) + (xpos * self.boxWidth)))

        # Vertical Lines
        for x in range(self.num_box + 1):
            for y in range(self.num_box):
                y_atas = 10 + ((y+2) * self.boxWidth) + (y * self.innerSize) + 1
                y_bawah = 10 + ((y+2) * self.boxWidth) + ((y+1) * self.innerSize)
                if(not is_horizontal) and (xpos == x) and (ypos == y) and self.boardv[ypos][xpos] == 0:
                    pygame.draw.line(self.screen, (150, 150, 150),
                                     (20 + (x * self.innerSize) + (x * self.boxWidth), y_atas),
                                     (20 + (x * self.innerSize) + (x * self.boxWidth), y_bawah),
                                     self.boxWidth)
                else:
                    pygame.draw.line(self.screen, self.colorWheel[self.boardv[y][x]],
                                 (20 + (x * self.innerSize) + (x * self.boxWidth), y_atas),
                                 (20 + (x * self.innerSize) + (x * self.boxWidth), y_bawah),
                                 self.boxWidth)
        # END Vertical Lines

        # Horizontal Lines
        for x in range(self.num_box + 1):
            for y in range(self.num_box):
                x_kiri = 10 + ((y+3) * self.boxWidth) + (y * self.innerSize) + 1
                x_kanan = 10 + ((y+3) * self.boxWidth) + ((y+1) * self.innerSize)
                if (is_horizontal) and (xpos == y) and (ypos == x) and (self.boardh[ypos][xpos] == 0):
                    pygame.draw.line(self.screen, (150, 150, 150),
                                 (x_kiri, 20 + (x * self.innerSize) + ((x-1) * self.boxWidth)),
                                 (x_kanan, 20 + (x * self.innerSize) + ((x-1) * self.boxWidth)),
                                 self.boxWidth)
                else:
                    pygame.draw.line(self.screen, self.colorWheel[self.boardh[x][y]],
                                 (x_kiri, 20 + (x * self.innerSize) + ((x-1) * self.boxWidth)),
                                 (x_kanan, 20 + (x * self.innerSize) + ((x-1) * self.boxWidth)),
                                 self.boxWidth)

        # Mouse click listener
        if pygame.mouse.get_pressed()[0]:
            self.move(is_horizontal, xpos, ypos)