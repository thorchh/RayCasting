from random import randint

import pygame
import math

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

dispW = 800
dispH = 400

sceneW = 400
sceneH = 400

lines = 400

gameDisplay = pygame.display.set_mode((dispW, dispH))
gameDisplay.fill(black)

pygame.display.set_caption('rettttt')
gameExit = False

leadX = 300
leadY = 300
leadXChange = 0
leadYChange = 0
leadDirChange = 0

collidePos = [0, 0]

clock = pygame.time.Clock()


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


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

    def updateDir(self,angle):
        self.dir.rotate_ip_rad(angle)

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
        self.pos = pygame.Vector2(w / 4, h / 4)
        self.rays = []
        self.heading = 0;
        for a in range(lines):
            self.rays.append(Ray(self.pos, math.radians(a * 0.05)))

    def update(self, x, y):
        self.pos.x = x
        self.pos.y = y

    def show(self):
        for b in self.rays:
            b.show()

    def look(self, walls):
        scene = []
        for i in range(lines):
            scene.append(i)

        for j in range(len(self.rays)):
            ray = self.rays[j]
            closest = None
            record = 10000000000000000
            for wall in walls:
                pt = ray.cast(wall)
                if pt:
                    distance = math.hypot(self.pos.x - pt.x, self.pos.y - pt.y)
                    if distance < record:
                        record = distance
                        closest = pt
            if closest:
                pygame.draw.line(gameDisplay, white, (self.pos.x, self.pos.y), (closest.x, closest.y))
            if record != 10000000000000000:
                scene[j] = record
            else:
                scene[j] = 0
        return scene

    def rotate(self, angle):
        self.heading += angle
        for l in range(len(particle.rays)):
            particle.rays[l].updateDir(angle)

    def move(self, amount):
        velocity = (pygame.Vector2(1,0))
        velocity.rotate_rad(self.heading)
        print(velocity)
        velocity .scale_to_length(amount)
        self.pos.dot(velocity)


walls = []
for i in range(5):
    walls.append(i)

w, h = pygame.display.get_surface().get_size()
walls.append(Boundary(0, 0, sceneW, 0))
walls.append(Boundary(sceneW, 0, sceneW, sceneH))
walls.append(Boundary(sceneW, sceneH, 0, sceneH))
walls.append(Boundary(0, sceneH, 0, 0))
for i in range(5):
    x1 = randint(0, sceneW)
    y1 = randint(0, sceneH)
    x2 = randint(0, sceneW)
    y2 = randint(0, sceneH)

    walls[i] = Boundary(x1, y1, x2, y2)
particle = Particle()
p12Change = 0
p34Change = 0

while not gameExit:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        particle.rotate(0.03)
    if keys[pygame.K_d]:
        particle.rotate(-0.03)
    if keys[pygame.K_w]:
        particle.move(1)
    if keys[pygame.K_s]:
        particle.move(-1)
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

    for wall in walls:
        wall.show()

    particle.show()
    scene = particle.look(walls)
    w = sceneW / len(scene)
    for k in range(len(scene)):
        # print (scene[i])
        sSQ = scene[k] * scene[k]
        wSQ = sceneW * sceneW
        hSQ = sceneH * sceneH
        colour11 = translate(sSQ, 0, math.hypot(wSQ, hSQ), 255, 0)
        height11 = translate(scene[k], 0, math.hypot(sceneW, sceneH) / 1.2, sceneH, 0)

        colour = (colour11, colour11, colour11)
        pygame.draw.rect(gameDisplay, colour, (((k * w) + sceneW), (sceneH - height11) / 2, w + sceneW +1, height11))
    # ray.show()
    # ray.lookAt(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
    # point = ray.cast(wall)
    # print(point)
    # if (point):
    #     pygame.draw.rect(gameDisplay, white, [point.x, point.y, 10, 10])
    pygame.display.update()
    clock.tick(10)

pygame.quit()
quit()
