#!/usr/bin/python3
from itertools import *
import math

USE_FILE = 1
if not USE_FILE:
    inp = r"""
0
3
0
1
-3
""".strip()
    inp = r"""

""".strip() or inp
    inp = r"""

""".strip() or inp
    inp = r"""

""".strip() or inp
    inp = r"""

""".strip() or inp
else:
    inp = open("input.txt").read().strip()

assert isinstance(inp, str)

lines = inp.splitlines()

o = 0

i = 0
steps = 0
l = list(map(int, lines))
while 0 <= i < len(l):
    off = l[i]
    oldi = i
    i += l[i]
    if off >= 3:
        l[oldi] -= 1
    else:
        l[oldi] += 1
    steps += 1

print(steps)
