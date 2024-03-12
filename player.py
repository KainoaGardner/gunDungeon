from settings import *
import math
from dungeon import *
import random
class Player(pygame.sprite.Sprite):
    def __init__(self,size,speed,bulletGroup):
        super().__init__()
        self.size = size
        self.surface = pygame.Surface((self.size,self.size))
        self.surface.fill("#2ecc71")
        self.rect = self.surface.get_rect(center = (WIDTH//2,HEIGHT//2))

        self.gun = "rifle" #"rifle","sniper","shotgun"
        self.gunLength = 40
        self.bulletCounter = 0
        self.reloadTimer = 0
        self.bulletGroup = bulletGroup
        self.angle = 0

        self.gun = pygame.image.load("graphics/wand.png").convert_alpha()
        self.rifle = pygame.transform.scale(self.gun,(80,20))
        self.shotgun = pygame.transform.scale(self.gun, (60, 30))
        self.sniper = pygame.transform.scale(self.gun, (100, 10))

        self.wandRotate = pygame.transform.rotate(self.rifle,self.angle)
        self.wandRotateRect = self.wandRotate.get_rect(center= (WIDTH//2,HEIGHT//2))

        self.speed = speed
        self.diagonalSpeed = math.sqrt((self.speed * self.speed) / 2)
        self.diagonal = False

        self.level = dungeon
        self.mos = pygame.mouse.get_pos()

        self.health = 3
        self.hit = False

        self.xShift = 0
        self.yShift = 0

    def move(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_w] and keys[pygame.K_a]) or (keys[pygame.K_w] and keys[pygame.K_d]) or (keys[pygame.K_s] and keys[pygame.K_a]) or (keys[pygame.K_s] and keys[pygame.K_d]):
            self.diagonal = True
        else:
            self.diagonal = False

        if self.diagonal:
            speed = self.diagonalSpeed
        else:
            speed = self.speed

        if keys[pygame.K_w] and self.collide((0,-speed)):
            self.yShift -= speed
        if keys[pygame.K_s] and self.collide((0,speed)):
            self.yShift += speed
        if keys[pygame.K_a] and self.collide((-speed,0)):
            self.xShift -= speed
        if keys[pygame.K_d] and self.collide((speed,0)):
            self.xShift += speed

        self.guns(keys)

    def guns(self,keys):
        if keys[pygame.K_1]:
            self.gun = "rifle"
            self.gunLength = 40
            self.reloadTimer = 15
            self.bulletCounter = 0
        if keys[pygame.K_2]:
            self.gun = "shotgun"
            self.gunLength = 25
            self.reloadTimer = 15
            self.bulletCounter = 0
        if keys[pygame.K_3]:
            self.gun = "sniper"
            self.gunLength = 50
            self.reloadTimer = 15
            self.bulletCounter = 0

        if keys[pygame.K_SPACE]:
            if self.gun == "rifle":
                self.bulletCounter += 1
                if self.bulletCounter % 5 == 0:
                    self.bulletGroup.add(Bullet(self.rect.centerx + self.xShift,self.rect.centery + self.yShift,3,20,self.angle + random.randint(-5,5),self.gunLength))

            elif self.gun == "shotgun":
                if self.reloadTimer == 0:
                    for i in range(8):
                        self.bulletGroup.add(Bullet(self.rect.centerx + self.xShift + random.randint(-10,10) ,self.rect.centery + self.yShift + random.randint(-10,10),3,15,self.angle + random.randint(-25,25),self.gunLength))
                    self.reloadTimer = 30

            elif self.gun == "sniper":
                if self.bulletCounter < 60:
                    self.bulletCounter += 1
                    size = self.bulletCounter / 3
                else:
                    size = 30
                angle = math.radians(self.angle)
                xMove = math.cos(angle) * self.gunLength
                yMove = math.sin(angle) * self.gunLength
                pygame.draw.circle(screen,"#f1c40f",(self.rect.centerx + xMove,self.rect.centery + yMove),size)

        if keys[pygame.K_SPACE] == False:
            if self.gun == "sniper":
                if self.bulletCounter >= 60:
                    self.bulletCounter = 0
                    self.bulletGroup.add(Bullet(self.rect.centerx + self.xShift, self.rect.centery + self.yShift, 5, 50, self.angle,self.gunLength))
                else:
                    self.bulletCounter = 0

        if self.reloadTimer > 0:
            self.reloadTimer -= 1


    def getAngle(self):
        mos = pygame.mouse.get_pos()
        xDif = mos[0] - WIDTH // 2
        yDif = mos[1] - HEIGHT // 2
        angle = math.degrees(math.atan2(yDif,xDif))
        self.angle = angle

        if self.gun == "rifle":
            self.wandRotate = pygame.transform.rotate(self.rifle,self.angle * -1)
        elif self.gun == "shotgun":
            self.wandRotate = pygame.transform.rotate(self.shotgun, self.angle * -1)
        elif self.gun == "sniper":
            self.wandRotate = pygame.transform.rotate(self.sniper, self.angle * -1)
        else:
            self.gun = "rifle"
        self.wandRotateRect = self.wandRotate.get_rect(center = (WIDTH//2,HEIGHT//2))

    def collide(self,direction):
        for room in self.level:
            for tile in room.tileGroup:
                if tile.type == 1:
                    if (tile.rect.x + TILESIZE - self.xShift > self.rect.x + direction[0] and tile.rect.x - self.xShift < self.rect.x + self.size + direction[0]):
                        if (tile.rect.y + TILESIZE - self.yShift > self.rect.y + direction[1] and tile.rect.y - self.yShift < self.rect.y + self.size + direction[1]):
                            return False
        return True

    def changeHealth(self):  #call when take damage !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if self.health == 3:
            self.surface.fill("#2ecc71")
        elif self.health == 2:
            self.surface.fill("#f39c12")
        elif self.health == 1:
            self.surface.fill("#e74c3c")
        elif self.health <= 0:
            self.kill()

    def displayHit(self):
        if self.hit:
            pygame.draw.circle(screen,"#ecf0f1",(self.rect.center),self.size,5)
    def display(self):
        screen.blit(self.surface,self.rect)
        self.displayHit()
        screen.blit(self.wandRotate,self.wandRotateRect)

    def update(self):
        self.move()
        self.getAngle()
        self.displayHit()
        self.display()


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,speed,size,angle,gunLength):
        super().__init__()
        self.gunLength = gunLength
        self.x = x
        self.y = y
        self.angle = angle
        self.setAimOffset()
        self.speed = speed
        self.size = size
        self.moveSize = 5

    def setAimOffset(self):
        angle = math.radians(self.angle)
        xOffset = math.cos(angle) * self.gunLength
        yOffset = math.sin(angle) * self.gunLength
        self.x += xOffset
        self.y += yOffset

    def getMoveDistance(self):
        angle = math.radians(self.angle)
        xMove = math.cos(angle) * self.moveSize
        yMove = math.sin(angle) * self.moveSize

        self.x += xMove * self.speed
        self.y += yMove * self.speed

    def collide(self):
        for room in dungeon:
            for tile in room.tileGroup:
                if tile.type == 1:
                    if tile.rect.x < self.x < tile.rect.x + TILESIZE and tile.rect.y < self.y < tile.rect.y + TILESIZE:
                            return True
        return False

    def draw(self,xShift,yShift):
        self.getMoveDistance()
        pygame.draw.circle(screen,"#f1c40f",(self.x - xShift,self.y - yShift),self.size)

        if self.collide():
            self.kill()

# self.x  < 0 or self.x  > WIDTH or self.y  < 0 or self.y > HEIGHT or




bulletGroup = pygame.sprite.Group()
player = Player(50,15,bulletGroup)