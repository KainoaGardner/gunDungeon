from settings import *
import random

class Level:
    def __init__(self,xShift,yShift,width,height,type,direction):
        self.type = type
        self.width = width + 6
        self.height = height + 6
        self.direction = direction

        self.level = self.createLevel()
        self.makePath()

        self.allRooms = []

        self.x = 0
        self.y = 0
        self.currentRoom = 0

        self.xShift = xShift
        self.yShift = yShift

        self.wall = pygame.image.load("graphics/wall.png").convert()
        self.floor = pygame.image.load("graphics/floor.png").convert()

        self.wall = pygame.transform.scale(self.wall,(TILESIZE,TILESIZE))
        self.floor = pygame.transform.scale(self.floor,(TILESIZE,TILESIZE))
        self.tileDict = {0:self.floor,1:self.wall}

        self.tileGroup = pygame.sprite.Group()
        self.createTiles()

    def makePath(self):
        for direction in self.direction:
            if direction == "up":
                for i in range(4):
                    self.level[i][((self.width - 1) // 2) - 1] = 1
                    self.level[i][(self.width - 1) // 2] = 0
                    self.level[i][((self.width - 1) // 2) + 1] = 0
                    self.level[i][((self.width - 1) // 2) + 2] = 1
            elif direction == "down":
                for i in range(4):
                    self.level[(self.height - 1) - i][((self.width - 1) // 2) - 1] = 1
                    self.level[(self.height - 1) - i][(self.width - 1) // 2] = 0
                    self.level[(self.height - 1) - i][((self.width - 1) // 2) + 1] = 0
                    self.level[(self.height - 1) - i][((self.width - 1) // 2) + 2] = 1
            elif direction == "right":
                for i in range(4):
                    self.level[((self.height - 1) // 2) - 1][self.width - 1 - i] = 1
                    self.level[(self.height - 1) //2 ][self.width -1- i] = 0
                    self.level[((self.height - 1) // 2) + 1][self.width-1 - i] = 0
                    self.level[((self.height - 1) // 2) + 2][self.width -1- i] = 1

            elif direction == "left":
                for i in range(4):
                    self.level[((self.height - 1) // 2) - 1][i] = 1
                    self.level[(self.height - 1) // 2][i] = 0
                    self.level[((self.height - 1) // 2) + 1][i] = 0
                    self.level[((self.height - 1) // 2) + 2][i] = 1

    def createLevel(self):
        list = []
        for r in range(3):
            row = []
            for c in range(self.width):
                row.append(3)
            list.append(row)

        for r in range(self.height - 6):
            row = []
            for c in range(3):
                row.append(3)
            for c in range(self.width - 6):
                if r == 0 or r == self.height - 6 - 1 or c == 0 or c == self.width -6 - 1:
                    row.append(1)
                else:
                    row.append(0)
            for c in range(3):
                row.append(3)
            list.append(row)

        for r in range(3):
            row = []
            for c in range(self.width):
                row.append(3)
            list.append(row)

        return list
    def createTiles(self):
            for r in range(len(self.level)):
                for c in range(len(self.level[r])):
                    if self.level[r][c] != 3:
                        self.tileGroup.add(Tile(self.xShift + c * TILESIZE,self.yShift + r * TILESIZE,self.tileDict[self.level[r][c]],self.level[r][c]))


class Tile(pygame.sprite.Sprite):
    def __init__(self,x,y,image,type):
        super().__init__()
        self.type = type
        self.image = image
        self.rect = self.image.get_rect(topleft = (x,y))

    def draw(self,xShift,yShift):
        screen.blit(self.image,(self.rect.x - xShift,self.rect.y - yShift))


class Dungeon:
    def __init__(self):
        self.directionDict = {"up":"down","down":"up","right":"left","left":"right"}
        self.direction = ["up","down","left","right"]
        self.lastDirection = ""
        self.lastSize = (0,0)
        self.posx = -300
        self.posy = -300
        self.empty = False
        self.placedRoomPoints = []

        self.dungeon = []


    def createDungeon(self,rooms):
        self.empty = False
        direction = random.choice(self.direction)
        startRoom = Level(self.posx,self.posy,10,10,"start",[direction])
        self.lastDirection = direction
        self.lastSize = (startRoom.width - 6,startRoom.height - 6)
        self.placedRoomPoints.append((self.posx,self.posy))
        self.placedRoomPoints.append((self.posx + 10 * TILESIZE,self.posy * TILESIZE))

        self.dungeon.append(startRoom)

        for i in range(rooms - 1):
            # while not self.empty:
            pathDirections = []
            pathDirections.append(self.directionDict[self.lastDirection])

            if i < rooms - 2:
                while len(pathDirections) <= 1:
                    nextPath = random.choice(self.direction)
                    if nextPath not in pathDirections:
                        pathDirections.append(nextPath)

                roomWidth = random.randint(10,20)
                roomHeight = random.randint(10,20)

                if roomWidth % 2 != 0:
                    roomWidth += 1
                if roomHeight % 2 != 0:
                    roomHeight += 1
            else:
                roomWidth = 20
                roomHeight = 20

            # self.empty = self.checkPlaced(roomWidth,roomHeight,pathDirections[0])

            if pathDirections[0] == "right":
                self.posx -= roomWidth * TILESIZE + 600
                self.posy += ((self.lastSize[1] // 2) - (roomHeight // 2)) * TILESIZE
            elif pathDirections[0] == "left":
                self.posx += self.lastSize[0] * TILESIZE + 600
                self.posy += ((self.lastSize[1] // 2) - (roomHeight // 2)) * TILESIZE
            elif pathDirections[0] == "up":
                self.posy += self.lastSize[1] * TILESIZE + 600
                self.posx += ((self.lastSize[0] // 2) - (roomWidth // 2)) * TILESIZE
            elif pathDirections[0] == "down":
                self.posy -= roomHeight * TILESIZE + 600
                self.posx += ((self.lastSize[0] // 2) - (roomWidth // 2)) * TILESIZE


            self.lastSize = (roomWidth,roomHeight)

            self.dungeon.append(Level(self.posx,self.posy,roomWidth,roomHeight,"",pathDirections))
            self.lastDirection = nextPath

        return self.dungeon

    def checkPlaced(self,width,height,direction):
        posx = self.posx
        posy = self.posy
        if direction == "right":
            posx -= width * TILESIZE + 600
            posy += ((self.lastSize[1] // 2) - (height // 2)) * TILESIZE
        elif direction == "left":
            posx += self.lastSize[0] * TILESIZE + 600
            posy += ((self.lastSize[1] // 2) - (height // 2)) * TILESIZE
        elif direction == "up":
            posy += self.lastSize[1] * TILESIZE + 600
            posx += ((self.lastSize[0] // 2) - (width // 2)) * TILESIZE
        elif direction == "down":
            posy -= height * TILESIZE + 600
            posx += ((self.lastSize[0] // 2) - (width // 2)) * TILESIZE

        point1 = (posx,posy)
        point2 = (posx + width * TILESIZE,posy + height * TILESIZE)

        for point in self.placedRoomPoints:
            if point1[0] < point[0] < point2[0] and point1[1] < point[1] < point2[0]:
                return False

        self.placedRoomPoints.append(point1)
        self.placedRoomPoints.append(point2)
        return True


dungeonLevel = Dungeon()
dungeon = dungeonLevel.createDungeon(5)