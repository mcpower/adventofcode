import sys; sys.dont_write_bytecode = True; from utils import *
"""
To do: ensure Code Runner works (in WSL), have preloaded the day and input in Chrome,
saved input into the folder, have utils on the side, collapse regions
Strings, lists, dicts:
lmap, ints, positive_ints, floats, positive_floats, words, keyvalues

Algorithms:
bisect, binary_search, hamming_distance, edit_distance

Data structures:
Linked, UnionFind
use deque for queue: q[0], q.append and q.popleft

List/Vector operations:
GRID_DELTA, OCT_DELTA
lget, lset, fst, snd
padd, pneg, psub, pmul, pdot, pdist1, pdist2sq, pdist2

Matrices:
matmat, matvec, matexp

Previous problems:
knot

Dict things:
dict.keys()
dict.values()
dict.items()
"""

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

def init_state(use_defaultdict=False):
    "If you use defaultdict you can't use any functions. Oops!"
    state = defaultdict(int) if use_defaultdict else dict()
    state["PC"] = 0
    state["HALT"] = False
    return state

def make_source(lines):
    def to_operation(line):
        l = line.split()
        for operation in operations:
            r = operation(*l)
            if r: return r
        return f"assert False, {repr(line)}"
    return list(map(to_operation, lines))

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
def addr(_, a, b, c):
    return f"r{c} = r{a} + r{b}"

@op()
@auto()
def addi(_, a, b, c):
    return f"r{c} = r{a} + {b}"


@op()
@auto()
def mulr(_, a, b, c):
    return f"r{c} = r{a} * r{b}"

@op()
@auto()
def muli(_, a, b, c):
    return f"r{c} = r{a} * {b}"

@op()
@auto()
def banr(_, a, b, c):
    return f"r{c} = r{a} & r{b}"

@op()
@auto()
def bani(_, a, b, c):
    return f"r{c} = r{a} & {b}"

@op()
@auto()
def borr(_, a, b, c):
    return f"r{c} = r{a} | r{b}"

@op()
@auto()
def bori(_, a, b, c):
    return f"r{c} = r{a} | {b}"


@op()
@auto()
def setr(_, a, b, c):
    return f"r{c} = r{a}"

@op()
@auto()
def seti(_, a, b, c):
    return f"r{c} = {a}"

@op()
@auto()
def gtir(_, a, b, c):
    return f"r{c} = int({a} > r{b})"

@op()
@auto()
def gtri(_, a, b, c):
    return f"r{c} = int(r{a} > {b})"

@op()
@auto()
def gtrr(_, a, b, c):
    return f"r{c} = int(r{a} > r{b})"

@op()
@auto()
def eqir(_, a, b, c):
    return f"r{c} = int({a} == r{b})"

@op()
@auto()
def eqri(_, a, b, c):
    return f"r{c} = int(r{a} == {b})"

@op()
@auto()
def eqrr(_, a, b, c):
    return f"r{c} = int(r{a} == r{b})"


def do_case(inp: str, sample=False):
    r1 = 0
    r4 = r1 | 65536
    r1 = 3798839
    seen = set()
    last = None
    while True:
        r1 = r1 + (r4 & 255)
        r1 = r1 & 16777215
        r1 = r1 * 65899
        r1 = r1 & 16777215
        if 256 > r4:
            if r1 in seen:
                print(last, r1)
                return
            seen.add(r1)
            last = r1
            r4 = r1 | 65536
            r1 = 3798839
            continue
        # set r4 to something and jump to line 9
        # r4 = max(0, ((r4 + 255) // 256) - 1)
        r4 >>= 8



    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    INSTRUCTION = ints(lines[0])[-1]
    print(INSTRUCTION)
    ops = lines[1:]

    source = make_source(ops)
    source = [line.replace(f"r{INSTRUCTION}", "PC") for line in source]
    print(*source,sep="\n\n")
    asd = None
    for x, i in enumerate(source):
        if "r0" in i:
            print("!!!", i)
            asd = x
    machine = compile_machine(source)

    state = init_state()

    for i in range(6):
        state[f"r{i}"] = 0
    # state[f"r0"] = 1
    count = 0
    while not state["HALT"]:
        
        cycle(machine, state)
        # print(state["r1"])
        if state["PC"] == asd:
            print(state["r1"])
            count += 1
            if count > 1000:
                return

    print(state["r0"])
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""],[
# Part 2
r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
