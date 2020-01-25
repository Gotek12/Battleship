# coding=utf-8
import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
pygame.init()
size = (915, 510)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Statki")

si = 40
margin = 5

shipsDictionary = {
    "1": 4,
    "2": 3,
    "3": 2,
    "4": 1
}


class Ship:
    def __init__(self, sizeS, x, y, x2, y2, position="vertical"):
        self.id = sizeS * x * y
        self.sizeS = sizeS  # size of ship
        self.x = x  # start position
        self.y = y
        self.x2 = x2  # end position
        self.y2 = y2
        self.blocked = False
        self.position = position  # horizontal/vertical


class Box:
    def __init__(self, x, y, add=0):
        self.id = str(x) + " " + str(y)
        self.x = x
        self.y = y
        self.blocked = False
        self.color = WHITE
        self.add = add
        self.foc = False

    def draw(self, screen, focus=False):
        if self.foc:
            pygame.draw.rect(screen, BLACK,
                             [self.add + margin + (margin + si) * self.y, margin + (margin + si) * self.x, si,
                              si])
        else:
            pygame.draw.rect(screen, self.color,
                             [self.add + margin + (margin + si) * self.y, margin + (margin + si) * self.x, si,
                              si])


class GameBoard():
    def __init__(self, add):
        self.grid = [[None for x in range(10)] for x in range(10)]
        self.screen = screen
        self.add = add

        for row in range(10):
            for column in range(10):
                box = Box(row, column, self.add)
                self.grid[row][column] = box

    def draw(self, screen):
        for row in range(10):
            for column in range(10):
                self.grid[row][column].draw(screen)

    def randomShips(self):
        # rgedon

        while True:
            randX = random.randrange(0, 9, 1)
            randY = random.randrange(0, 9, 1)


p1 = GameBoard(0)
p2 = GameBoard(460)
lastPosition = [-1, -1]
tabE = []
for x, y in shipsDictionary.items():
    for i in range(int(x)):
        tabE.append(y)
tabE.append(-1)


def main():
    # read how many ships must add
    # total = 10
    for i in range(len(tabE)):
        print(tabE[i])

    can = True
    canSize = 0
    iterator = 0

    global lastPosition
    done = False
    clock = pygame.time.Clock()
    while not done:
        clock.tick(60)
        # --- Main event loop
        for event in pygame.event.get():  # User did something
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            column = pos[0] // (si + margin)
            row = pos[1] // (si + margin)
            if pos[0] > 460:
                column = (pos[0] - 460) // (si + margin)

            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pos[0] > 460:

                    if can and tabE[iterator] != -1:

                        yes = True
                        for i in range(tabE[iterator]):
                            if not p2.grid[row + i][column].blocked:
                                yes = False
                                can = False
                                break

                        if not yes:
                            for i in range(tabE[iterator]):
                                p2.grid[row + i][column].foc = False
                                p2.grid[row + i][column].blocked = True
                                p2.grid[row + i][column].color = RED
                            iterator = iterator + 1
                            can = False

                if pos[0] < 450 and tabE[iterator] == -1:
                    p1.grid[row][column].color = GREEN

            elif event.type == pygame.MOUSEMOTION:
                # test for multiple stat
                if 0 < pos[0] < 910 and 0 < pos[1] < 450:
                    if pos[0] < 450 or pos[0] > 460:

                        # pierwsza tablica
                        if pos[0] < 450 and tabE[iterator] == -1:
                            if lastPosition[0] == row and lastPosition[1] == column:
                                p1.grid[row][column].foc = True
                            else:
                                p1.grid[lastPosition[0]][lastPosition[1]].foc = False
                                lastPosition = [row, column]

                        # druga tablica
                        if pos[0] > 460:
                            print(row, column)

                            if lastPosition[0] == row and lastPosition[1] == column:

                                if row + tabE[iterator] <= 10:
                                    can = True
                                    for i in range(tabE[iterator]):
                                        p2.grid[row + i][column].foc = True
                                else:
                                    for i in range(tabE[iterator]):
                                        if i + row < 10:
                                            p2.grid[row + i][column].foc = True
                                    can = False
                            else:
                                p2.grid[lastPosition[0]][lastPosition[1]].foc = False
                                if row + tabE[iterator] < 10:
                                    for i in range(tabE[iterator]):
                                        if i + row < 10:
                                            p2.grid[lastPosition[0] + i][lastPosition[1]].foc = False

                                lastPosition = [row, column]

                else:  # do poprawy
                    if lastPosition[0] != -1 and lastPosition[1] != -1:
                        p2.grid[lastPosition[0]][lastPosition[1]].foc = False
                        lastPosition = [-1, -1]

        # screen update
        screen.fill(BLACK)
        # draw player1/2 gameboard
        p1.draw(screen)
        p2.draw(screen)

        pygame.display.flip()

    pygame.quit()


main()
