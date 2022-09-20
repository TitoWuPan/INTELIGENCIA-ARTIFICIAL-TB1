from operator import truediv
from pygame import display, time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w
from random import randint
import pygame
from numpy import sqrt
from tkinter import messagebox

def star():
    done = False
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    cols = 50
    rows = 50

    width = 600
    height = 600
    wr = width/cols
    hr = height/rows
    direction = 1

    screen = display.set_mode([width, height])
    display.set_caption("Snake IA")
    clock = time.Clock()


    def getpath(food1, snake1):
    ##
    #It takes a food and a snake as input, and returns a list of directions that the snake should take to
    #get to the food
    
    #:param food1: the food object
    #:param snake1: the snake
    #:return: The path from the snake's head to the food.
    #
    # Setting the camefrom attribute of the food object to an empty list.
        food1.camefrom = []
        for s in snake1:
            s.camefrom = []
        openset = [snake1[-1]]
        closedset = []
        dir_array1 = []
    # The A* algorithm.
        while True:
        # Getting the Spot object with the lowest f value from the openset list and adding it to the
        # closedset list.
            if openset == []:
                messagebox.showinfo(message="SIN CAMINO", title="ERROR")
            current1 = min(openset, key=lambda x: x.f)
            openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1]
            closedset.append(current1)
            for neighbor in current1.neighbors:
                if neighbor not in closedset and not neighbor.obstacule and neighbor not in snake1:
                    tempg = neighbor.g + 1
                    if neighbor in openset:
                        if tempg < neighbor.g:
                            neighbor.g = tempg
                    else:
                        neighbor.g = tempg
                        openset.append(neighbor)
                    # Calculating the distance between the current spot and the food.
                    neighbor.h = sqrt((neighbor.x - food1.x) **
                                  2 + (neighbor.y - food1.y) ** 2)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.camefrom = current1
            if current1 == food1:
                break
        # Getting the path from the snake's head to the food.
        while current1.camefrom:
            if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
                dir_array1.append(2)
            elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
                dir_array1.append(0)
            elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
                dir_array1.append(3)
            elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
                dir_array1.append(1)
            current1 = current1.camefrom

        # Resetting the camefrom, f, h, and g attributes of the Spot objects.
        for i in range(rows):
            for j in range(cols):
                grid[i][j].camefrom = []
                grid[i][j].f = 0
                grid[i][j].h = 0
                grid[i][j].g = 0
        return dir_array1


    class Spot:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.f = 0
            self.g = 0
            self.h = 0
            self.neighbors = []
            self.camefrom = []
            self.obstacule = False
            if randint(1, 101) < 3: self.obstacule = True

        def show(self, color):
            draw.rect(screen, color, [self.x*hr+2, self.y*wr+2, hr-4, wr-4])

        def add_neighbors(self):
            if self.x > 0:
                self.neighbors.append(grid[self.x - 1][self.y])
            if self.y > 0:
                self.neighbors.append(grid[self.x][self.y - 1])
            if self.x < rows - 1:
                self.neighbors.append(grid[self.x + 1][self.y])
            if self.y < cols - 1:
                self.neighbors.append(grid[self.x][self.y + 1])


    # Creating a 2D array of Spot objects.
    grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]


    for i in range(rows):
        for j in range(cols):
            grid[i][j].add_neighbors()

    # Initializing the snake and the food.
    snake = [grid[round(rows/2)][round(cols/2)]]
    food = grid[randint(0, rows-1)][randint(0, cols-1)]
    current = snake[-1]
    dir_array = getpath(food, snake)
    food_array = [food]

    # The main loop of the game. It is the loop that runs the game.
    while not done:

        clock.tick(50)
        screen.fill(BLACK)
        direction = dir_array.pop(-1)
        if direction == 0:
            snake.append(grid[current.x][current.y + 1])
        elif direction == 1:
            snake.append(grid[current.x + 1][current.y])
        elif direction == 2:
            snake.append(grid[current.x][current.y - 1])
        elif direction == 3:
            snake.append(grid[current.x - 1][current.y])
        current = snake[-1]

        # Checking if the snake has reached the food. If it has, it will generate a new food and get the
        # path to it. If it hasn't, it will remove the first element of the snake.
        if current.x == food.x and current.y == food.y:
            while 1:
                food = grid[randint(2, rows - 3)][randint(2, cols - 3)]
                if not (food.obstacule or food in snake):
                    break
            food_array.append(food)
            dir_array = getpath(food, snake)
        else:
            snake.pop(0)

        for spot in snake:
            spot.show(WHITE)
        for i in range(rows):
            for j in range(cols):
                if grid[i][j].obstacule:
                    grid[i][j].show(GREEN)

        food.show(RED)
        snake[-1].show((0, 0, 230))
        display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_w and not direction == 0:
                    direction = 2
                elif event.key == K_a and not direction == 1:
                    direction = 3
                elif event.key == K_s and not direction == 2:
                   direction = 0
                elif event.key == K_d and not direction == 3:
                    direction = 1
