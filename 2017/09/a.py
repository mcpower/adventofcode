#!/usr/bin/pypy3
from itertools import *
import math

USE_FILE = 1
if not USE_FILE:
    inp = r"""
{{<!!>},{<!!>},{<!!>},{<!!>}}
""".strip()
    inp = r"""
{{<a!>},{<a!>},{<a!>},{<ab>}}
""".strip() or inp
    inp = r"""
{{<ab>},{<ab>},{<ab>},{<ab>}}
""".strip() or inp
    inp = r"""
<{o"i!a,<{i<a>
""".strip() or inp
else:
    inp = open("input.txt").read().strip()

assert isinstance(inp, str)

lmap = lambda func, *iterables: list(map(func, *iterables))
splitf = lambda s, f=int: lmap(f,s.split())



level = 0
is_garbage = False
ignore = False

out = 0

c = 0
for char in inp:
    if is_garbage:
        if ignore:
            ignore = False
            continue
        if char == '>':
            is_garbage = False
        elif char == '!':
            ignore = True
        else:
            c += 1
        continue
    
    if char == '{':
        level += 1
        continue
    if char == '}':
        out += level
        level -= 1
    if char == '<':
        is_garbage = True

assert(level == 0)
print(out)
print(c)