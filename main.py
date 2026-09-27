import pygame
import sys
from point import Point
from line import Line
from bezier import Bezier

def scale_image(img, target_rect):
    return pygame.transform.smoothscale(
        surface=img, size=(target_rect.width, target_rect.height)
    )


def draw_surface(elements, surface):
    surface.fill((0, 0, 0, 0))
    for element in elements:
        element.draw(surface)
    return surface

def main():
    
    # Default Parameters
    SCREENX = 1080
    SCREENY = 1080
    scaleX = SCREENX / 1080
    scaleY = SCREENY / 1080

    mousePressed = False
    
    elements = []

    WHITE = (255,255,255)
    RED = (255,0,0)

    pygame.init()
    
    #Currently, we make the screen resizable, I want to ensure visual clarity on the size of the robot and spline graph
    screen = pygame.display.set_mode((1080, 1080), pygame.RESIZABLE)

    pygame.display.set_caption("Spline Editor")

    display = pygame.Surface((1080,1080), pygame.SRCALPHA)
    
    p0 = Point(72,72,1,WHITE)
    elements.append(p0)

    p1 = Point(10,10,1,RED)
    elements.append(p1)

    l1 = Line(p0, p1, WHITE, 5)
    elements.append(l1)

    p2 = Point(120,120,1,RED)
    elements.append(p2)

    p3 = Point(130,130,1,WHITE)
    elements.append(p3)

    l2 = Line(p2, p3, WHITE, 5)
    elements.append(l2)

    b1 = Bezier(p0, p1, p2, p3, WHITE, 5, 0.001)
    elements.append(b1)
    #This is the background yoinked from the official pedro pathing visualizer, we need to make our own later
    bg = pygame.image.load("biobuzz.webp").convert_alpha()
    running = True
    bg_rect = screen.get_rect()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                # This is specifically to ensure that what we render remaains a square regardless of the window size to 
                # get rid of apparent scalign issues
                print("REISIZING")
                width, height = event.w, event.h
                dimension = width if width < height else height
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                bg_rect = pygame.Rect(0, 0, dimension, dimension)
                # scaleX = width / 1080
                # scaleY = height / 1080
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = True
                validElements = {}
                for element in elements:
                    if (element.type == "circle"):
                        distance = element.computeDistance(event.pos, screen, bg_rect)
                        if (element.checkMouseCollision(distance, 1.25)):
                            validElements[element] = distance
                if (not len(validElements) == 0):
                    closest = min(validElements, key=validElements.get)
                    closest.isDragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                mousePressed = False
                for element in elements:
                    element.isDragging = False
            if event.type == pygame.MOUSEMOTION:
                for element in elements:
                    if  element.isDragging:
                        print("We gotta a drag")
                        element.updateCoords(element.parseMouseCoords(event.pos, screen, bg_rect))
            #This takes 2 args, the screen and the rectangle that the mouse coordinates need to be localized to


        screen.blit(scale_image(bg, bg_rect), (0, 0))
        screen.blit(scale_image(draw_surface(elements, display), bg_rect),  (0,0))
        #print(screen.get_rect().center)
        #print("ScaleX", scaleX)
        #print("ScaleY", scaleY)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


main()
