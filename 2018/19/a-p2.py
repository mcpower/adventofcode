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
    r0 = 1
    r2 = 0
    r3 = 0
    r4 = 0
    r5 = 0

    r5 += 2
    r5 *= r5
    r5 *= 19  # PC
    r5 *= 11
    r4 += 2
    r4 *= 22  # PC
    r4 += 16
    r5 += r4
    if r0:
        r4 = 27  # PC
        r4 *= 28  # PC
        r4 += 29  # PC
        r4 *= 30  # PC
        r4 *= 14
        r4 *= 32  # PC
        r5 += r4
        r0 = 0


    # r2 = 1
    # while r2 <= r5:
    #     r3 = 1

    #     while r3 <= r5:
    #         if r2*r3 == r5:
    #             r0 += r2                    
    #         r3 += 1

    #     r2 += 1


    # (or equivalently)
    # for r2 in range(1, r5+1):
    #     for r3 in range(1, r5+1):
    #         if r2*r3 == r5:
    #             r0 += r2 

    # (or equivalently)
    for r2 in range(1, r5+1):
        if r5 % r2 == 0:
            r0 += r2
    print(r0)



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
