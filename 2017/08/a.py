#!/usr/bin/pypy3
from itertools import *
import math

USE_FILE = 1
if not USE_FILE:
    inp = r"""
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
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

reg = {}
# default 0

q = 0
for line in lines:
    var, ty, num, _, var2, op, cond = line.split()

    if eval("reg.get('{}',0) {} {}".format(var2, op, cond)):
        reg[var] = reg.get(var, 0) + (1 if ty == "inc" else -1) * int(num)
    q = max(q, reg.get(var, 0))
    

print(max(reg.values()))
print(q)