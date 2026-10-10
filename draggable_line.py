import pygame
import pygame_gui
import math


class DraggableLine:
    # THESE COORDINATES ARE IN THE ACTUAL SIZE OF THE SCREEN
    # NOT THE 144 x 144 FTC COORDINATES
    #
    def __init__(self, x, y, height, thickness, hitbox_size):
        ### Hitbox is measured in
        self.x = x
        self.y = y
        self.height = height
        self.thickness = thickness
        self.hitbox_size = hitbox_size
        self.is_dragged = False

    def testDistance(self, mx, my):
        return (
            my > self.y - self.hitbox_size
            and self.y < self.y + self.height + self.hitbox_size
            and abs(mx - self.x) < self.hitbox_size
        )

    def setX(self, x):
        self.x = x
