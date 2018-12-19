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
            # if increment: out += "\nif not HALT: PC += 1"
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
    # print("!",s)
    # print(CONTEXT)
    # print(l)
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
    return f"r{c} = 1 if ({a} > r{b}) else 0"

@op()
@auto()
def gtri(_, a, b, c):
    return f"r{c} = 1 if (r{a} > {b}) else 0"

@op()
@auto()
def gtrr(_, a, b, c):
    return f"r{c} = 1 if (r{a} > r{b}) else 0"

@op()
@auto()
def eqir(_, a, b, c):
    return f"r{c} = 1 if ({a} == r{b}) else 0"

@op()
@auto()
def eqri(_, a, b, c):
    return f"r{c} = 1 if (r{a} == {b}) else 0"

@op()
@auto()
def eqrr(_, a, b, c):
    return f"r{c} = 1 if (r{a} == r{b}) else 0"


def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    INSTRUCTION = ints(lines[0])[-1]
    ops = lines[1:]

    source = make_source("\n".join(ops))
    print(*source,sep="\n")
    machine = compile_machine(source)

    state = init_state()

    # print(INSTRUCTION)

    for i in range(6):
        state[f"r{i}"] = 0
    # state[f"r0"] = 1

    while not state["HALT"]:
        sprint(state)
        state["r{}".format(INSTRUCTION)] = state["PC"]
        cont, _ = cycle(machine, state)
        # print(source[state["PC"]])
        if not cont:
            break
        state["PC"] = state["r{}".format(INSTRUCTION)]
        state["PC"] += 1
        if not 0 <= state["PC"] < len(source):
            break
        # print(state)
        # quit()


    print(state)
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
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
