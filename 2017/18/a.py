#!/usr/bin/pypy3
from pprint import pprint
from functools import reduce
import operator
import sys
sys.setrecursionlimit(100000)
lmap = lambda func, *iterables: list(map(func, *iterables))
splitf = lambda s, f=int: lmap(f,s.split())
def d(*a, **k):
    if DEBUG:
        print(*a, **k)

def dd(object):
    if DEBUG:
        pprint(object, compact=True)


DEBUG = 1

def knot(inp: str, binary=False) -> str:
    lengths = lmap(ord, inp) + [17, 31, 73, 47, 23]
    pos = skip = 0
    l = list(range(256))
    for _ in range(64):
        for i in lengths:
            positions = [x & 255 for x in range(pos, pos+i)]
            oldl = list(l)
            for x, y in zip(positions, reversed(positions)):
                l[x] = oldl[y]
            pos += i + skip
            skip += 1
    sparse = [reduce(operator.xor, l[i:i+16]) for i in range(0, 256, 16)]
    if binary:
        return "".join(bin(i)[2:].zfill(8) for i in sparse)
    else:
        return "".join(hex(i)[2:].zfill(2) for i in sparse)


def do_case(inp: str, sample=False):
    sprint = lambda *a, **k: sample and print(*a, **k)
    
    inst = inp.splitlines()

    from collections import defaultdict
    from collections import deque
    d0 = defaultdict(int)
    d1 = defaultdict(int)
    d0["p"] = 0
    d1["p"] = 1

    q0 = deque()
    q1 = deque()

    cur0 = 0
    cur1 = 0

    out = 0
    
    # d, cur, inqueue, outqueue
    def simulate(d, cur, inq, outq, p):
        nonlocal out
        c = inst[cur]
        a, *b = c.split()

        if a == "snd" or a == "rcv":
            y = b[0]
            
            if a == "snd":
                if p == 1:
                    out += 1
                if y.isalpha():
                    y = d[y]
                else:
                    y = int(y)
                outq.append(y)
            else:
                if inq:
                    d[y] = inq.popleft()
                else:
                    return d, cur, inq, outq, False
        else:
            x, y = b
            if y.isalpha():
                y = d[y]
            else:
                y = int(y)
            # if x.isdigit():
            #     x = int(x)
            # if y.is():
            #     y = int(y)
            # else:
            #     y = d[y]
            if a == "set":
                d[x] = y
            if a == "add":
                d[x] += y
            if a == "mul":
                d[x] *= y
            if a == "mod":
                d[x] %= y
            if a == "jgz":
                if x.isalpha():
                    if d[x] > 0:
                        cur += y
                        cur -= 1
                else:
                    if int(x) > 0:
                        cur += y
                        cur -= 1
        
        
        cur += 1
        return d, cur, inq, outq, True

    # while True:
    #     good = True
    #     count = 0
    #     while good:
    #         if not 0 <= cur0 < len(inst):
    #             print("0 broke")
    #             break
    #         d0, cur0, q0, q1, good = simulate(d0, cur0, q0, q1, 0)
    #         if good:
    #             count += 1
        
    #     # print(cur0, cur1, len(q0), len(q1))
    #     sprint(q0, q1)

    #     good = True
    #     count2 = 0
    #     while good:
    #         if not 0 <= cur1 < len(inst):
    #             print("1 broke")
    #             break
    #         d1, cur1, q1, q0, good = simulate(d1, cur1, q1, q0, 1)
    #         if good:
    #             count += 1
        

    
    #     print(cur0, cur1, len(q0), len(q1))
    #     sprint(q0, q1)
    #     if not count and not count2:
    #         break

    # print(d0, d1)
    while True:
        count0 = count1 = 0
        while 0 <= cur0 < len(inst):
            d0, cur0, q0, q1, good = simulate(d0, cur0, q0, q1, 0)
            if q1:
                count0 += 1
                break
            if not good:
                break
            count0 += 1

        while 0 <= cur1 < len(inst):
            d1, cur1, q1, q0, good = simulate(d1, cur1, q1, q0, 1)
            if q0:
                count1 += 1
                break
            if not good:
                break
            count1 += 1
        if count1 == 0 and count1 == 0:
            break



    print(out)
    return


samples = [
r"""
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
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
    print("running {}:".format(repr(sample)[:100]))
    print("-"*10)
    do_case(sample, True)
    print("-"*10)
    print("#"*10)

try:
    actual_input = open("input.txt").read().strip()
except FileNotFoundError:
    actual_input = ""

if actual_input:
    print("!! running actual: !!")
    print("-"*10)
    do_case(actual_input, False)
    print("-"*10)
