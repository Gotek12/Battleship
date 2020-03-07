#!/usr/bin/python3
# -*- coding: iso-8859-2 -*-
import pygame
import os

class Menu():
    width = 500
    height = 500
    white = (255, 255, 255)
    dark = (0, 0, 0)
    blue = (0, 0, 255)

    def __init__(self):
        pygame.init()
        # ustawienie parametrów ekranu
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(" Statki")
        self.screen.fill(self.white)

        ico = pygame.image.load("images/ship_icon.png")
        pygame.display.set_icon(ico)

        # ustawiamy zegar gry
        self.clock = pygame.time.Clock()

    def menu(self):
        font = pygame.font.SysFont('Arial', 70)
        gameName = font.render("STATKI", True, self.dark)
        self.screen.blit(gameName, (150, 100))

        font1 = pygame.font.SysFont('Arial', 35)
        playBtn = font1.render("Graj", True, self.white)
        zasadyBtn = font1.render("Zasady", True, self.white)
        netBtn = font1.render("Siec lokalna", True, self.white)
        net2Btn = font1.render("Siec globalna", True, self.white)

        rec1 = pygame.draw.rect(self.screen, self.blue, (155, 200, 170, 50))  # left, top, width, height
        rec2 = pygame.draw.rect(self.screen, self.blue, (155, 270, 170, 50))
        rec3 = pygame.draw.rect(self.screen, self.blue, (155, 330, 170, 50))
        rec4 = pygame.draw.rect(self.screen, self.blue, (155, 390, 170, 50))

        self.screen.blit(playBtn, (205, 205))
        self.screen.blit(zasadyBtn, (190, 275))
        self.screen.blit(netBtn, (160, 335))
        self.screen.blit(net2Btn, (155, 395))

        return [rec1, rec2, rec3, rec4]

    def zasady(self):
        font = pygame.font.SysFont('Arial', 50)
        gameName = font.render("ZASADY", True, self.dark)
        self.screen.blit(gameName, (170, 40))

        font1 = pygame.font.SysFont('Arial', 35)
        playBtn = font1.render("MENU", True, self.white)
        rec1 = pygame.draw.rect(self.screen, self.blue, (160, 450, 170, 50))
        self.screen.blit(playBtn, (205, 455))

        opis = ["Gra planszowa dla 2 osób. Każda osoba posiada 2",
                "planszę 10 x 10. Kolumny opisujemy literami",
                "alfabetu od a od j, a wiersze cyframi od 1 do 10.",
                "Na jednej zaznaczamy swoje statki, a na drugiej",
                "statki przeciwnika.",
                "                                               ",
                "Każda osoba posiada:                           ",
                "- 4 jednomasztwoce",
                "- 3 dwumasztowce",
                "- 2 trzymasztowce,",
                "- 1 czteromasztowiec"]

        for i in range(len(opis)):
            fontTxt = pygame.font.SysFont('Arial', 20)
            t = fontTxt.render(opis[i], True, self.dark)
            self.screen.blit(t, (90, 120 + i*20))
        return rec1

    def welcome(self):
        ifMenu = True
        menu = self.menu()
        zasadyBt = None

        run_menu = True
        while run_menu:

            for event in pygame.event.get():
                # zamykamy program
                if event.type == pygame.QUIT:
                    print("End game")
                    exit()

                # obsługa menu
                if event.type == pygame.MOUSEBUTTONDOWN:
                    xPos, yPos = event.pos
                    if menu[0].collidepoint((xPos, yPos)) and ifMenu:
                        print("Graj")
                        pygame.display.iconify()
                        os.system("python3 gameBoard.py")
                        run_menu = False

                    if menu[1].collidepoint((xPos, yPos)) and ifMenu:
                        ifMenu = False
                        print("Zasady")
                        self.screen.fill(self.white)
                        zasadyBt = self.zasady()

                    if menu[2].collidepoint((xPos, yPos)) and ifMenu:
                        print("Siec lokalna")

                    if menu[3].collidepoint((xPos, yPos)) and ifMenu:
                        print("Siec globalna")

                    if not zasadyBt is None:
                        if zasadyBt.collidepoint((xPos, yPos)):
                            print("Powrót do menu")
                            self.screen.fill(self.white)
                            menu = self.menu()
                            ifMenu = True

            # aktualizacja całego ekranu
            pygame.display.update()

game = Menu()
while True:
    game.welcome()
