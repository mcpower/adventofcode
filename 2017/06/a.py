#!/usr/bin/pypy3
from itertools import *
import math

USE_FILE = 1
if not USE_FILE:
    inp = r"""
0 2 7 0
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

l = list(map(int,inp.split()))



o = 0

seen = []
while tuple(l) not in seen:
    seen.append(tuple(l))
    q = list(l)
    i, x = max(enumerate(q), key=lambda a: (a[1], -a[0]))
    q[i] = 0
    for j in range(x):
        a = (i + j + 1) % len(q)
        q[a] += 1
    l = q
    #print(q)
print(len(seen) - seen.index(tuple(l)))