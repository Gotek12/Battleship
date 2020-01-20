# coding=utf-8
import pygame

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


class Box:
    def __init__(self, x, y, add=0):
        self.id = str(x) + " " + str(y)
        self.x = x
        self.y = y
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


p1 = GameBoard(0)
p2 = GameBoard(460)

lastPosition = [-1, -1]

def main():
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
                    p2.grid[row][column].color = RED

            elif event.type == pygame.MOUSEMOTION:
                # test for multiple stat
                if 0 < pos[0] < 910 and 0 < pos[1] < 450:
                    if pos[0] < 450 or pos[0] > 460:
                        if pos[0] > 460:
                            print(row, column)
                            if lastPosition[0] == row and lastPosition[1] == column:
                                p2.grid[row][column].foc = True

                                if row + 1 <= 9:
                                    p2.grid[row+1][column].foc = True
                            else:

                                p2.grid[lastPosition[0]][lastPosition[1]].foc = False
                                if row + 1 < 9:
                                    p2.grid[lastPosition[0]+1][lastPosition[1]].foc = False

                                lastPosition = [row, column]
                else:  # do poprawy
                    if lastPosition[0] != -1 and lastPosition[1] != -1:
                        p2.grid[lastPosition[0]][lastPosition[1]].foc = False
                        lastPosition = [-1, -1]
                # if 0 < pos[0] < 910 and 0 < pos[1] < 450:
                #     if pos[0] < 450 or pos[0] > 460:
                #         if pos[0] > 460:
                #             if lastPosition[0] == row and lastPosition[1] == column:
                #                 p2.grid[row][column].foc = True
                #             else:
                #                 p2.grid[lastPosition[0]][lastPosition[1]].foc = False
                #                 lastPosition = [row, column]
                # else:  # do poprawy
                #     if lastPosition[0] != -1 and lastPosition[1] != -1:
                #         p2.grid[lastPosition[0]][lastPosition[1]].foc = False
                #         lastPosition = [-1, -1]





        screen.fill(BLACK)
        p1.draw(screen)
        p2.draw(screen)

        pygame.display.update()

    pygame.quit()


main()
