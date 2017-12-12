#!/usr/bin/pypy3
from pprint import pprint
from functools import reduce
import operator
lmap = lambda func, *iterables: list(map(func, *iterables))
splitf = lambda s, f=int: lmap(f,s.split())
def d(*a, **k):
    if DEBUG:
        print(*a, **k)

def dd(object):
    if DEBUG:
        pprint(object, compact=True)


DEBUG = 1

def do_case(inp: str, sample=False):
    l = inp.splitlines()
    n = len(l)
    adj = [[] for _ in range(n)]
    for i in l:
        q, w = i.split(" <-> ")
        adj[int(q)] = lmap(int,w.split(", "))
    

    blah = [None] * n
    cur = 0
    def dfs(i, v):
        if blah[i] is not None: return
        blah[i] = v
        for x in adj[i]:
            dfs(x, v)
    for i in range(n):
        if blah[i] is None:
            dfs(i, cur)
            cur += 1
    print(cur)
    return


samples = [
r"""
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""
]
samples = lmap(str.strip, samples)
while samples and not samples[-1]:
    samples.pop()

for sample in samples:
    print(f"running {repr(sample)[:100]}:")
    print("-"*10)
    do_case(sample, True)
    print("-"*10)
    print("#"*10)

try:
    actual_input = open("input.txt").read().strip()
except FileNotFoundError:
    actual_input = ""

if actual_input:
    print("running actual:")
    print("-"*10)
    do_case(actual_input, False)
    print("-"*10)
