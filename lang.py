"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import os
import random
import logging

LETTERS = 'EEEEEEEEEEEEAAAAAAAAAIIIIIIIIIOOOOOOOONNNNNNRRRRRRTTTTTTLLLLSSS'\
'SUUUUDDDDGGGBBCCMMPPFFHHVVWWYYKJXQZ'
letters = LETTERS.lower()
filehandle = [None] * 9


# checks word (2 to 8 letters) -> True/False
def check_word(w):
    l = len(w)
    if l < 2 or l > 8:
        return False
    fname = os.path.join('data', str(l) + '.txt')
    f = filehandle[l]
    if f is None:
        try:
            f = open(fname, 'r')
        except Exception as e:
            logging.error("Couldn't open %s: %s" % (fname, e))
            return False
        filehandle[l] = f
    p1 = 0
    p2 = int(os.path.getsize(fname) / (l + 2))
    w0 = w.lower()
    while True:
        q1 = p1
        q2 = p2
        p = int((p1 + p2) / 2)
        f.seek(p * (l + 2))
        w1 = f.read(l)
        if w0 == w1:
            return True
        if w0 < w1:
            p2 = p
        else:
            p1 = p
        if (q1 == p1) and (q2 == p2):
            return False


def letter():
    r = random.randint(0, len(letters) - 1)
    return letters[r]


def vowel():
    l = 'x'
    while l not in 'aeiou':
        l = letter()
    return l


def consonant():
    l = 'a'
    while l in 'aeiou':
        l = letter()
    return l
