# g.py - globals
"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""

import pygame
import random

import utils

app = 'Letters'
ver = '1'
ver = '21'
ver = '22'
# error message does not persist where it shouldn't
ver = '23'
# circle key toggles help

UP = (264, 273)
DOWN = (258, 274)
LEFT = (260, 276)
RIGHT = (262, 275)
CROSS = (259, pygame.K_2)
CIRCLE = (265, pygame.K_3)
SQUARE = (263, 32)
TICK = (257, 13)
NUMBERS = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4,
         pygame.K_5: 5, pygame.K_6: 6, pygame.K_7: 7, pygame.K_8: 8,
         pygame.K_9: 9, pygame.K_0: 0}


def init():  # called by run()
    random.seed()
    global redraw
    global screen, w, h, font1, font2, clock
    global factor, offset, imgf, message, version_display
    global pos, pointer
    redraw = True
    version_display = False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((70, 0, 70))
    pygame.display.flip()
    w, h = screen.get_size()
    if float(w) / float(h) > 1.5:  # widescreen
        offset = (w - 4 * h / 3) / 2  # we assume 4:3 - centre on widescreen
    else:
        h = int(.75 * w)  # allow for toolbar - works to 4:3
        offset = 0
    factor = float(h) / 24  # measurement scaling factor (32x24 = design units)
    imgf = float(h) / 900  # image scaling factor - images built for 1200x900
    clock = pygame.time.Clock()
    if pygame.font:
        t = int(80 * imgf)
        font1 = pygame.font.Font(None, t)
        t = int(96 * imgf)
        font2 = pygame.font.Font(None, t)
    message = ''
    pos = pygame.mouse.get_pos()
    pointer = utils.load_image('pointer.png', True)
    pygame.mouse.set_visible(False)

    # this activity only
    global score, best, state, ms, message_cxy, bgd, score_cxy, best_cxy
    global help_img, help_on, help_cxy
    score = 0
    best = 0
    state = 1
    # 1 displaying given
    # 2 accepting input
    # 3 right
    # 4 wrong
    ms = pygame.time.get_ticks()
    message_cxy = None  # set in let.py
    bgd = utils.load_image('bgd.png', False)
    cy = sy(19)
    score_cxy = (sx(16), cy)
    best_cxy = (sx(26), cy)
    help_img = utils.load_image('help.png', False)
    help_cxy = (sx(16), sy(10))
    help_on = False


def sx(f):  # scale x function
    return int(f * factor + offset + .5)


def sy(f):  # scale y function
    return int(f * factor + .5)
