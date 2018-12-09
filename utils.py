#region Imports
import collections
import functools
import itertools
import math
import operator
import re
import sys
import typing
from collections import Counter, defaultdict, deque
from functools import reduce
from pprint import pprint
from typing import List
#endregion

sys.setrecursionlimit(100000)
# Copy a function if you need to modify it.

#region Strings, lists, dicts
def lmap(func, *iterables):
    return list(map(func, *iterables))

def ints(s: str) -> List[int]:
    return lmap(int, re.findall(r"-?\d+", s))  # thanks mserrano!
def positive_ints(s: str) -> List[int]:
    return lmap(int, re.findall(r"\d+", s))  # thanks mserrano!
def floats(s: str) -> List[float]:
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))
def positive_floats(s: str) -> List[float]:
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))
def words(s: str) -> List[str]:
    return re.findall(r"[a-zA-Z]+", s)

def keyvalues(d):
    return list(d.items())  # keep on forgetting this...
#endregion

#region Algorithms
def bisect(f, lo=0, hi=None, eps=1e-9):
    """
    Returns a value x such that f(x) is true.
    Based on the values of f at lo and hi.
    Assert that f(lo) != f(hi).
    """
    lo_bool = f(lo)
    if hi is None:
        hi = 1
        while f(hi) == lo_bool:
            hi *= 2
    else:
        assert f(hi) != lo_bool
    while hi - lo > eps:
        mid = (hi + lo) / 2
        if f(mid) == lo_bool:
            lo = mid
        else:
            hi = mid
    if lo_bool:
        return lo
    else:
        return hi

def binary_search(f, lo=0, hi=None):
    """
    Returns a value x such that f(x) is true.
    Based on the values of f at lo and hi.
    Assert that f(lo) != f(hi).
    """
    lo_bool = f(lo)
    if hi is None:
        hi = 1
        while f(hi) == lo_bool:
            hi *= 2
    else:
        assert f(hi) != lo_bool
    best_so_far = lo if lo_bool else hi
    while lo <= hi:
        mid = (hi + lo) // 2
        result = f(mid)
        if result:
            best_so_far = mid
        if result == lo_bool:
            lo = mid + 1
        else:
            hi = mid - 1
    return best_so_far

# Distances
BLANK = object()
def hamming_distance(a, b) -> int:
    return sum(i is BLANK or j is BLANK or i != j for i, j in itertools.zip_longest(a, b, fillvalue=BLANK))
def edit_distance(a, b) -> int:
    n = len(a)
    m = len(b)
    dp = [[None] * (m+1) for _ in range(n+1)]
    dp[n][m] = 0
    def aux(i, j):
        assert 0 <= i <= n and 0 <= j <= m
        if dp[i][j] is not None:
            return dp[i][j]
        if i == n:
            dp[i][j] = 1 + aux(i, j+1)
        elif j == m:
            dp[i][j] = 1 + aux(i+1, j)
        else:
            dp[i][j] = min((a[i] != b[j]) + aux(i+1, j+1), 1 + aux(i+1, j), 1 + aux(i, j+1))
        return dp[i][j]
    return aux(0, 0)
#endregion

