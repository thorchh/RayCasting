from random import randint

import pygame
import math

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

gameDisplay = pygame.display.set_mode((800, 600))
gameDisplay.fill(black)

pygame.display.set_caption('rettttt')
gameExit = False

leadX = 300
leadY = 300
leadXChange = 0
leadYChange = 0

collidePos = [0, 0]

clock = pygame.time.Clock()




class Boundary:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.a = pygame.Vector2(x1, y1)
        self.b = pygame.Vector2(x2, y2)

    def update(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.a = pygame.Vector2(x1, y1)
        self.b = pygame.Vector2(x2, y2)

    def show(self):
        pygame.draw.line(gameDisplay, white, self.a, self.b)


class Ray:
    def __init__(self, pos, angle):
        self.pos = pos
        self.dir = (pygame.Vector2(0, 1)).rotate_rad(angle)

    def lookAt(self, x, y):
        self.dir.x = x - self.pos.x
        self.dir.y = y - self.pos.y
        if self.dir != 0:
            self.dir = pygame.Vector2.normalize(self.dir)

    def show(self):
        pygame.draw.line(gameDisplay, white, self.pos, (self.dir * 10) + self.pos)

    def cast(self, boundary):
        cx1 = boundary.a.x
        cy1 = boundary.a.y
        cx2 = boundary.b.x
        cy2 = boundary.b.y

        cx3 = self.pos.x
        cy3 = self.pos.y
        cx4 = self.pos.x + self.dir.x
        cy4 = self.pos.y + self.dir.y

        den = (cx1 - cx2) * (cy3 - cy4) - (cy1 - cy2) * (cx3 - cx4)
        num = (cx1 - cx3) * (cy3 - cy4) - (cy1 - cy3) * (cx3 - cx4)
        if den == 0:
            return False

        t = num / den
        u = -((cx1 - cx2) * (cy1 - cy3) - (cy1 - cy2) * (cx1 - cx3)) / den

        if 0 < t < 1 and 0 < u:
            point = pygame.Vector2(0, 0)
            point.x = cx1 + t * (cx2 - cx1)
            point.y = cy1 + t * (cy2 - cy1)
            return point


class Particle:

    def __init__(self):
        w, h = pygame.display.get_surface().get_size()
        self.pos = pygame.Vector2(w / 2, h / 2)
        self.rays = []
        for a in range(3600):
            self.rays.append(Ray(self.pos, math.radians(a*0.1)))

    def update(self, x, y):
        self.pos.x = x
        self.pos.y = y

    def show(self):
        for b in self.rays:
            b.show()

    def look(self, wall):
        for b in self.rays:
            closest = None
            record = 10000000000000000
            for wall in walls:
                pt = b.cast(wall)
                if pt:
                    distance = math.hypot(self.pos.x - pt.x, self.pos.y - pt.y)
                    if distance < record:
                      record = distance
                      closest = pt
            if closest:
                pygame.draw.line(gameDisplay, white, (self.pos.x, self.pos.y), (closest.x, closest.y))


walls = []
for i in range(5):
    walls.append(i)

w, h = pygame.display.get_surface().get_size()
walls.append( Boundary(0,0, w, 0))
walls.append( Boundary(w,0, w, h))
walls.append( Boundary(w,h, 0, h))
walls.append( Boundary(0,h, 0, 0))
for i in range (5):
    x1 = randint(0,w)
    y1 = randint(0,h)
    x2 = randint(0,w)
    y2 = randint(0,h)

    walls[i] = Boundary(x1, y1, x2, y2)
ray = Ray((100, 200), 30)
particle = Particle()
p12Change = 0
p34Change = 0
while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                leadXChange -= 10
                # p12Change -= 10
            if event.key == pygame.K_RIGHT:
                leadXChange += 10
                # p12Change += 10
            if event.key == pygame.K_UP:
                leadYChange -= 10
                # p34Change -= 10
            if event.key == pygame.K_DOWN:
                leadYChange += 10
                # p34Change += 10
            if event.key == pygame.K_ESCAPE:
                gameExit = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                leadXChange = 0
                # p12Change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                leadYChange = 0
                # p34Change = 0
        # print(event)
    # leadX += leadXChange
    # leadY += leadYChange
    # p3 += p12Change
    # p4 += p34Change
    gameDisplay.fill(black)
    # wall.update(p1, p2, p3, p4)
    for wall in walls:
        wall.show()

    particle.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    particle.show()
    particle.look(wall)
    # ray.show()
    # ray.lookAt(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
    # point = ray.cast(wall)
    # print(point)
    # if (point):
    #     pygame.draw.rect(gameDisplay, white, [point.x, point.y, 10, 10])
    pygame.display.update()
    clock.tick(30)

pygame.quit()
quit()
