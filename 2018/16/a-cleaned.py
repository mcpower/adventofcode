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
    triplet = []
    empty = 0
    is_part2 = False
    for line in lines:
        nums = ints(line)
        if not nums:
            empty += 1
            if empty == 3:
                is_part2 = True
            continue
        empty = 0
        if is_part2:
            part2.append(nums)
        else:
            triplet.append(nums)
            if len(triplet) == 3:
                part1.append(triplet)
                triplet = []
    
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
        ops.append(functools.partial(op, imm=False))
        ops.append(functools.partial(op, imm=True))
    for op in [gt,eq]:
        ops.append(functools.partial(op, imm1=True, imm2=False))
        ops.append(functools.partial(op, imm1=False, imm2=True))
        ops.append(functools.partial(op, imm1=False, imm2=False))
    part1_ans = 0

    opcodes = frozenset(x[0] for _, x, _ in part1)
    opcode_to_candidates = {i: frozenset(ops) for i in opcodes}

    for before, (opcode, *args), after in part1:
        def good(op):
            return op(before, *args) == after
        candidates = frozenset(filter(good, ops))
        if len(candidates) >= 3:
            part1_ans += 1
        opcode_to_candidates[opcode] &= candidates

    print("part 1:", part1_ans)
    if sample:
        return
    
    opcode_to_func = dict()
    while len(opcodes) != len(opcode_to_func):
        found_opcode = None
        for opcode, candidates in opcode_to_candidates.items():
            assert candidates
            if len(candidates) == 1:
                opcode_to_func[opcode] = next(iter(candidates))
                for other_opcode in opcode_to_candidates:
                    opcode_to_candidates[other_opcode] -= candidates
                found_opcode = opcode
                break
        else:
            assert False, "can't find unique assignment"
        del opcode_to_candidates[found_opcode]


    registers = [0] * 4
    for opcode, *args in part2:
        registers = opcode_to_func[opcode](registers, *args)
    # 3 or more
    print("part 2:", registers[0])
    
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
