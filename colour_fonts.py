"""
colour_fonts by Andy Wang
========================================================================================
This Python module contains a bunch of colour constants and fonts.
========================================================================================
Copyright (c) 2020 Andy Wang
"""
import pygame

# COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_RED = (255, 125, 125)
ORANGE = (255, 127, 0)
LIGHT_ORANGE = (255, 190, 125)
YELLOW = (245, 206, 66)
LIGHT_BLUE = (200, 234, 247)

# FONTS
pygame.init()
# Calibri 14 bold
CALIBRI_14_B = pygame.font.SysFont('Calibri', 14, bold=True)
CALIBRI_24_B = pygame.font.SysFont('Calibri', 24, bold=True)

if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'E9999', 'E1101']
    })
