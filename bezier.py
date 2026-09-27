import pygame
from point import Point

class Bezier:

    def __init__(self, p0, p1, p2, p3, col, width, stepSize):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.col = col
        self.type = "line"
        self.width = width
        self.stepSize = stepSize
        self.isDragging = False

    def draw(self, surface):
        rect = surface.get_rect()
        w = rect.width
        h = rect.height
        #for i in range(0,1,self.stepSize):
        i = 0.0
        while (i<=1.0):
            x = (1-i)**3 * self.p0.getPos()[0] + 3*(1-i)**2 * i * self.p1.getPos()[0] + 3*(1-i)*i**2*self.p2.getPos()[0] + i**3 * self.p3.getPos()[0]
            y = (1-i)**3 * self.p0.getPos()[1] + 3*(1-i)**2 * i * self.p1.getPos()[1] + 3*(1-i)*i**2*self.p2.getPos()[1] + i**3 * self.p3.getPos()[1]
            pygame.draw.rect(surface,self.col,(x*w/144 - self.width/2, (144-y)*w/144 - self.width/2, self.width, self.width))
            i += self.stepSize


    def coordinateTransform(self, surface, pos):
        return (pos[0] * surface.get_rect().width / 144 , ((144-pos[1]) * surface.get_rect().height / 144))
