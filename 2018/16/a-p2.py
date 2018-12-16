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
        hash(functools.partial(op, imm=False))
        ops.append((functools.partial(op, imm=False), op.__name__ + "r"))
        ops.append((functools.partial(op, imm=True), op.__name__ + "i"))
    for op in [gt,eq]:
        ops.append((functools.partial(op, imm1=True, imm2=False), op.__name__ + "ir"))
        ops.append((functools.partial(op,imm1=False, imm2=True), op.__name__ + "ri"))
        ops.append((functools.partial(op,imm1=False, imm2=False), op.__name__ + "rr"))
    out = 0

    op_numbers = set(x[0] for _, x, _ in part1)
    thing = {i: set(map(snd,ops)) for i in op_numbers}

    for before, numbers, after in part1:
        def good(op):
            asd = op(before, *numbers[1:])
            # sprint(asd)
            # sprint(after)
            # sprint()
            return asd == after
        
        q = 0
        # for op in [add, mul, ban, bor, set_]:
        #     q += good(lambda reg, a, b, c: op(reg, a, b, c, False))
        #     q += good(lambda reg, a, b, c: op(reg, a, b, c, True))
        # for op in [gt,eq]:
        #     q += good(lambda reg, a, b, c: op(reg, a, b, c, True, False))
        #     q += good(lambda reg, a, b, c: op(reg, a, b, c, False, True))
        #     q += good(lambda reg, a, b, c: op(reg, a, b, c, False, False))
        # sprint(good(ops[3]))
        q = sum(map(good, map(fst,ops)))
        # sprint(q)
        # sprint(mul(before, *numbers[1:], False))
        # sprint(after)
        if q >= 3:
            out += 1
        # asdasd = 
        # sprint(asdasd)
        thing[numbers[0]] &= set(b for a, b in ops if good(a))
    print(out)
    pprint(thing)

    print(len(op_numbers))
    print(len(thing))
    if sample:
        return
    
    to_f = dict()
    print(lmap(len, thing.values()))

    

    while len(to_f) != len(op_numbers):
        to_delete = []
        for k in thing:
            v = thing[k]
            if len(v) == 0:
                assert False
            elif len(v) == 1:
                the = list(v)[0]
                to_f[k] = the
                for k2 in thing:
                    if the in thing[k2]:
                        thing[k2].remove(the)
                    # thing[k2] -= thing[k2] - v
                to_delete.append(k)
                break
        else:
            assert False, "wat"
        for i in to_delete:
            del thing[i]
        # print(lmap(len, thing.values()))
    print(to_f)

    asdasdasd = {b: a for a, b in ops}
    final = {i: asdasdasd[to_f[i]] for i in to_f}
    registers = [0] * 4
    for opcode, *x in part2:
        registers = final[opcode](registers, *x)
    # 3 or more
    print(registers)
    
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
