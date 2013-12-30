"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import pygame

import utils
import lang
import g


class Let:
    def __init__(self):
        img = utils.load_image('abcd.png', True)
        wf = 0.0 + img.get_width() / 26.0
        self.h = img.get_height()
        x = 0.0
        y = 0
        self.w = int(wf)
        self.imgs = []
        for i in range(26):
            self.imgs.append(img.subsurface((int(x + .5), y, self.w, self.h)))
            x += wf
        self.x0 = g.sx(16) - 4 * self.w
        self.y0 = g.sy(2)
        self.y1 = self.y0 + 1.5 * self.h
        g.message_cxy = (g.sx(16), self.y0 + 1.25 * self.h)
        self.setup()
        self.ind = None

    def setup(self):
        self.taken = [False] * 8
        self.ans = ''
        self.given = ''
        self.v = 0
        self.c = 0

    def reset(self):
        self.taken = [False] * 8
        self.ans = ''

    def choose(self):  # min 3 vowels,  4 consonants
        d = pygame.time.get_ticks() - g.ms
        if d > 500:  # delay in ms
            g.redraw = True
            if len(self.given) < 8:
                if self.v == 3:
                    l = lang.consonant()
                elif self.c == 4:
                    l = lang.vowel()
                else:
                    l = lang.letter()
                if l in 'aeiou':
                    self.v += 1
                else:
                    self.c += 1
                self.given += l
                g.ms = pygame.time.get_ticks()
            else:
                g.state = 2

    def draw(self):
        x = self.x0
        y = self.y0
        ind1 = 0
        for l in self.given:
            ind = ord(l) - 97
            if not self.taken[ind1]:
                g.screen.blit(self.imgs[ind], (x, y))
            x += self.w
            ind1 += 1
        x = self.x0
        y = self.y1
        for l in self.ans:
            ind = ord(l) - 97
            g.screen.blit(self.imgs[ind], (x, y))
            x += self.w

    def click(self):
        x = self.x0
        y = self.y0
        ind1 = 0
        for l in self.given:
            if utils.mouse_in(x, y, x + self.w, y + self.h):
                if not self.taken[ind1]:
                    self.taken[ind1] = True
                    self.ans += l
                return True
            x += self.w
            ind1 += 1
        x = self.x0
        y = self.y1
        ind1 = 0
        for l in self.ans:
            if utils.mouse_in(x, y, x + self.w, y + self.h):
                self.put_back(l)
                self.ans = self.ans[:ind1] + self.ans[ind1 + 1:]
                g.state = 2
                return True
            x += self.w
            ind1 += 1
        return False

    def set_mouse(self):
        x = self.x
        y = self.y
        pygame.mouse.set_pos(x, y)
        g.pos = (x, y)

    def reset_mouse(self):
        self.x = self.x0 + self.w / 2
        self.y = self.y0 + self.h / 2
        self.ind = 0
        self.set_mouse()

    def right(self):
        if len(self.ans) == 8:
            return
        if self.ind is None:
            self.reset_mouse()
            return
        self.move_right()
        while self.taken[self.ind]:
            self.move_right()
        self.set_mouse()

    def move_right(self):
        if self.ind == 7:
            self.reset_mouse()
            return
        self.ind += 1
        self.x += self.w

    def left(self):
        if len(self.ans) == 8:
            return
        if self.ind is None:
            self.reset_mouse()
            return
        self.move_left()
        while self.taken[self.ind]:
            self.move_left()
        self.set_mouse()

    def move_left(self):
        if self.ind == 0:
            self.ind = 8
            self.x = self.x0 + self.w / 2 + 8 * self.w
        self.ind -= 1
        self.x -= self.w

    def key(self, letter):
        ind = 0
        for l in self.given:
            if not self.taken[ind]:
                if l == letter:
                    self.taken[ind] = True
                    self.ans += l
                    return
            ind += 1
        ind = 0
        for l in self.ans:
            if l == letter:
                self.put_back(l)
                self.ans = self.ans[:ind] + self.ans[ind + 1:]
                g.state = 2
                return
            ind += 1

    def check(self):
        return lang.check_word(self.ans)

    def back(self):
        if len(self.ans) > 0:
            ln = len(self.ans)
            l = self.ans[ln - 1:]
            self.ans = self.ans[:ln - 1]
            self.put_back(l)

    def put_back(self, letter):
        ind = 0
        for l in self.given:
            if l == letter:
                if self.taken[ind]:
                    self.taken[ind] = False
                    return
            ind += 1