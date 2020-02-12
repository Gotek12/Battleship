# coding=utf-8
import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
INNY = (123, 23, 34)
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


class Box:
    def __init__(self, x, y, add=0):
        self.id = str(x) + " " + str(y)
        self.x = x
        self.y = y
        self.blocked = False
        self.color = WHITE
        self.add = add
        self.sunk = False  # zatopiony
        self.foc = False  # focused
        self.clicked = False

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
        self.counter = 0

        for row in range(10):
            for column in range(10):
                box = Box(row, column, self.add)
                self.grid[row][column] = box

    def draw(self, screen):
        for row in range(10):
            for column in range(10):
                self.grid[row][column].draw(screen)

    def bang(self):
        while True:
            randX = random.randint(0,9)
            randY = random.randint(0,9)

            if not self.grid[randX][randY].clicked:
                if self.grid[randX][randY].blocked and not self.grid[randX][randY].sunk:
                    self.grid[randX][randY].sunk = True
                    self.grid[randX][randY].clicked = True
                    self.grid[randX][randY].color = INNY
                    self.counter = self.counter + 1
                    print("bum", self.counter)
                    break
                else:
                    self.grid[randX][randY].color = BLACK
                    self.grid[randX][randY].clicked = True
                    print("o nie")
                    break

    def randomShips(self, tabE):
        # read how many ships must add
        # total = 10
        # generujemy statki dla p1
        total = 0  # jeśli 10 to koniec
        while True:
            if total == 10:
                break
            siz = tabE[total]  # wielkości statków do ustawienia
            zeroOrOne = random.randrange(0, 2, 1)

            # losowanie poło
            while True:
                randX = random.randrange(0, 9, 1)
                randY = random.randrange(0, 9, 1)

                if zeroOrOne == 0 and randX + siz < 10:
                    can2 = False
                    for i in range(siz):
                        if not self.grid[randX + i][randY].blocked:
                            can2 = True
                        else:
                            can2 = False
                            break

                    if can2:
                        for i in range(siz):
                            self.grid[randX + i][randY].blocked = True
                            self.grid[randX + i][randY].color = RED
                        total = total + 1
                        break

                if zeroOrOne == 1 and randY + siz < 10:
                    can2 = False
                    for i in range(siz):
                        if not self.grid[randX][randY + i].blocked:
                            can2 = True
                        else:
                            can2 = False
                            break

                    if can2:
                        for i in range(siz):
                            self.grid[randX][randY + i].blocked = True
                            self.grid[randX][randY + i].color = RED
                        total = total + 1
                        break


p1 = GameBoard(0)
p2 = GameBoard(460)
lastPosition = [-1, -1]
tabE = []
for x, y in shipsDictionary.items():
    for i in range(int(x)):
        tabE.append(y)
tabE.append(-1)

# przenieść logikę do klas
def main():
    p1.randomShips(tabE)

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

                    # can działa gdy foc jest ok
                    if can and tabE[iterator] != -1:

                        yes = True
                        # sprawdza czy na dane miejsce moge dodać element
                        for i in range(tabE[iterator]):
                            if not p2.grid[row + i][column].blocked:
                                yes = False
                                can = False
                            else:
                                yes = True
                                can = False
                                break

                        # jeśli moge to dodaje
                        if not yes:
                            for i in range(tabE[iterator]):
                                p2.grid[row + i][column].foc = False
                                p2.grid[row + i][column].blocked = True
                                p2.grid[row + i][column].color = RED
                            iterator = iterator + 1
                            can = False

                # gdy dodam wszystkie el i tabE[] == -1 to odblokowuje lewą tarcze
                if pos[0] < 450 and tabE[iterator] == -1:
                    if not p1.grid[row][column].clicked:
                        p1.grid[row][column].clicked = True
                        if p1.grid[row][column].blocked:
                            p1.grid[row][column].color = INNY
                            p1.grid[row][column].sunk = True
                            p1.counter = p1.counter + 1
                            print(p1.counter)
                        else:
                            p1.grid[row][column].color = BLACK

                        # wywołuje kod przeciwnika
                        p2.bang()

                        if p1.counter == 20:
                            print("Wygrales")
                        if p2.counter == 20:
                            print("Przegrales")


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
        p1.draw(screen)  # przeciwnik
        p2.draw(screen)

        pygame.display.flip()

    pygame.quit()


main()
