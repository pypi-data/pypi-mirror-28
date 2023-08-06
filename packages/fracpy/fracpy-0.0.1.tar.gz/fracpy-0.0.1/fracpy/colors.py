import numpy as np


GREEN = np.array([0, 255, 0])
RED = np.array([255, 0, 0])
BLUE = np.array([0, 0, 255])

SKY = np.array([179, 225, 242], dtype=np.float32)
PINKY = np.array([255, 170, 221], dtype=np.float32)

SKY /= 255.
PINKY /= 255.


def linear(*, color_from, color_to, zigzag=1):
    assert zigzag > 0
    assert type(zigzag) == int

    col_f = np.array(color_from)
    col_t = np.array(color_to)

    def simple_linear(x):
        return (1 - x) * col_f + x * col_t

    if zigzag == 1:
        return simple_linear

    def zigzag_linear(x):
        mult = x * zigzag
        chunk = int(mult)
        shifted = mult - chunk
        if chunk % 2 == 0:
            return simple_linear(shifted)
        else:
            return simple_linear(1. - shifted)

    return zigzag_linear


def func(f_r, f_g, f_b):
    def f(x):
        return np.array([f_r(x), f_g(x), f_b(x)])
    return f


def sinusoidal(col):
    pass

"""
def color_sin_small(x):
    return [sin(x * pi * 512) ** 2, 0, cos(x * pi * 512) ** 2]


def color_sin(x):
    return [sin(x * pi / 2) ** 2, 0, cos(x * pi / 2) ** 2]
"""

def color3(x):
    x = (3 * x + .5) % 3
    if x < 1:
        return [x, 0, 1 - x]
    elif x < 2:
        x -= 1
        return [1 - x, x, 0]
    else:
        x -= 2
        return [0, 1 - x, x]


'''
switch = -1
def color_switch(x):
    global switch
    switch = (switch + 1) % 3
    if switch == 0:
        return [0, 0, 1]
    elif switch == 1:
        return [0, 1, 0]
    elif switch == 2:
        return [1, 0, 0]
'''
