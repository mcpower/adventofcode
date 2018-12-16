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

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()

    part1 = []
    part2 = []
    asd = []
    empty = 0
    is_part2 = False
    for line in lines:
        if not line:
            empty += 1
            if empty == 3:
                print("!")
                is_part2 = True
            continue
        empty = 0
        if is_part2:
            part2.append(ints(line))
        else:
            asd.append(ints(line))
            if len(asd) == 3:
                part1.append(asd)
                asd = []
    
    def add(reg, a, b, c, imm=False):
        out = list(reg)
        out[c] = reg[a] + (b if imm else reg[b])
        return out
    def mul(reg, a, b, c, imm=False):
        out = list(reg)
        out[c] = reg[a] * (b if imm else reg[b])
        return out
    def ban(reg, a, b, c, imm=False):
        out = list(reg)
        out[c] = reg[a] & (b if imm else reg[b])
        return out
    def bor(reg, a, b, c, imm=False):
        out = list(reg)
        out[c] = reg[a] | (b if imm else reg[b])
        return out
    def set_(reg, a, b, c, imm=False):
        out = list(reg)
        out[c] = a if imm else reg[a]
        return out
    def gt(reg, a, b, c, imm1=False, imm2=False):
        out = list(reg)
        first_val = a if imm1 else reg[a]
        second_val = b if imm2 else reg[b]
        out[c] = int(first_val > second_val)
        return out
    def eq(reg, a, b, c, imm1=False, imm2=False):
        out = list(reg)
        first_val = a if imm1 else reg[a]
        second_val = b if imm2 else reg[b]
        out[c] = int(first_val == second_val)
        return out
    
    ops = []
    for op in [add, mul, ban, bor, set_]:
        ops.append(lambda reg, a, b, c: op(reg, a, b, c, False))
        ops.append(lambda reg, a, b, c: op(reg, a, b, c, True))
    for op in [gt,eq]:
        ops.append(lambda reg, a, b, c: op(reg, a, b, c, True, False))
        ops.append(lambda reg, a, b, c: op(reg, a, b, c, False, True))
        ops.append(lambda reg, a, b, c: op(reg, a, b, c, False, False))
    out = 0
    for before, numbers, after in part1:
        def good(op):
            asd = op(before, *numbers[1:])
            # sprint(asd)
            # sprint(after)
            # sprint()
            return asd == after
        
        q = 0
        for op in [add, mul, ban, bor, set_]:
            q += good(lambda reg, a, b, c: op(reg, a, b, c, False))
            q += good(lambda reg, a, b, c: op(reg, a, b, c, True))
        for op in [gt,eq]:
            q += good(lambda reg, a, b, c: op(reg, a, b, c, True, False))
            q += good(lambda reg, a, b, c: op(reg, a, b, c, False, True))
            q += good(lambda reg, a, b, c: op(reg, a, b, c, False, False))
        # sprint(good(ops[3]))
        # q = sum(map(good, ops))
        # sprint(q)
        # sprint(mul(before, *numbers[1:], False))
        # sprint(after)
        if q >= 3:
            out += 1
    print(out)

    # 3 or more
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
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
