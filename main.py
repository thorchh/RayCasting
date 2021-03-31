import pygame

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

gameDisplay = pygame.display.set_mode((800, 600))

pygame.display.set_caption('rettttt')
gameExit = False

leadX = 300
leadY = 300
leadXChange = 0
leadYChange = 0

clock = pygame.time.Clock()


class Boundary():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.a = pygame.Vector2(x1, y1)
        self.b = pygame.Vector2(x2, y2)

    def show(self):
        pygame.draw.line(gameDisplay, black, (self.a), (self.b))

    def update(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.a = pygame.Vector2(x1, y1)
        self.b = pygame.Vector2(x2, y2)


class Ray():
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.dir = pygame.Vector2(1, 0)

    def show(self):
        pygame.draw.line(gameDisplay, black, self.pos, (self.dir * 10) + self.pos)

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
            x = cx1 + t * (cx2 - cx1)
            y = cy1 + t * (cy2 - cy1)
            collidePos = [x, y]
            return collidePos

p1 = 300
p2 = 100
p3 = 300
p4 = 300
wall = Boundary(p1, p2, p3, p4)
ray = Ray(100, 200)
p12Change = 0
p34Change = 0
while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                leadXChange -= 10
                p12Change -= 10
            if event.key == pygame.K_RIGHT:
                leadXChange += 10
                p12Change += 10
            if event.key == pygame.K_UP:
                leadYChange -= 10
                p34Change -= 10
            if event.key == pygame.K_DOWN:
                leadYChange += 10
                p34Change += 10
            if event.key == pygame.K_ESCAPE:
                gameExit = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                leadXChange = 0
                p12Change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                leadYChange = 0
                p34Change = 0
        print(event)
    leadX += leadXChange
    leadY += leadYChange
    p3 += p12Change
    p4 += p34Change
    gameDisplay.fill(white)
    pygame.draw.rect(gameDisplay, black, [leadX, leadY, 10, 10])
    wall.update(p1, p2, p3, p4)
    wall.show()
    ray.show()
    point = ray.cast(wall)
    print(point)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
