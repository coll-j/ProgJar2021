import pygame

class Bolonization():
    def __init__(self):
        pygame.init()
        width, height = 378, 489
        self.boxSize = 60
        self.boxWidth = 4
        self.innerSize = self.boxSize - (2 * self.boxWidth)
        self.gap = self.boxWidth * 2

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bolonization")

        self.clock = pygame.time.Clock()

        self.boardh = [[False for x in range(6)] for y in range(7)]
        self.boardv = [[False for x in range(7)] for y in range(6)]

        # self.initGraphics()

    def initGraphics(self):
        self.normallinev = pygame.image.load("normalline.png")
        self.normallineh = pygame.transform.rotate(pygame.image.load("normalline.png"), -90)
        self.bar_donev = pygame.image.load("bar_done.png")
        self.bar_doneh = pygame.transform.rotate(pygame.image.load("bar_done.png"), -90)
        self.hoverlinev = pygame.image.load("hoverline.png")
        self.hoverlineh = pygame.transform.rotate(pygame.image.load("hoverline.png"), -90)

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

    def drawBoard(self):

        # Vertical Lines
        for x in range(7):
            for y in range(6):
                # if not self.boardv[y][x]:
                    # self.screen.blit(self.normallineh, [(x) * 64 + 5, (y) * 64])
                y_atas = 10 + ((y+2) * self.boxWidth) + (y * self.innerSize) + 1
                y_bawah = 10 + ((y+2) * self.boxWidth) + ((y+1) * self.innerSize)
                pygame.draw.line(self.screen, (50, 50, 50),
                                 (20 + (x * self.innerSize) + (x * self.boxWidth), y_atas),
                                 (20 + (x * self.innerSize) + (x * self.boxWidth), y_bawah),
                                 self.boxWidth)
                # print(y_atas, y_bawah)
                # else:
                #     self.screen.blit(self.bar_doneh, [(x) * 64 + 5, (y) * 64])
        # END Vertical Lines

        # Horizontal Lines
        for x in range(7):
            for y in range(6):
                # pass
                x_kiri = 10 + ((y+3) * self.boxWidth) + (y * self.innerSize) + 1
                x_kanan = 10 + ((y+3) * self.boxWidth) + ((y+1) * self.innerSize)
                pygame.draw.line(self.screen, (50, 50, 50),
                                 (x_kiri, 20 + (x * self.innerSize) + ((x-1) * self.boxWidth)),
                                 (x_kanan, 20 + (x * self.innerSize) + ((x-1) * self.boxWidth)),
                                 self.boxWidth)
                # print(x_kiri, x_kanan)
        #         if not self.boardv[y][x]:
        #             self.screen.blit(self.normallinev, [(x) * 64, (y) * 64 + 5])
        #         else:
        #             self.screen.blit(self.bar_donev, [(x) * 64, (y) * 64 + 5])
