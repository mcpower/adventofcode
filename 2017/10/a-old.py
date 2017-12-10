#!/usr/bin/pypy3
from itertools import *
import math

USE_FILE = 1
if not USE_FILE:
    input_num = 0
    inputs = []
    # 0
    inputs.append(r"""
3, 4, 1, 5
""".strip())
    # 1
    inputs.append(r"""

""".strip())
    # 2
    inputs.append(r"""

""".strip())
    # 3
    inputs.append(r"""

""".strip())
    # 4 
    inputs.append(r"""

""".strip())
    # 5
    inputs.append(r"""

""".strip())


    
    inp = list(filter(None, inputs))[-1]
    inp = inputs[input_num]
    n = 5
else:
    n = 256
    inp = open("input.txt").read().strip()

assert isinstance(inp, str)

lmap = lambda func, *iterables: list(map(func, *iterables))
splitf = lambda s, f=int: lmap(f,s.split())

lengths = lmap(int,inp.replace(" ","").split(","))

pos = 0
skip = 0

l = list(range(n))

for i in lengths:
    # print(l)
    # l[pos:pos+i] = l[pos:pos+i][::-1]
    positions = [x % n for x in range(pos, pos+i)]
    newpos = positions[::-1]
    # print(positions,newpos)
    newl = list(l)
    for x, y in zip(positions, newpos):
        # print(x,y)
        newl[x] = l[y]
    # print(newl)
    l = newl
    pos += i + skip
    skip += 1

out = l[0] * l[1]
# print(l)
print(out)
print(l)
