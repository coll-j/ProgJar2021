import pickle
import sys

import pygame
import math

class GameServer():
    def __init__(self, num_box):
        self.players = []
        self.num_box = num_box
        self._turn = 1

        self.boardh = [[0 for x in range(self.num_box)] for y in range(self.num_box + 1)]
        self.boardv = [[0 for x in range(self.num_box + 1)] for y in range(self.num_box)]
        pass

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, turn):
        self._turn = turn % (len(self.getPlayer()) + 1)
        self._turn = 1 if self._turn == 0 else self._turn

    def removePlayer(self, username):
        self.players.remove(username)

    def addPlayer(self, username):
        self.players.append(username)

    def getPlayer(self):
        return self.players

    def getBoard(self):
        return {'boardh': self.boardh, 'boardv': self.boardv}

    def updateBoard(self, moveDict):
        is_horizontal = moveDict['is_horizontal']
        ypos = moveDict['ypos']
        xpos = moveDict['xpos']
        player_num = moveDict['player_num']
        moved = False
        if is_horizontal and self.boardh[ypos][xpos] == 0:
            moved = True
            self.boardh[ypos][xpos] = player_num

            # Check upper part
            if (ypos > 0) and (xpos < self.num_box) and \
                    self.boardh[ypos-1][xpos] == player_num and \
                    self.boardv[ypos-1][xpos] == player_num and \
                    self.boardv[ypos-1][xpos+1] == player_num:
                print("colonized")

            #Check lower part
            if (xpos < self.num_box) and (ypos < self.num_box) and \
                    self.boardh[ypos+1][xpos] == player_num and \
                    self.boardv[ypos][xpos] == player_num and \
                    self.boardv[ypos][xpos+1] == player_num:
                print("colonized")
        elif not is_horizontal and self.boardv[ypos][xpos] == 0:
            moved = True
            self.boardv[ypos][xpos] = player_num


            # Check left part
            if (xpos > 0) and (ypos < self.num_box) and \
                    self.boardv[ypos][xpos-1] == player_num and \
                    self.boardh[ypos][xpos-1] == player_num and \
                    self.boardh[ypos + 1][xpos - 1] == player_num:
                print("colonized")

            # Check right part
            if (xpos < self.num_box) and (ypos < self.num_box) and \
                    self.boardv[ypos][xpos+1] == player_num and \
                    self.boardh[ypos][xpos] == player_num and \
                    self.boardh[ypos+1][xpos] == player_num:
                print("colonized")

        return moved

class GameClient():
    def __init__(self, num_box, player_num):
        pygame.init()
        print("creating game...")
        self.is_running = True
        self._turn = 1
        self.moved = False
        self.player_num = player_num
        self.num_box = num_box
        self.boxSize = 60
        self.boxWidth = 4
        self.innerSize = self.boxSize - (2 * self.boxWidth)
        self.gap = self.boxWidth * 2
        self.moveDict = {}

        width = 42 + (self.num_box * self.innerSize) + (self.num_box * self.boxWidth)
        height = width + 50

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bolonization")

        self.clock = pygame.time.Clock()

        self.boardh = [[0 for x in range(self.num_box)] for y in range(self.num_box + 1)]
        self.boardv = [[0 for x in range(self.num_box + 1)] for y in range(self.num_box)]

        self.colorWheel = [(50, 50, 50), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 0, 255)]
        print("game created")

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, turn):
        self._turn = turn % (len(self.getPlayer()) + 1)
        self._turn = 1 if self._turn == 0 else self._turn

    def hasMoved(self):
        return self.moved

    def setMoved(self, moved):
        self.moved = moved

    def update(self):
        # sleep to make the game 60 fps
        self.clock.tick(60)

        # clear the screen
        self.screen.fill(0)
        self.drawBoard()

        for event in pygame.event.get():
            # quit if the quit button was pressed
            if event.type == pygame.QUIT:
                self.is_running = False
                # exit()
                # sys.exit(0)

        # update the screen
        pygame.display.flip()

    def isRunning(self):
        return self.is_running

    def move(self, is_horizontal, xpos, ypos):
        moveDict = {'is_horizontal': is_horizontal, 'xpos': xpos, 'ypos': ypos, 'player_num': self.player_num}
        self.moveDict = moveDict
        self.moved = True

    def getMove(self):
        return pickle.dumps(self.moveDict)

    def updateBoard(self, data):
        data = pickle.loads(data)
        self._turn = data['turn']
        self.boardh = data['boardh']
        self.boardv = data['boardv']

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
            if self.player_num == self._turn:
                self.move(is_horizontal, xpos, ypos)