import pygame
import pygame_gui
import sys
from point import Point
from line import Line
from bezier import Bezier
from draggable_line import DraggableLine
from robot import Robot


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

    nativeOffset = (200, 000)
    offset = nativeOffset

    mousePressed = False

    elements = []

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    pygame.init()

    # Currently, we make the screen resizable, I want to ensure visual clarity on the size of the robot and spline graph
    screen = pygame.display.set_mode((1080, 1080), pygame.RESIZABLE)
    manager = pygame_gui.UIManager((1080, 1080), "theme.json")

    pygame.display.set_caption("Spline Editor")

    display = pygame.Surface((1080, 1080), pygame.SRCALPHA)

    bg_rect = screen.get_rect()

    p0 = Point(72, 72, 1, WHITE)
    elements.append(p0)

    p1 = Point(10, 10, 1, RED)
    elements.append(p1)

    l1 = Line(p0, p1, WHITE, 5)
    elements.append(l1)

    p2 = Point(120, 120, 1, RED)
    elements.append(p2)

    p3 = Point(130, 130, 1, WHITE)
    elements.append(p3)

    l2 = Line(p2, p3, WHITE, 5)
    elements.append(l2)

    b1 = Bezier(p0, p1, p2, p3, WHITE, 5, 0.001)
    elements.append(b1)

    drag = DraggableLine(offset[0], offset[1], bg_rect.height, 5, 10)

    robot = Robot(72, 72, 0, "robot.png")
    elements.append(robot)
    # This is the background yoinked from the official pedro pathing visualizer, we need to make our own later
    bg = pygame.image.load("biobuzz.webp").convert_alpha()

    background_panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect(
            (0, 0), (screen.get_rect().width, screen.get_rect().height)
        ),
        starting_height=1,
        manager=manager,
    )

    hello_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 50), (100, 50)),
        text="Say Hello",
        manager=manager,
    )

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60) / 1000
        mpos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            manager.process_events(event)

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
                #
                # On Window Resize, we must determine the offset
                dx = (
                    screen.get_rect().width - bg_rect.width + nativeOffset[0]
                )  # native x offset for our side panel
                # im going to change bg_rect, now to be limited, by the size of our side panel
                dimension = screen.get_rect().width - dx
                bg_rect = pygame.Rect(0, 0, dimension, dimension)
                dy = (
                    screen.get_rect().height - bg_rect.height
                )  # difference between our scaleed bg rect and screen size
                offset = (
                    dx,
                    dy / 2,
                )  # Divide dy by 2 so we have the same buffer on top and the bottum
                manager.set_window_resolution((width, height))
                background_panel.set_dimensions((width, height))

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = True
                validElements = {}
                for element in elements:
                    if element.type == "circle":
                        distance = element.computeDistance(
                            event.pos, screen, bg_rect, offset
                        )
                        if element.checkMouseCollision(distance, 1.25):
                            validElements[element] = distance
                if not len(validElements) == 0:
                    closest = min(validElements, key=validElements.get)
                    closest.isDragging = True

                ## Handle Case where we are dragging the mouse
                drag.is_dragged = drag.testDistance(mpos[0], mpos[1])

            if event.type == pygame.MOUSEBUTTONUP:
                mousePressed = False
                for element in elements:
                    element.isDragging = False
                drag.is_dragged = False
            if event.type == pygame.MOUSEMOTION:
                for element in elements:
                    if element.isDragging:
                        print("We gotta a drag")
                        element.updateCoords(
                            element.parseMouseCoords(event.pos, screen, bg_rect, offset)
                        )
                if drag.is_dragged:
                    drag.setX(mpos[0])
                    offset = (
                        mpos[0],
                        (screen.get_rect().height - (screen.get_rect().width - mpos[0]))
                        / 2,
                    )
                    bg_rect = pygame.Rect(
                        0,
                        0,
                        screen.get_rect().width - mpos[0],
                        screen.get_rect().width - mpos[0],
                    )

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    print("Hello World")
            # This takes 2 args, the screen and the rectangle that the mouse coordinates need to be localized to

        manager.update(dt)

        manager.draw_ui(screen)
        screen.blit(scale_image(bg, bg_rect), offset)
        screen.blit(scale_image(draw_surface(elements, display), bg_rect), offset)
        # print(screen.get_rect().center)
        # print("ScaleX", scaleX)
        # print("ScaleY", scaleY)
        # print(drag.x)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


main()
