"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import pygame

# letter_keys
d = {pygame.K_a: 'a',
     pygame.K_b: 'b',
     pygame.K_c: 'c',
     pygame.K_d: 'd',
     pygame.K_e: 'e',
     pygame.K_f: 'f',
     pygame.K_g: 'g',
     pygame.K_h: 'h',
     pygame.K_i: 'i',
     pygame.K_j: 'j',
     pygame.K_k: 'k',
     pygame.K_l: 'l',
     pygame.K_m: 'm',
     pygame.K_n: 'n',
     pygame.K_o: 'o',
     pygame.K_p: 'p',
     pygame.K_q: 'q',
     pygame.K_r: 'r',
     pygame.K_s: 's',
     pygame.K_t: 't',
     pygame.K_u: 'u',
     pygame.K_v: 'v',
     pygame.K_w: 'w',
     pygame.K_x: 'x',
     pygame.K_y: 'y',
     pygame.K_z: 'z'}


def which(key):
    if key in d:
        return d[key]
    else:
        return None
