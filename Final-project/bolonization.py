import pygame
import math

class Bolonization():
    def __init__(self, num_box):
        pygame.init()
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
        mouse = pygame.mouse.get_pos()
        xpos = int(math.ceil((mouse[0] - 10 - (3 * self.boxWidth) - self.innerSize)/(self.boxWidth + self.innerSize)))
        ypos = int(math.ceil((mouse[1] - 10 - (2 * self.boxWidth) - self.innerSize)/(self.boxWidth + self.innerSize)))
        is_horizontal = abs(mouse[1] - (20 + (ypos * self.innerSize) + ((ypos-1) * self.boxWidth))) \
                        <  \
                        abs(mouse[0] - (20 + (xpos * self.innerSize) + (xpos * self.boxWidth)))
        self.drawBoard(xpos, ypos, is_horizontal)

        for event in pygame.event.get():
            # quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()

        # update the screen
        pygame.display.flip()

    def drawBoard(self, xpos, ypos, is_horizontal):

        # Vertical Lines
        for x in range(self.num_box + 1):
            for y in range(self.num_box):
                y_atas = 10 + ((y+2) * self.boxWidth) + (y * self.innerSize) + 1
                y_bawah = 10 + ((y+2) * self.boxWidth) + ((y+1) * self.innerSize)
                if(not is_horizontal) and (xpos == x) and (ypos == y):
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
                if (is_horizontal) and (xpos == y) and (ypos == x):
                    pygame.draw.line(self.screen, (150, 150, 150),
                                 (x_kiri, 20 + (x * self.innerSize) + ((x-1) * self.boxWidth)),
                                 (x_kanan, 20 + (x * self.innerSize) + ((x-1) * self.boxWidth)),
                                 self.boxWidth)
                else:
                    pygame.draw.line(self.screen, self.colorWheel[self.boardh[x][y]],
                                 (x_kiri, 20 + (x * self.innerSize) + ((x-1) * self.boxWidth)),
                                 (x_kanan, 20 + (x * self.innerSize) + ((x-1) * self.boxWidth)),
                                 self.boxWidth)