#!/usr/bin/python3
# -*- coding: iso-8859-2 -*-
# Prototyp

import pygame
import random
from enum import Enum

pygame.init()
size = (915, 510)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Statki")
ico = pygame.image.load("images/ship_icon.png")
pygame.display.set_icon(ico)

lastPosition = [-1, -1]
SI = 40
MARGIN = 5


class Game:
    def __init__(self):
        self.initGraphics()
        self.screen = screen

    def loadMusic(self):
        pygame.mixer.music.load('sounds/Ship.ogg')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def crashed(self):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/bang.ogg'))
        pygame.mixer.Channel(0).set_volume(0.8)

    def initGraphics(self):
        self.winningscreen = pygame.image.load("images/youwin.png")
        self.gameover = pygame.image.load("images/gameover.png")

    def finish(self, what):
        screen.fill(Color.BLACK.value)
        if what:
            self.screen.blit(self.winningscreen, (272, 0))
            pygame.mixer.music.load('sounds/win.ogg')
            pygame.mixer.music.play(-1)
        else:
            self.screen.blit(self.gameover, (272, 0))
            pygame.mixer.music.load('sounds/over.ogg')
            pygame.mixer.music.play(-1)
        pygame.display.flip()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()


setti = Game()
setti.loadMusic()


# Define some colors
class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (30, 144, 255)
    BLUEDED = (20, 164, 225)
    INNY = (123, 23, 34)


class Box:
    def __init__(self, x, y, add=0):
        self.id = str(x) + " " + str(y)
        self.x = x
        self.y = y
        self.blocked = False
        self.color = Color.WHITE.value
        self.add = add
        self.sunk = False  # zatopiony
        self.foc = False  # focused
        self.clicked = False

    def draw(self, screen, focus=False):
        if self.foc:
            pygame.draw.rect(screen, Color.BLACK.value,
                             [self.add + MARGIN + (MARGIN + SI) * self.y, MARGIN + (MARGIN + SI) * self.x, SI,
                              SI])
        else:
            pygame.draw.rect(screen, self.color,
                             [self.add + MARGIN + (MARGIN + SI) * self.y, MARGIN + (MARGIN + SI) * self.x, SI,
                              SI])


class GameBoard():
    def __init__(self, add, op=False):
        self.opponent = op
        self.grid = [[None for x in range(10)] for x in range(10)]
        self.screen = screen
        self.add = add
        self.counter = 0
        self.shipsDictionary = {
            "1": 4,
            "2": 3,
            "3": 2,
            "4": 1
        }
        self.tabE = []

        for x, y in self.shipsDictionary.items():
            for i in range(int(x)):
                self.tabE.append(y)
        self.tabE.append(-1)

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
            randX = random.randint(0, 9)
            randY = random.randint(0, 9)

            if not self.grid[randX][randY].clicked:
                if self.grid[randX][randY].blocked and not self.grid[randX][randY].sunk:
                    self.grid[randX][randY].sunk = True
                    self.grid[randX][randY].clicked = True
                    self.grid[randX][randY].color = Color.INNY.value
                    self.counter = self.counter + 1
                    print("bum", self.counter)
                    break
                else:
                    self.grid[randX][randY].color = Color.BLACK.value
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
                            # self.grid[randX + i][randY].color = Color.RED.value
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
                            # self.grid[randX][randY + i].color = Color.RED.value
                        total = total + 1
                        break


p1 = GameBoard(0, True)
p2 = GameBoard(460)

