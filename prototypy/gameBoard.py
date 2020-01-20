import pygame
import os


class Menu():
    width = 800
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


    def main(self):
        while True:

            for event in pygame.event.get():
                # zamykamy program
                if event.type == pygame.QUIT:
                    print("End game")
                    exit()

            # aktualizacja całego ekranu
            pygame.display.update()


game = Menu()
while True:
    game.main()
