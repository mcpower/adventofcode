#!/usr/bin/pypy3
from pprint import pprint
from functools import reduce
import operator
import sys
from collections import defaultdict, deque
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

operations = []
CONTEXT = {"operator": operator}

def op(increment=True):
    def o(f):
        def wrapped(*a):
            try:
                res = f(*a)
            except TypeError:
                res = None
            if not res: return
            lines = [line for line in res.splitlines() if line and not line.isspace()]
            i = 0
            while all(line[i:i+1].isspace() for line in lines): i += 1
            out = "\n".join(line[i:] for line in lines)
            if increment: out += "\nif not HALT: PC += 1"
            return out
        operations.append(wrapped)
        return wrapped
    return o

def auto(pos=0):
    def o(f):
        n = f.__name__.strip("_")
        def wrapped(*a):
            if not 0 <= pos < len(a): return
            if a[pos] != n: return
            return f(*a)
        return wrapped
    return o

def init_state():
    state = defaultdict(int)
    state["PC"] = 0
    state["HALT"] = False
    return state

def make_source(s):
    def to_operation(line):
        l = line.split()
        for operation in operations:
            r = operation(*l)
            if r: return r
        return "assert False"
    return list(map(to_operation, s.strip().splitlines()))

def compile_machine(s):    
    return [compile(i, "<string>", "exec") for i in s]

def sexec(s, l):
    exec(s, CONTEXT, l)

def cycle(machine, state):
    if not 0 <= state["PC"] < len(machine):
        state["HALT"] = True
    if state["HALT"]: return False, None
    state["RETURN"] = None
    sexec(machine[state["PC"]], state)
    return not state["HALT"], state["RETURN"]

@op()
@auto()
def snd(_, x):
    return f"""
OUTQ.append({x})
RETURN = True
OUT += 1
"""

@op()
@auto()
def set_(_, x, y):
    return f"{x} = {y}"

@op()
@auto()
def add(_, x, y):
    return f"{x} += {y}"

@op()
@auto()
def mul(_, x, y):
    return f"{x} *= {y}"

@op()
@auto()
def mod(_, x, y):
    return f"{x} %= {y}"

@op()
@auto()
def rcv(_, x):
    return f"""
if INQ:
    {x} = INQ.popleft()
else:
    HALT = True
"""

@op()
@auto()
def jgz(_, x, y):
    return f"""
    if {x} > 0:
        PC += {y}
        PC -= 1
    """

def do_case(inp: str, sample=False):
    sprint = lambda *a, **k: sample and print(*a, **k)
    
    source = make_source(inp)
    machine = compile_machine(source)
    s0 = init_state()
    s1 = init_state()

    q0 = deque()
    q1 = deque()
    s0["INQ"] = s1["OUTQ"] = q0
    s0["OUTQ"] = s1["INQ"] = q1

    s0["p"] = 0
    s1["p"] = 1
    while not (s0["HALT"] and s1["HALT"]):
        while not s0["HALT"]:
            _, sent = cycle(machine, s0)
            if sent:
                s1["HALT"] = False
        while not s1["HALT"]:
            _, sent = cycle(machine, s1)
            if sent:
                s0["HALT"] = False
    print(s1["OUT"])
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

# if False:
if actual_input:
    print("!! running actual: !!")
    print("-"*10)
    do_case(actual_input, False)
    print("-"*10)
