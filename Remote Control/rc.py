from collections import namedtuple
import win32gui
import pygame
import sys

Button = namedtuple('Button', ('id', 'x', 'y', 'w', 'h', 'name'))

buttons = (
    Button(0x00,  80,  92, 80, 80, 'All'),
    Button(0x01, 202,  92, 80, 80, 'Mute'),
    Button(0x03, 446,  92, 80, 80, 'Power'),
    Button(0x04,  80, 228, 76, 76, 'Part L'),
    Button(0x05, 202, 228, 76, 76, 'Part R'),
    Button(0x06, 326, 228, 76, 76, 'Inst L'),
    Button(0x07, 448, 228, 76, 76, 'Inst R'),
    Button(0x08,  80, 360, 76, 76, 'Level L'),
    Button(0x09, 202, 360, 76, 76, 'Level R'),
    Button(0x0A, 326, 360, 76, 76, 'Reverb L'),
    Button(0x0B, 448, 360, 76, 76, 'Reverb R'),
    Button(0x0C,  80, 492, 76, 76, 'Song L'),
    Button(0x0D, 202, 492, 76, 76, 'Song R'),
    Button(0x0E, 326, 492, 76, 76, 'Tempo L'),
    Button(0x0F, 448, 492, 76, 76, 'Tempo R'),
    Button(0x10,  80, 626, 76, 76, 'Stop'),
    Button(0x11, 202, 626, 76, 76, 'Play'),
    Button(0x12, 326, 626, 76, 76, 'Rew'),
    Button(0x13, 448, 626, 76, 76, 'FF')
)

WM_APP = 0x8000

def enum_window_callback(hwnd, button):
    class_name = win32gui.GetClassName(hwnd)
    if class_name == "SDL_app":
        win32gui.PostMessage(hwnd, WM_APP, button, 0)

def send_to_nuked_sc55(button):
    win32gui.EnumWindows(enum_window_callback, button.id)

def is_hovered(button, x, y):
    if button.x <= x and button.y <= y and (button.x + button.w) >= x and (button.y + button.h) >= y:
        center_x = button.x + button.w / 2
        center_y = button.y + button.h / 2
        dx = x - center_x
        dy = y - center_y
        return (dx * dx) / ((button.w / 2) ** 2) + (dy * dy) / ((button.h / 2) ** 2) <= 1
    return False

pygame.init()

SCALE = 2
WIDTH, HEIGHT = int(600 / SCALE), int(960 / SCALE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Remote Control")

image = pygame.image.load("rc_background.png").convert_alpha()

image = pygame.transform.smoothscale(image, (WIDTH, HEIGHT))

clock = pygame.time.Clock()

screen.blit(image, (0, 0))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            x *= SCALE
            y *= SCALE
            for button in buttons:
                if is_hovered(button, x, y):
                    # print(f"Pressed button {button.name}")
                    send_to_nuked_sc55(button)
                    break
    clock.tick(30)

pygame.quit()
sys.exit()
