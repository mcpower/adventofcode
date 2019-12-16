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
    start = lmap(int, lines[0])

    def get_base(pos):
        # pos is 0-ondexed
        repeat = pos + 1
        pat = [0] * repeat + [1] * repeat + [0] * repeat + [-1] * repeat
        x = itertools.cycle(pat)
        next(x)
        return x
    test = get_base(1)
    print(next(test), next(test), next(test), next(test), next(test), next(test))

    def phase(inp):
        # inp is list of ints
        out = []

        for i in range(len(inp)):
            blah = abs(sum(map(operator.mul, inp, get_base(i))))
            out.append(blah % 10)

        return out
    
    sprint(start)
    for _ in range(100):
        start = phase(start)
        # sprint(start)
    
    print("".join(lmap(str, start))[:8])
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
12345678
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
