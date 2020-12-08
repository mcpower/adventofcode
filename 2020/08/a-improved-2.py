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

ACC = "acc"
NOP = "nop"
JMP = "jmp"

class InfiniteLoopError(Exception):
    pass

class Asm:
    def __init__(self, insts: typing.List[typing.List[str]]) -> None:
        self.insts = copy.deepcopy(insts)
        self.reset_state()
    
    def reset_state(self):
        self.pc = 0
        self.acc = 0
        self.seen_flow = set()
        self.cycles_run = 0

    def get_flow(self):
        "Returns everything needed to determine the current flow of the program."
        return self.pc
    
    def copy(self):
        return copy.deepcopy(self)

    def self_eval(self, s):
        return eval(s, None, self.__dict__)
    
    def parse_args(self, op: str, args: typing.List[str]):
        out = []
        for arg in args:
            parsed = None

            if arg.startswith(("+", "-")):
                parsed = int(arg)
            else:
                raise Exception(f"can't parse arg {arg} in {op} instruction")

            out.append(parsed)
        return out
    
    def cycle(self):
        if not 0 <= self.pc < len(self.insts):
            raise Exception(f"pc {self.pc} out of bounds [0, {len(self.insts)})")
        flow = self.get_flow()
        if flow in self.seen_flow:
            raise InfiniteLoopError
        self.seen_flow.add(flow)
        op, *args = self.insts[self.pc]
        args = self.parse_args(op, args)
        
        if op == ACC:
            a, = args
            self.acc += a
        elif op == JMP:
            a, = args
            self.pc += a
            self.pc -= 1
        elif op == NOP:
            a, = args
        else:
            raise Exception(f"Unknown operation {op}")
        
        self.pc += 1
        self.cycles_run += 1
    
    def run(self):
        while self.pc != len(self.insts):
            self.cycle()
    
    @classmethod
    def from_inp(cls, inp: str):
        return cls(lmap(str.split, inp.splitlines()))

    

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    
    asm = Asm.from_inp(inp)

    # part 1
    try:
        asm.run()
    except InfiniteLoopError:
        pass
    print("part 1:", asm.acc)
    asm.reset_state()
    
    # part 2
    SWAP = ["jmp", "nop"]
    for inst in asm.insts:
        op = inst[0]
        if op in SWAP:
            inst[0] = SWAP[op==SWAP[0]]
            try:
                asm.run()
            except InfiniteLoopError:
                pass
            else:
                print("part 2:", asm.acc)
            inst[0] = op
            asm.reset_state()

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
