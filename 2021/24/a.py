import sys; sys.dont_write_bytecode = True; from utils import *

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
    # print(s)
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
def inp(_, a):
    return f"{a} = g()"

@op()
@auto()
def add(_, a, b):
    return f"{a} += {b}"


@op()
@auto()
def mul(_, a, b):
    return f"{a} *= {b}"

@op()
@auto()
def div(_, a, b):
    return f"{a} /= {b}"

@op()
@auto()
def mod(_, a, b):
    return f"{a} %= {b}"

@op()
@auto()
def eql(_, a, b):
    return f"{a} = int({a} == {b})"


def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    # INSTRUCTION = ints(lines[0])[-1]
    # print(INSTRUCTION)
    ops = lines

    source = make_source(ops)
    print("\n".join(source))
    return



run_samples_and_actual([
r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
