# coding=utf-8
import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ch = False
pygame.init()

# Set the width and height of the screen [width, height]
size = (915, 510)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Statki")

size = 40
margin = 5

grid = [[0 for x in range(10)] for y in range(10)]
grid2 = [[0 for x in range(10)] for y in range(10)]


class Box:
    def __init__(self, x, y, screen, add = 0, color = WHITE):
        self.id = str(x) + " " + str(y)
        self.x = x
        self.y = y
        self.screen = screen
        self.color = color
        self.add = add

    def draw(self, focus=False, color = WHITE):
        # if focus:
        #     pygame.draw.rect(self.screen, RED,
        #                      [self.add + margin + (margin + size) * self.y, margin + (margin + size) * self.x, size,
        #                       size])
        # else:
        pygame.draw.rect(self.screen, self.color,
                             [self.add + margin + (margin + size) * self.y, margin + (margin + size) * self.x, size,
                              size])



def draw(screen, g, foc, add=0):
    for row in range(10):
        for column in range(10):
            # if g[row][column] == 1:
            #     color = GREEN
            # elif g[row][column] == 2:
            #     color = RED
            # else:
            #     color = WHITE
            box = Box(row, column, screen, add)
            g[row][column] = box
            box.draw(foc)


# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Limit to 60 frames per second
    clock.tick(60)
    foc2 = False
    foc = False

    # --- Main event loop
    for event in pygame.event.get():  # User did something
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        column = pos[0] // (size + margin)
        row = pos[1] // (size + margin)
        if pos[0] > 460:
            column = (pos[0] - 460) // (size + margin)

        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pos[0] > 460:
                print("Click grid2", pos, "Grid coordinates: ", row, column)
                print(grid2[row][column].id)
                print(grid2[row][column].color)

            else:
                print("Click grid1", pos, "Grid coordinates: ", row, column)
                # grid[row][column] = 1

        elif event.type == pygame.MOUSEMOTION:

            if 0 < pos[0] < 910 and 0 < pos[1] < 450:

                if pos[0] < 450 or pos[0] > 460:
                    if pos[0] > 460:
                        # foc2 = True
                        print("Over grid2", pos, "Grid coordinates: ", row, column)
                    else:
                        # foc = True
                        print("Over grid1", pos, "Grid coordinates: ", row, column)

    screen.fill(BLACK)

    draw(screen, grid, foc)
    draw(screen, grid2, foc2, 460)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Close the window and quit.
pygame.quit()

# stworzyć klasę gameboard
# następnie tworzymy 2 gamebordy i w pętli gry je odświerzamy całe gamebordy które każda z osobna generuje kwadraty