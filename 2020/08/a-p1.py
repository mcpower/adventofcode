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

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    out = 0
    

    acc = 0
    pc = 0
    seen = set()
    while True:
        line = lines[pc]
        if pc in seen:
            print(acc)
            return
        seen.add(pc)
        
        a, b = line.split()
        b = int(b)
        if a == "acc":
            acc += b
        elif a == "jmp":
            pc += b
            continue
        
        pc += 1
    
    if out:
        print("out:    ", out)
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
