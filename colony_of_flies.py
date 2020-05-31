import pygame
import random
import math
import numpy as np
import sys
import matplotlib.pyplot as plt

WHITE = (255,255,255)
GREEN = (0,255,0)
DARK_GREEN = (50,205,50)
RED = (255,0,0)
BLACK =(0,0,0)

class fly():
    def __init__(self, x, y):
        """
        (x,y) - coordinates of fly
        """
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 2, 2)  #obiekt pygame'u
        self.color = RED

    def movement(self):
        """
        Fly's movement is a bit modified Brown Motion, because for large t, variance of
        normal distribution is so high and fly's movement is similar to random jumping on the screen,
        so finally variance is equal to 4
        """
        u1 = random.normalvariate(0,4)
        u2 = random.normalvariate(0,4)
        self.x = self.x + u1
        self.y = self.y + u2

        if self.x < 0:
            self.x = 0
        elif self.x > 1000:
            self.x = 1000
        if self.y < 0:
            self.y = 0
        elif self.y > 600:
            self.y = 600

        self.rect.center = (self.x, self.y)

    def breeding(self):
        """
        Breeding - program generate number from defined interval, if generated number
        is equal to time t, defined fly set one egg in (x,y)"""
        if t == random.randint(int(t-1/p), int(t+1/p)):
            eggs.append(egg(self.x, self.y, t + 50)) # t + 50 ---> time, when egg will be hatched

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class egg():
    """
    (x,y) - coordinates of egg
    hatchtime - time, in which eggs will change in flies"""
    def __init__(self, x, y, hatchtime):
        self.x = x
        self.y = y
        self.hatchtime = hatchtime
        self.rect = pygame.Rect(self.x, self.y, 5, 5)

    def hatch(self):
        """
        eggs are changing for defined number of flies"""
        if t == self.hatchtime:
            for i in range(size_of_breeding):
                flies.append(fly(self.x, self.y))
            eggs.remove(self)

    def draw(self):
        pygame.draw.rect(screen, (255,255,0), self.rect)


class car():
    """
    Car - rectangular shape on the screen, always starts on the left side
    """
    def __init__(self, y):
        self.x = 0
        self.y = y
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, 50, 25)
        self.color = (random.uniform(10,250),random.uniform(10,250), random.uniform(10,250))

    def movement(self):
        self.rect.center = (self.x, self.y)
        self.x = self.x + self.speed
        if self.x > 1000:
            pass

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def lyrics(message, size, x,y, color=WHITE):
    largeText = pygame.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_objects(message, largeText,color)
    TextRect.center = (x,y)
    screen.blit(TextSurf,TextRect)


def draw_a_background(t):
    """
    Function to draw all scenery
    """
    d = min(int(t/10),100)
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLACK, (0,200,1000,400),0)
    pygame.draw.rect(screen,DARK_GREEN,(0,0,1000, 200-d),0)
    pygame.draw.rect(screen,DARK_GREEN,(0,400+d,1000, 200+d),0)
    for i in range(0,10,2):
        pygame.draw.line(screen,WHITE,(100*i + 25,300),(100*(i+1) + 25,300))


size_of_breeding = 20 #number of flies hacthed from egg
p = 0.0005  #probability od setting an egg by one fly in time t
initial_number_of_flies = 100 #initial number of flies
N_t = 1/2 #intensity of appearing cars on the screen

pygame.display.init()
screen = pygame.display.set_mode((1000,600))
pygame.display.flip()
pygame.font.init()
clock = pygame.time.Clock()

intro = True

eggs = []
cars = []
flies = []

for i in range(initial_number_of_flies):
    flies.append(fly(random.uniform(20,980), random.uniform(20,580)))


t = 0
t1 = 0
deaths = 0

while intro:
    if t1 <= t:
        U = random.random()
        t1 = t1 - 1/N_t * math.log(U)
        t1 = int(t1) + 7
        d = min(int(t/10),100)
        cars.append(car(random.uniform(220-d,380+d)))
    t+=1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()

    draw_a_background(t)

    for item in cars:
        item.draw()
        item.movement()

    for item in eggs:
        for item1 in cars:
            if item1.rect.colliderect(item.rect):
                eggs.remove(item)
        item.hatch()
        item.draw()

    for item in flies:
        for item1 in cars:
            if item1.rect.colliderect(item.rect):
                flies.remove(item)
                deaths +=1

        item.draw()
        item.movement()
        item.breeding()

    if len(flies) > 4000:
        print("Too much flies")
        pygame.display.quit()
        sys.exit()


    if len(flies) == 0:
        pygame.display.quit()
        sys.exit()

    lyrics("Week: " + str(int(t/10)),20, 60, 510)
    lyrics("Flies: " + str(len(flies)),20, 70, 540)
    lyrics("Deaths: " + str(deaths),20, 60, 570)
    pygame.display.update()
    clock.tick(20)