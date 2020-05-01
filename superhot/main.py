import pygame as pg, time, math, random
from levels import *
width = 800
height = 800
pg.init()
screen = pg.display.set_mode((width, height))
done = False
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
grey = (134, 136, 138)
keys = pg.key.get_pressed()
counter = 0
pace = 1
levelCounter = 0
gunshot = pg.mixer.Sound('gunshot.wav')
pg.mixer.music.load('music.mp3')
pg.mixer.music.play(-1)
class Player:
    def __init__(self, x, y):
        self.type = "player"
        self.alive = True
        self.width = 40
        self.height = 40
        self.skin = pg.image.load("pSkin.png")
        self.skin = pg.transform.scale(self.skin, (self.width, self.height))
        self.x = x
        self.y = y
        self.vel = pace * 3
        self.moving = False
        self.center = (self.x + self.width / 2, self.y + self.height / 2)
        self.rect = self.skin.get_rect(center=(self.x, self.y))
        self.center = self.skin.get_rect().center[0] + self.x, self.skin.get_rect().center[1] + self.y
        #self.mousePos = pg.mouse.get_pos()

    def move(self):
        keys = pg.key.get_pressed()
        self.moving = False
        if keys[pg.K_w]:
            self.y -= self.vel
            self.moving = True
        if keys[pg.K_s]:
            self.y += self.vel
            self.moving = True
        if keys[pg.K_a]:
            self.x -= self.vel
            self.moving = True
        if keys[pg.K_d]:
            self.x += self.vel
            self.moving = True

    def draw(self):
        self.center = (self.x + self.width / 2, self.y + self.height / 2)
        pg.draw.rect(screen, blue, (self.x, self.y, self.width, self.height))
        screen.blit(self.skin, (self.x, self.y))

class Bullet:
    def __init__(self, startX, startY, endX, endY, type):
        self.type = type
        self.width = 5
        self.height = 4
        if self.type == "eBullet":
            self.color = red
        else:
            self.color = blue
        self.x = startX
        self.y = startY
        self.endX = endX
        self.endY = endY
        self.xLeg = self.x - self.endX
        self.yLeg = self.y - self.endY
        self.hypo = math.sqrt(self.xLeg ** 2 + self.yLeg ** 2)
        self.xVel = self.xLeg / self.hypo
        self.yVel = self.yLeg / self.hypo

    def draw(self):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.x -= self.xVel * pace * 5
        self.y -= self.yVel * pace * 5

class Enemy:
    def __init__(self, x, y):
        self.type = "enemy"
        self.skin = pg.image.load("eSkin.png")
        self.x = x
        self.y = y
        self.vel = pace / 7
        self.width = 40
        self.height = 40
        self.skin = pg.transform.scale(self.skin, (self.width, self.height))
        self.xLeg = 0
        self.yLeg = 0
        self.hypo = 0
        self.center = 0
        self.eCounter = 0

    def move(self):
        self.vel = pace
        self.xLeg = self.x - player.x
        self.yLeg = self.y - player.y
        self.hypo = math.sqrt(self.xLeg ** 2 + self.yLeg ** 2)
        self.x -= self.xLeg / self.hypo * self.vel
        self.y -= self.yLeg / self.hypo * self.vel
        self.eCounter += 1

        if self.eCounter > 50:
            gunshot.play()
            self.eCounter = 0
            sprites.append(Bullet(self.center[0], self.center[1], player.center[0], player.center[1], "eBullet"))

    def draw(self):
        pg.draw.rect(screen, red, (self.x, self.y, self.width, self.height))
        self.center = (self.x + self.width / 2, self.y + self.height / 2)
        screen.blit(self.skin, (self.x, self.y))


class Wall:
    def __init__(self, x, y, width, height):
        self.type = "wall"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.skin = pg.image.load("wSkin.png")
        self.color = grey

    def draw(self):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        pass

class Button:
    def __init__(self, x, y, width, height, color):
        self.type = "enemy"
        self.skin = pg.image.load("startButton.png")
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        screen.blit(self.skin, (self.x, self.y))

    def move(self):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