#region Data Structures
T = typing.TypeVar("T")
class Linked(typing.Generic[T], typing.Iterable[T]):
    """
    Represents a node in a doubly linked lists.

    Can also be interpreted as a list itself.
    Consider this to be first in the list.
    """
    # item: T
    # forward: "Linked[T]"
    # backward: "Linked[T]"
    def __init__(self, item: T) -> None:
        self.item = item
        self.forward = self
        self.backward = self

    def _join(self, other: "Linked[T]") -> None:
        self.forward = other
        other.backward = self
    
    def concat(self, other: "Linked[T]") -> None:
        """
        Concatenates other AFTER THE END OF THE LIST,
        i.e. before this current node.
        """
        first_self = self
        last_self = self.backward

        first_other = other
        last_other = other.backward
        # self ++ other
        # consider last_self and first_other
        last_self._join(first_other)
        last_other._join(first_self)
    
    def concat_immediate(self, other: "Linked[T]") -> None:
        """
        Concatenates other IN THE "SECOND" INDEX OF THE LIST
        i.e. after this current node.
        """
        self.forward.concat(other)
    
    def append(self, val: T) -> None:
        """
        Appends an item AFTER THE END OF THE LIST,
        i.e. before this current node.
        """
        self.concat(Linked(val))
    
    def append_immediate(self, val: T) -> None:
        """
        Appends an item IN THE "SECOND" INDEX OF THE LIST
        i.e. after this current node.
        """
        self.concat_immediate(Linked(val))
    
    def delete(self) -> None:
        """
        Deletes this node.
        After this is called, you should never use this node.
        """
        forward = self.forward
        backward = self.backward
        forward.backward = backward
        backward.forward = forward
    
    def move(self, n: int) -> "Linked[T]":
        """
        Move n nodes forward, or backwards if n is negative.
        """
        out = self
        if n >= 0:
            for _ in range(n):
                out = out.forward
        else:
            for _ in range(-n):
                out = out.backward
        return out
    
    def iterate_nodes_inf(self) -> typing.Iterator["Linked[T]"]:
        cur = self
        while True:
            yield cur
            cur = cur.forward
    
    def iterate_nodes(self, count=1) -> typing.Iterator["Linked[T]"]:
        for node in self.iterate_nodes_inf():
            if node is self:
                count -= 1
                if count < 0:
                    break
            yield node
    
    def iterate_inf(self) -> typing.Iterator[T]:
        return map(lambda node: node.item, self.iterate_nodes_inf())
    
    def iterate(self, count=1) -> typing.Iterator[T]:
        return map(lambda node: node.item, self.iterate_nodes(count))
    
    def to_list(self):
        return list(self.iterate())
    
    def check_correctness(self) -> None:
        assert self.forward.backward is self
        assert self.backward.forward is self
    
    def check_correctness_deep(self) -> None:
        for node in self.iterate_nodes():
            node.check_correctness()
    
    def __iter__(self) -> typing.Iterator[T]:
        return self.iterate()
    
    def __repr__(self) -> str:
        return "Linked({})".format(self.to_list())

    @classmethod
    def from_list(cls, l: typing.Iterable[T]) -> "Linked[T]":
        it = iter(l)
        out = cls(next(it))
        for i in it:
            out.concat(cls(i))
        return out
#endregion

#region List/Vector operations
GRID_DELTA = [[-1, 0], [1, 0], [0, -1], [0, 1]]
OCT_DELTA = [[1, 1], [-1, -1], [1, -1], [-1, 1]] + GRID_DELTA
def lget(l, i):
    if len(l) == 2: return l[i[0]][i[1]]
    for index in i: l = l[index]
    return l
def lset(l, i, v):
    if len(l) == 2:
        l[i[0]][i[1]] = v
        return
    for index in i[:-1]: l = l[index]
    l[i[-1]] = v
def fst(x):
    return x[0]
def snd(x):
    return x[1]

def padd(x, y):
    if len(x) == 2: return [x[0] + y[0], x[1] + y[1]]
    return [a+b for a, b in zip(x, y)]
def pneg(v):
    if len(v) == 2: return [-v[0], -v[1]]
    return [-i for i in v]
def psub(x, y):
    if len(x) == 2: return [x[0] - y[0], x[1] - y[1]]
    return [a-b for a, b in zip(x, y)]
def pmul(m: int, v):
    if len(v) == 2: return [m * v[0], m * v[1]]
    return [m * i for i in v]
def pdot(x, y):
    if len(x) == 2: return x[0] * y[0] + x[1] * y[1]
    return sum(a*b for a, b in zip(x, y))
def pdist1(x, y=None):
    if y is not None: x = psub(x, y)
    if len(x) == 2: return abs(x[0]) + abs(x[1])
    return sum(map(abs, x))
def pdist2sq(x, y=None):
    if y is not None: x = psub(x, y)
    if len(x) == 2: return (x[0] * x[0]) + (x[1] * x[1])
    return sum(i*i for i in x)
def pdist2(v):
    return math.sqrt(pdist2sq(v))
#endregion

#region Matrices
def matmat(a, b):
    n, k1 = len(a), len(a[0])
    k2, m = len(b), len(b[0])
    assert k1 == k2
    out = [[None] * m for _ in range(n)]
    for i in range(n):
        for j in range(m): out[i][j] = sum(a[i][k] * b[k][j] for k in range(k1))
    return out
def matvec(a, v):
    return [j for i in matmat(a, [[x] for x in v]) for j in i]
def matexp(a, k):
    n = len(a)
    out = [[int(i==j) for j in range(n)] for i in range(n)]
    while k > 0:
        if k % 2 == 1: out = matmat(a, out)
        a = matmat(a, a)
        k //= 2
    return out
#endregion

#region Previous problems
def knot(inp: str, binary: bool=False) -> str:
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
    return "".join(bin(i)[2:].zfill(8) if binary else hex(i)[2:].zfill(2) for i in sparse)
#endregion



#region Running
def parse_samples(l):
    samples = lmap(str.strip, l)
    while samples and not samples[-1]: samples.pop()
    return samples

def run_samples_and_actual(part1, part2, do_case):
    p1 = parse_samples(part1)
    p2 = parse_samples(part2)
    for sample in p2 or p1:
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
#endregion
