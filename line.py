import pygame
from point import Point

class Line:

    def __init__(self, p1, p2, col, width):
        self.p1 = p1
        self.p2 = p2
        self.col = col
        self.type = "line"
        self.width = width
        self.isDragging = False

    def draw(self, surface):
        pygame.draw.line(surface, self.col, self.coordinateTransform(surface,self.p1.getPos()), self.coordinateTransform(surface,self.p2.getPos()), width=self.width)


    def coordinateTransform(self, surface, pos):
        return (pos[0] * surface.get_rect().width / 144 , ((144-pos[1]) * surface.get_rect().height / 144))