def collide(s, s2):
    if s.type != s2.type:
        rect1 = pg.Rect(s.x, s.y, s.width, s.height)
        rect2 = pg.Rect(s2.x, s2.y, s2.width, s2.height)
        if rect1.colliderect(rect2):
            if s.type == "wall":
                if s2.type == "player" or s2.type == "enemy":
                    wallCollide(s2, s)
                    return False
                if s2.type == "eBullet" or s2.type == "pBullet":
                    sprites.remove(s2)
                    return False
            if s2.type == "wall":
                return False

        if s.type == "pBullet" and s2.type == "eBullet" or s.type == "eBullet" and s2.type == "pBullet":
            return False
        if s.type == "pBullet" and s2.type == "player" or s.type == "player" and s2.type == "pBullet":
            return False
        if s.type == "eBullet" and s2.type == "enemy" or s.type == "enemy" and s2.type == "eBullet":
            return False

        if rect1.colliderect(rect2):
            return True
        else:
            return False

def wallCollide(p, wall):
    pRect = pg.Rect(p.x, p.y, p.width, p.height)
    wallRect = pg.Rect(wall.x, wall.y, wall.width, wall.height)

    if wallRect.left < pRect.right < wallRect.right:
        if wallRect.top < pRect.bottom < wallRect.bottom or wallRect.top < pRect.top < wallRect.bottom:
            p.x -= p.vel
    if wallRect.left < pRect.left < wallRect.right:
        if wallRect.top < pRect.bottom < wallRect.bottom or wallRect.top < pRect.top < wallRect.bottom:
            p.x += p.vel
    if wallRect.top < pRect.bottom < wallRect.bottom:
        if wallRect.left < pRect.left < wallRect.right or wallRect.left < pRect.right < wallRect.right:
            p.y -= p.vel
    if wallRect.top < pRect.top < wallRect.bottom:
        if wallRect.left < pRect.left < wallRect.right or wallRect.left < pRect.right < wallRect.right:
            p.y += p.vel

stage = []
def buildLevel(level):
    for row in range(len(level)):
        for block in range(len(level[row])):
            if level[row][block] == "p":
                player.x = block * 50
                player.y = row * 50
            if level[row][block] == "e":
                sprites.append(Enemy(block * 50 + 25 / 2, row * 50 + 25 / 2))
            if level[row][block] == "w":
                sprites.append(Wall(block * 50, row * 50, 50, 50))
            if level[row][block] == 's':
                sprites.append(Wall(block * 50, row * 50, width / 16, height - width / 10))
            if level[row][block] == 'c':
                sprites.append(Wall(block * 50, row * 50, width, height / 16))



def levelReset(levelCounter):
    global sprites
    sprites = []
    sprites.append(player)
    global counter
    counter = 1000
    buildLevel(levels[levelCounter])

place = "home"
sprites = []
player = Player(400, 700)
sprites.append(player)
startButton = Button(300, 300, 200, 100, red)
sprites.append(startButton)
clock = pg.time.Clock()
skipCounter = 100
stage = []
counter = 50
gameStart = True
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

    enemiesAlive = False
    for s in sprites:
        if s.type == "enemy":
            enemiesAlive = True
    if not enemiesAlive:
        levelCounter += 1
        levelReset(levelCounter)
    if not player.alive:
        player.alive = True
        levelReset(levelCounter)
    if player.moving:
        pace = 2
    else:
        pace = 1

    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE] and skipCounter > 100:
        levelCounter += 1
        levelReset(levelCounter)
        skipCounter = 0
    skipCounter += 1
    if event.type == pg.MOUSEBUTTONDOWN:
        if event.button == 1 and counter > 50:
            gunshot.play()
            counter = 0
            mousePos = pg.mouse.get_pos()
            newBullet = Bullet(player.center[0], player.center[1], mousePos[0], mousePos[1], "pBullet")
            sprites.append(newBullet)
    counter += 1
    for s in sprites:
        for s2 in sprites:
            if s.type != s2.type:
                collided = collide(s, s2)
                if collided and s.type == "player" or collided and s2.type == "player":
                    player.alive = False
                elif collided:
                    sprites.remove(s)
                    sprites.remove(s2)
    screen.fill(white)
    for s in sprites:
        s.move()
        s.draw()
    pg.display.flip()