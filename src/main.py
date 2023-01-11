from time import sleep

from screen import draw_screen
from chip8 import *










if __name__ == '__main__':
    while True:
        sleep(0.1)
        draw_screen(vram, draw_flag)
