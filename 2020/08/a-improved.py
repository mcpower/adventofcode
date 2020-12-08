import sys; sys.dont_write_bytecode = True; from utils import *
"""
Strings, lists, dicts:
lmap, ints, positive_ints, floats, positive_floats, words

Data structures:
Linked, UnionFind
dict: d.keys(), d.values(), d.items()
deque: q[0], q.append and q.popleft

List/Vector operations:
GRID_DELTA, OCT_DELTA
lget, lset, fst, snd
padd, pneg, psub, pmul, pdot, pdist1, pdist2sq, pdist2

Matrices:
matmat, matvec, matexp
"""

from collections import defaultdict
import operator

operations = {}
CONTEXT = {"operator": operator}

PC = "PC"
HALT = "HALT"
RETURN = "RETURN"


def op(increment=True):
    def o(f):
        def wrapped(*a):
            try:
                res = f(*a)
            except TypeError:
                res = None
            lines = [line for line in res.splitlines() if line and not line.isspace()]
            if lines:
                i = 0
                while all(line[i:i+1].isspace() for line in lines): i += 1
                out = "\n".join(line[i:] for line in lines)
            else:
                out = ""
            if increment: out += f"\nif not {HALT}: PC += 1"
            return out
        operations[f.__name__.strip("_")] = wrapped
        return wrapped
    return o

def init_state(defaults=None, use_defaultdict=False):
    "If you use defaultdict you can't use any functions. Oops!"
    state = defaultdict(int) if use_defaultdict else dict()
    if defaults:
        state.update(defaults)
    state["PC"] = 0
    state["HALT"] = False
    return state

def lines_to_split(lines):
    return list(map(str.split, lines))

def split_to_source(split):
    def to_operation(l):
        a, *rest = l
        assert a in operations, f"instruction {a} not in operations"
        return operations[a](*rest)
    return list(map(to_operation, split))

def source_to_py(s):
    return [compile(i, "<string>", "exec") for i in s]

def split_to_py(split):
    return source_to_py(split_to_source(split))

def sexec(s, l):
    exec(s, CONTEXT, l)

def cycle(machine, state):
    "Returns HALT, RETURN."
    if not 0 <= state[PC] < len(machine):
        state[HALT] = True
    if state[HALT]: return True, None
    state[RETURN] = None
    sexec(machine[state[PC]], state)
    return state[HALT], state[RETURN]

ACC = "acc"

@op()
def acc(a: str):
    return f"{ACC} += {a}"

@op(increment=False)
def jmp(a: str):
    return f"{PC} += {a}"

@op()
def nop(a: str):
    return ""

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()

    start_state = init_state(defaults={"acc": 0})

    split = lines_to_split(lines)

    # part 1
    machine = split_to_py(split)
    state = copy.copy(start_state)
    seen = set()
    while True:
        cur_pc = state[PC]
        if cur_pc in seen:
            print("part 1:", state[ACC])
            break
        seen.add(cur_pc)

        halted, returned = cycle(machine, state)
    
    # part 2
    def run(split):
        machine = split_to_py(split)
        state = copy.copy(start_state)
        seen = set()
        halted = False
        while not halted:
            cur_pc = state[PC]
            if cur_pc in seen:
                return None
            seen.add(cur_pc)

            
            halted, returned = cycle(machine, state)
        return state[ACC]
    
    for s in split:
        if s[0] == "nop":
            s[0] = "jmp"
            q = run(split)
            if q:
                print("part 2:", q)
            s[0] = "nop"
        if s[0] == "jmp":
            s[0] = "nop"
            q = run(split)
            if q:
                print("part 2:", q)
            s[0] = "jmp"
    

    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6

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
