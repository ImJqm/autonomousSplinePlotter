import pygame
import math

class Point:

    def __init__(self, x, y, r, col):
        self.x = x
        self.y = y
        self.r = r
        self.type = "circle"
        self.isDragging = False
        self.col  = col

    def draw(self, surface):
        pygame.draw.circle(
                            surface,
                            self.col,
                            (self.coordinateTransform(surface)),
                            self.r *  surface.get_rect().width / 144
                        )

    def checkMouseCollision(self, distance, hitboxMultiplier):
        return distance < self.r * hitboxMultiplier

    def computeDistance(self, pos, screen, interactionRect):
        print("Mouse POS", pos)
        print("Parsed Mouse", self.parseMouseCoords(pos, screen, interactionRect))
        print("Actual Coords", (self.x, self.y))
        return math.dist(self.parseMouseCoords(pos, screen, interactionRect), (self.x, self.y))

    def coordinateTransform(self, surface):
        return (self.x * surface.get_rect().width / 144 , ((144-self.y) * surface.get_rect().height / 144))

    def parseMouseCoords(self, pos, screen, interactionRect):
        xMax = interactionRect.width
        yMax = interactionRect.height
        screen_rect = screen.get_rect()
        newX = None
        newY = None
        if (pos[0] > xMax):
            newX = xMax
        elif (pos[0] < 0):
            newX = 0
        else:
            newX = pos[0]  
        if (pos[1] > yMax):
            newY = yMax
        elif (pos[1] < 0):
            newY = 0
        else:
            newY = pos[1]  
        return (newX / xMax * 144, (144 - newY / yMax * 144))

    def updateCoords(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def getPos(self):
        return (self.x, self.y)
