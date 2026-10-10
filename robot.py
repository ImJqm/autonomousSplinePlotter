import pygame
import math


class Robot:
    def __init__(self, x, y, theta, image):
        self.x = x
        self.y = y
        self.theta = theta
        self.image = pygame.image.load(image).convert_alpha()
        self.anchorPoint = (x, y)
        self.type = "robot"
        self.isDragging = False
        # THis should be of type string for path of robot image

    def draw(self, surface):
        surface.blit(
            pygame.transform.rotate(self.image, self.theta),
            self.coordinateTransform(surface),
        )

    def coordinateTransform(self, surface):
        return (
            self.x * surface.get_rect().width / 144,
            ((144 - self.y) * surface.get_rect().height / 144),
        )
