#!/usr/bin/python
# Letters.py
"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""

import sys
from gi.repository import Gtk
import pygame
from gettext import gettext as _

import g
import utils
import load_save
import let
import buttons
import letter_keys


class Letters:

    def __init__(self, colors, sugar=False):
        self.colors = colors[:]
        self.sugar = sugar
        self.journal = True  # set to False if we come in via main()
        self.canvas = None
        self.new_button = None
        self.tick_button = None
        self.back_button = None
        self.label = None

    def set_buttons(self, new, tick, back):
        ''' Sugar toolbar buttons '''
        self.new_button = new
        self.tick_button = tick
        self.back_button = back

    def set_label(self, label):
        ''' Sugar toolbar label '''
        self.label = label

    def display(self):
        g.screen.fill(self.colors[1])
        if not self.sugar:
            g.screen.blit(g.bgd, (g.sx(0), 0))
        self.let.draw()
        if self.sugar:
            self.back_button.set_sensitive(False)
            self.tick_button.set_sensitive(False)
        else:
            buttons.off(['back', 'tick'])
        if g.state in (2, 4):
            if len(self.let.ans) > 0:
                if self.sugar:
                    self.back_button.set_sensitive(True)
                else:
                    buttons.on('back')
            if len(self.let.ans) > 1:
                if self.sugar:
                    self.tick_button.set_sensitive(True)
                else:
                    buttons.on('tick')
        buttons.draw()
        #utils.display_number(g.state,(10,10),g.font1)
        if g.state == 3:
            ln = len(self.let.ans)
            if ln == 2:
                s = _('Your word scores one point.')
            else:
                s = _('Your word scores %s points.' % (str(2 ** (ln - 2))))
            utils.text_blit(g.screen, s, g.font2, g.message_cxy,
                            self.colors[0], False)
        if g.state == 4:
            s = _('Sorry, %s is not in my word list' % self.let.ans)
            utils.text_blit(g.screen, s, g.font2, g.message_cxy,
                            self.colors[0], False)
        if self.sugar:
            self.label.set_markup(
                '<span><big><b> %s (%s)</b></big></span>' % (str(g.score),
                                                             str(g.best)))
        else:
            if g.score > 0:
                s = _('Total: %s' % (str(g.score)))
                utils.text_blit(g.screen, s, g.font1, g.score_cxy,
                                self.colors[0], False)
            if g.best > 0:
                s = _('Best: %s' % (str(g.best)))
                utils.text_blit(g.screen, s, g.font1, g.best_cxy,
                                self.colors[0], False)
        if g.help_on:
            utils.centre_blit(g.screen, g.help_img, g.help_cxy)

    def do_click(self):
        if g.state in (2, 4):
            if self.let.click():
                g.state = 2

    def do_button(self, bu):
        if bu == 'new':
            if not self.let.check():
                if g.score > 0:
                    g.score -= 1
            self.let.setup()
            g.state = 1
            return
        if bu == 'back':
            self.let.reset()
            g.state = 2
            return
        if bu == 'tick':
            self.do_tick()
            return
        if bu == 'help':
            g.help_on = True
            if not self.sugar:
                buttons.off('help')

    def do_tick(self):
        if g.state == 2:
            if self.let.check():
                g.state = 3
                g.score += (2 ** (len(self.let.ans) - 2))
                if g.score > g.best:
                    g.best = g.score
            else:
                g.state = 4

    def do_key(self, key):
        if key == pygame.K_1:
            g.version_display = not g.version_display
            return
        if key in g.CROSS:
            self.do_click()
            return
        if key in g.CIRCLE:
            if g.help_on:
                if not self.sugar:
                    g.help_on = False
                    buttons.on('help')
                return
            else:
                if not self.sugar:
                    g.help_on = True
                    buttons.off('help')
                return
        if key in g.SQUARE:
            self.do_button('new')
            return
        if key in g.UP:
            if g.state in (2, 4):
                self.do_button('back')
            return
        if key in g.LEFT:
            self.let.left()
            return
        if key in g.RIGHT:
            self.let.right()
            return
        if key in g.TICK:
            if len(self.let.ans) > 1:
                self.do_tick()
            return
        #if key==pygame.K_4: self.let.given='clangers'; return###
        if g.state in (2, 4):
            letter = letter_keys.which(key)
            if letter is not None:
                self.let.key(letter)
                return
            if key == pygame.K_BACKSPACE:
                g.state = 2
                self.let.back()
                return

    def buttons_setup(self):
        if self.sugar:
            self.tick_button.set_sensitive(False)
            self.back_button.set_sensitive(False)
            return
        dx = g.sy(4)
        cx = g.sx(16) - 1.5 * dx
        cy = g.sy(15)
        buttons.Button('new', (cx, cy))
        cx += dx
        buttons.Button('tick', (cx, cy))
        cx += dx
        buttons.off('tick')
        buttons.Button('back', (cx, cy))
        cx += dx
        buttons.off('back')
        buttons.Button('help', (cx, cy))

    def flush_queue(self):
        flushing = True
        while flushing:
            flushing = False
            if self.journal:
                while Gtk.events_pending():
                    Gtk.main_iteration()
            for event in pygame.event.get():
                flushing = True

    def run(self, restore=False):
        g.init()
        if not self.journal:
            utils.load()
        self.let = let.Let()
        # setup before retrieve
        load_save.retrieve()
        self.buttons_setup()
        if self.canvas is not None:
            self.canvas.grab_focus()
        ctrl = False
        pygame.key.set_repeat(600, 120)
        key_ms = pygame.time.get_ticks()
        going = True
        while going:
            if self.journal:
                # Pump GTK messages.
                while Gtk.events_pending():
                    Gtk.main_iteration()
            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if not self.journal:
                        utils.save()
                    going = False
                elif event.type == pygame.MOUSEMOTION:
                    g.pos = event.pos
                    g.redraw = True
                    if self.canvas is not None:
                        self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw = True
                    if event.button == 1:
                        if not self.sugar and g.help_on:
                            g.help_on = False
                            buttons.on('help')
                        elif self.do_click():
                            pass
                        else:
                            bu = buttons.check()
                            if bu != '':
                                self.do_button(bu)
                                self.flush_queue()
                    if not self.sugar and event.button == 3:
                        g.help_on = True
                        buttons.off('help')
                elif event.type == pygame.KEYDOWN:
                    if not self.sugar and event.key not in g.CIRCLE:
                        g.help_on = False
                        buttons.on('help')
                    # throttle keyboard repeat
                    if pygame.time.get_ticks() - key_ms > 110:
                        key_ms = pygame.time.get_ticks()
                        if ctrl:
                            if event.key == pygame.K_q:
                                if not self.journal:
                                    utils.save()
                                going = False
                                break
                            else:
                                ctrl = False
                        if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                            ctrl = True
                            break
                        self.do_key(event.key)
                        g.redraw = True
                        self.flush_queue()
                elif event.type == pygame.KEYUP:
                    ctrl = False
            if not going:
                break

            if g.state == 1:
                self.let.choose()
            if g.redraw:
                self.display()
                if g.version_display:
                    utils.version_display()
                if g.state != 1:
                    g.screen.blit(g.pointer, g.pos)
                pygame.display.flip()
                g.redraw = False
            g.clock.tick(40)

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((1024, 768), pygame.FULLSCREEN)
    game = Letters(([0, 0, 0], [255, 255, 255]))
    game.journal = False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
