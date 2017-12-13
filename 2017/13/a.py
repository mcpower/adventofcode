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
    d = {}
    for x in l:
        a, b = x.split(": ")
        d[int(a)] = int(b)
    q = max(d.keys())
    def test(qqq):
        cur = dict(d)
        for j in d:
            cur[j] = qqq
            cur[j] %= 2*(d[j] - 1)
        # cur * 2
        state = 0
        out = 0
        for i in range(q+1):
            dd = False
            if i in cur and cur[i] == 0:
                out += i * d[i]
                dd = True
                if sample: print("!")
                return False
            # print(i)
            if sample:
                print(i, cur)
            for j in d:
                cur[j] += 1
                cur[j] %= 2*(d[j] - 1)
        return True
        
        # if i in cur and cur[i] == 0 and not dd:
        #     out += i * d[i]
        #     if sample: print("!!")
    for i in range(100000000):
        if test(i):
            print(i)
            return
        
    print(out)
    return


samples = [
r"""
0: 3
1: 2
4: 4
6: 4
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
