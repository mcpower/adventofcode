#!/usr/bin/pypy3
from itertools import *
import math

USE_FILE = 1
if not USE_FILE:
    inp = r"""
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
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

nums = {}
adj = {}
antiadj = {}

for line in lines:
    a = []
    if "->" in line:
        line, rest = line.split(" -> ")
        a = rest.split(", ")
    
    line, r = line.split(" (")
    r = r.strip(")")
    nums[line] = int(r)
    adj[line] = a
    antiadj.setdefault(line, [])
    for i in a:
        antiadj.setdefault(i, []).append(line)


for x in antiadj:
    if not antiadj[x]:
        print(x)