# przenieść logikę do klas
def main():
    p1.randomShips(p1.tabE)

    can = True
    iterator = 0

    global lastPosition
    done = False
    clock = pygame.time.Clock()
    rot_yes_no = False

    while not done:
        clock.tick(60)

        # --- Main event loop
        for event in pygame.event.get():  # User did something
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            column = pos[0] // (SI + MARGIN)
            row = pos[1] // (SI + MARGIN)
            if pos[0] > 460:
                column = (pos[0] - 460) // (SI + MARGIN)

            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pos[0] > 460:

                    # can działa gdy foc jest ok
                    if can and p1.tabE[iterator] != -1:

                        yes = True
                        # sprawdza czy na dane miejsce moge dodać element
                        for i in range(p1.tabE[iterator]):

                            if not rot_yes_no:

                                if not p2.grid[row + i][column].blocked:
                                    yes = False
                                    can = False
                                else:
                                    yes = True
                                    can = False
                                    break
                            else:

                                if not p2.grid[row][column + i].blocked:
                                    yes = False
                                    can = False
                                else:
                                    yes = True
                                    can = False
                                    break

                        print(yes)

                        # jeśli moge to dodaje
                        if not yes:

                            for i in range(p1.tabE[iterator]):
                                if not rot_yes_no:
                                    p2.grid[row + i][column].foc = False
                                    p2.grid[row + i][column].blocked = True
                                    p2.grid[row + i][column].color = Color.RED.value
                                else:
                                    p2.grid[row][column+i].foc = False
                                    p2.grid[row][column+i].blocked = True
                                    p2.grid[row][column+i].color = Color.RED.value
                            iterator = iterator + 1
                            can = False

                # gdy dodam wszystkie el i tabE[] == -1 to odblokowuje lewą tarcze
                if pos[0] < 450 and p1.tabE[iterator] == -1:
                    if not p1.grid[row][column].clicked:
                        p1.grid[row][column].clicked = True
                        if p1.grid[row][column].blocked:
                            p1.grid[row][column].color = Color.INNY.value
                            p1.grid[row][column].sunk = True
                            p1.counter = p1.counter + 1
                            print(p1.counter)
                            setti.crashed()
                        else:
                            p1.grid[row][column].color = Color.BLACK.value

                        # wywołuje kod przeciwnika
                        p2.bang()

                        if p1.counter == 20:
                            print("Wygrales")
                            setti.finish(True)
                        if p2.counter == 20:
                            print("Przegrales")
                            setti.finish(False)



            elif event.type == pygame.MOUSEMOTION:
                # test for multiple stat
                if 0 < pos[0] < 910 and 0 < pos[1] < 450:
                    if pos[0] < 450 or pos[0] > 460:

                        # pierwsza tablica - tablica przeciwnika
                        if pos[0] < 450 and p2.tabE[iterator] == -1:
                            if lastPosition[0] == row and lastPosition[1] == column:
                                p1.grid[row][column].foc = True
                            else:
                                p1.grid[lastPosition[0]][lastPosition[1]].foc = False
                                lastPosition = [row, column]

                        # druga tablica - moja tablica
                        if pos[0] > 460:

                            if not rot_yes_no:
                                if lastPosition[0] == row and lastPosition[1] == column:

                                    if row + p2.tabE[iterator] <= 10:
                                        can = True
                                        for i in range(p2.tabE[iterator]):
                                            p2.grid[row + i][column].foc = True
                                    else:
                                        for i in range(p2.tabE[iterator]):
                                            if i + row < 10:
                                                p2.grid[row + i][column].foc = True
                                        can = False
                                else:
                                    p2.grid[lastPosition[0]][lastPosition[1]].foc = False
                                    if row + p2.tabE[iterator] < 10:
                                        for i in range(p2.tabE[iterator]):
                                            if i + row < 10:
                                                p2.grid[lastPosition[0] + i][lastPosition[1]].foc = False

                                    lastPosition = [row, column]

                            else:
                                if lastPosition[0] == row and lastPosition[1] == column:

                                    if column + p2.tabE[iterator] <= 10:
                                        can = True
                                        for i in range(p2.tabE[iterator]):
                                            p2.grid[row][column + i].foc = True
                                    else:
                                        for i in range(p2.tabE[iterator]):
                                            if i + column < 10:
                                                p2.grid[row][column + i].foc = True
                                        can = False
                                else:
                                    p2.grid[lastPosition[0]][lastPosition[1]].foc = False
                                    if column + p2.tabE[iterator] < 10:
                                        for i in range(p2.tabE[iterator]):
                                            if i + column < 10:
                                                p2.grid[lastPosition[0]][lastPosition[1] + i].foc = False

                                    lastPosition = [row, column]

                else:  # do poprawy
                    if lastPosition[0] != -1 and lastPosition[1] != -1:
                        # p2.grid[lastPosition[0]][lastPosition[1]].foc = False # nie jest potrzebne
                        lastPosition = [-1, -1]

            #  klawisz
            if event.type == pygame.KEYDOWN:
                if event.key == 114:
                    print("rotate")
                    if rot_yes_no:
                        rot_yes_no = False
                        p2.grid[lastPosition[0]][lastPosition[1]].foc = False
                        if column + p2.tabE[iterator] < 10:
                            for i in range(p2.tabE[iterator]):
                                if i + column < 10:
                                    p2.grid[lastPosition[0]][lastPosition[1] + i].foc = False

                        lastPosition = [row, column]
                    else:
                        rot_yes_no = True
                        p2.grid[lastPosition[0]][lastPosition[1]].foc = False
                        if row + p2.tabE[iterator] < 10:
                            for i in range(p2.tabE[iterator]):
                                if i + row < 10:
                                    p2.grid[lastPosition[0] + i][lastPosition[1]].foc = False

                        lastPosition = [row, column]

        # screen update
        screen.fill(Color.BLACK.value)
        # draw player1/2 gameboard
        p1.draw(screen)  # przeciwnik
        p2.draw(screen)

        pygame.display.flip()

    pygame.quit()


main()
