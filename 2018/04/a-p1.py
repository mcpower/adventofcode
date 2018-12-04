import collections
import functools
import itertools
import math
import operator
import re
import sys
from collections import Counter, defaultdict, deque
from functools import reduce
from pprint import pprint
from typing import List
def knot(inp: str, binary: bool=False) -> str:
    lengths = lmap(ord, inp) + [17, 31, 73, 47, 23]; pos = skip = 0; l = list(range(256))
    for _ in range(64):
        for i in lengths:
            positions = [x & 255 for x in range(pos, pos+i)]; oldl = list(l)
            for x, y in zip(positions, reversed(positions)): l[x] = oldl[y]
            pos += i + skip; skip += 1
    sparse = [reduce(operator.xor, l[i:i+16]) for i in range(0, 256, 16)]
    return "".join(bin(i)[2:].zfill(8) if binary else hex(i)[2:].zfill(2) for i in sparse)
sys.setrecursionlimit(100000)
GRID_DELTA = [[-1, 0], [1, 0], [0, -1], [0, 1]]; OCT_DELTA = [[1, 1], [-1, -1], [1, -1], [-1, 1]] + GRID_DELTA
def padd(x, y): return [a+b for a, b in zip(x, y)]
def pneg(v): return [-i for i in v]
def psub(x, y): return [a-b for a, b in zip(x, y)]
def pmul(m: int, v): return [m * i for i in v]
def pdot(x, y): return sum(a*b for a, b in zip(x, y))
def pnorm1(v): return sum(map(abs, v))
def pnorm2sq(v): return sum(i*i for i in v)
def pnorm2(v): return math.sqrt(pnorm2sq(v))
def lget(l, i):
    if isinstance(i, int): return l[i]
    for index in i: l = l[index]
    return l
def lset(l, i, v):
    if isinstance(i, int): l[i] = v
    for index in i[:-1]: l = l[index]
    l[i[-1]] = v

def lmap(func, *iterables): return list(map(func, *iterables))
def ints(s: str) -> List[int]: return lmap(int, re.findall(r"\d+", s))  # thanks mserrano!
def floats(s: str) -> List[float]: return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))
def words(s: str) -> List[str]: return re.findall(r"[a-zA-Z]+", s)

def matmat(a, b):
    n, k1 = len(a), len(a[0]); k2, m = len(b), len(b[0]); assert k1 == k2; out = [[None] * m for _ in range(n)]
    for i in range(n):
        for j in range(m): out[i][j] = sum(a[i][k] * b[k][j] for k in range(k1))
    return out
def matvec(a, v): return [j for i in matmat(a, [[x] for x in v]) for j in i]
def matexp(a, k):
    n = len(a); out = [[int(i==j) for j in range(n)] for i in range(n)]
    while k > 0:
        if k % 2 == 1: out = matmat(a, out)
        a = matmat(a, a); k //= 2
    return out

BLANK = object()
def hamming(a, b) -> int: return sum(i is BLANK or j is BLANK or i != j for i, j in itertools.zip_longest(a, b, fillvalue=BLANK))
def edit(a, b) -> int:
    n = len(a); m = len(b); dp = [[None] * (m+1) for _ in range(n+1)]; dp[n][m] = 0
    def aux(i, j):
        assert 0 <= i <= n and 0 <= j <= m
        if dp[i][j] is not None: return dp[i][j]
        if i == n: dp[i][j] = 1 + aux(i, j+1)
        elif j == m: dp[i][j] = 1 + aux(i+1, j)
        else: dp[i][j] = min((a[i] != b[j]) + aux(i+1, j+1), 1 + aux(i+1, j), 1 + aux(i, j+1))
        return dp[i][j]
    return aux(0, 0)



def do_case(inp: str, sample=False):
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    lines.sort()
    d = {}
    freqs = {}
    def get_max(s):
        return max((s[a], a) for a in s)
    cur_guard = None
    last_time = None
    for line in lines:
        sprint(line)
        year, month, day, hour, minute, *guard = ints(line)
        minutes = minute + 60 * (hour + 24 * (day))
        if guard:
            g = guard[0]
            cur_guard = g
            if g not in d:
                d[g] = 0
                # minute: thing
                freqs[g] = {i: 0 for i in range(60)}
        else:
            if "falls" in line:
                # stop
                last_time = minutes
            else:
                d[cur_guard] += minutes - last_time
                last_minute = last_time % 60
                for i in range(last_minute, minute):
                    freqs[cur_guard][i] += 1
    print(d)
    s = max((get_max(freqs[i]), i) for i in freqs)
    print(s)
    # quit()
    print(s[1] * s[0][1])
    


    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



def parse_samples(l):
    samples = lmap(str.strip, l)
    while samples and not samples[-1]: samples.pop()
    return samples
# Part 1
samples = parse_samples([
r"""
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""
])

# Part 2
samples = parse_samples([
r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""
]) or samples

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
