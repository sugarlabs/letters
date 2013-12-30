#load_save.py
import g

loaded = []  # list of strings


def load(f):
    global loaded
    try:
        for line in f.readlines():
            loaded.append(line)
    except:
        pass


def save(f):
    f.write(str(g.best) + '\n')


# note need for rstrip() on strings
def retrieve():
    global loaded
    if len(loaded) > 0:
        g.best = int(loaded[0])