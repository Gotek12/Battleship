#!/usr/bin/python3
# -*- coding: iso-8859-2 -*-
import pygame
from enum import Enum

# Define some colors
pygame.init()
SIZE = 10

# tymczasowe wyświetlanie
size = (920, 510)
screen = pygame.display.set_mode(size)
# ustawienia kafelka
width = 40
height = 40
margin = 2
clock = pygame.time.Clock()

class BoxOpt(Enum):
    SHIP = [False, True]    # czy statek
    HIT = [False, True]   # czy trafiony
    WRECK = [False, True]  # czy zatopiony
    SET = [False, True]  # czy można go tu ustawić

class Color(Enum):
    BLACK = (0, 0, 0)  # gdy najedziemy myszką
    WHITE = (255, 255, 255)  # morze
    GREEN = (0, 255, 0)  # można dodać
    RED = (255, 0, 0)  # nie można dodać, trafiony
    BLUE = (30, 144, 255)  # nie trafiony
    BLUEDED = (20, 164, 225)  # cały statek zatopiony
    SHIPCOLOR = (148, 148, 135)  # statek

class Box:

    def __init__(self, x, y, who, add):
        self.width = 40
        self.add= add
        self.height = 40
        self.pos = [x, y]
        self.who = who  # czy gracz, czy przeciwnik
        self.settings = [
            BoxOpt.SHIP.value[0],
            BoxOpt.HIT.value[0],
            BoxOpt.WRECK.value[0],
            BoxOpt.SET.value[0]
        ]

    # rysowanie pojedynczego kafelka
    def draw(self, screen, color):
        pygame.draw.rect(screen, color, [self.add + margin + (margin + self.width) * self.pos[1], margin + (margin + self.height) * self.pos[0], self.width, self.height])

    # rysowanie kafelka w zależności od opcji
    def drawBox(self, screen, over = False):

        if over:
            self.draw(screen, Color.BLACK.value)
        elif self.settings[0]:
            if self.settings[2]:
                self.draw(screen, Color.BLUEDED.value)
            elif self.settings[1]:
                self.draw(screen, Color.RED.value)
            elif self.settings[3]:
                self.draw(screen, Color.SHIPCOLOR.value)
        else:
            if self.settings[1]:
                self.draw(screen, Color.BLUE.value)



class GameBoard:

    def __init__(self, add = 0, who = 0):
        # pusta tablica 2d
        self.board = [[0 for x in range(SIZE)] for y in range(SIZE)]
        self.add = add
        self.who = who

        #  tworzenie pustej planszy 10x10
        for i in range(SIZE):
            for j in range(SIZE):
                color = Color.WHITE.value
                box = Box(i, j, who, add)
                self.board[i][j] = box
                box.drawBox(screen)
                # pygame.draw.rect(screen, color,
                #              [margin + (margin + width) * j, margin + (margin + height) * i, width,
                #               height])


    # tymczasowa funkcja odpalająca grida
    def run(self):
        while True:
            for event in pygame.event.get():
                # zamykamy program
                if event.type == pygame.QUIT:
                    print("End game")
                    exit()

                # obsługa klikania
                if event.type == pygame.MOUSEBUTTONDOWN:
                    column = pos[0] // (width + margin)
                    row = pos[1] // (height + margin)
                    print("Click ", pos, "Grid coordinates: ", row, column)
                    self.board[row][column] = 1

            # --- Game logic should go here
            # pobieranie pozycji
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]

            #czyszczenie obrazu
            screen.fill(Color.BLACK.value)

            # update 2d array
            for i in range(SIZE):
                for j in range(SIZE):
                    if self.board[i][j] == 1:
                        color = Color.GREEN.value
                    else:
                        color = Color.WHITE.value
                    pygame.draw.rect(screen, color,
                                     [margin + (margin + width) * j, margin + (margin + height) * i, width,
                                      height])

                    # odświeżanie ekranu
            pygame.display.flip()
            clock.tick(60)

g = GameBoard()
while True:
    g.run()

