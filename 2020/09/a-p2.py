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

    backtrack = 5 if sample else 25

    
    l = ints(inp)

    target = None

    for i in range(backtrack, len(l)):
        last = l[i-backtrack:i]
        good = False
        for j, x in enumerate(last):
            for k, y in enumerate(last):
                if j == k:
                    continue
                if x + y == l[i]:
                    good = True
        if not good:
            target = (l[i])
            break
    
    o = [0]
    for i in l:
        o.append(o[-1] + i)
    
    for i in range(len(l)+1):
        for j in range(i, len(l)+1):
            if o[j] - o[i] == target:
                print(i, j)
                print(min(l[i:j]) + max(l[i:j]))

    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
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
