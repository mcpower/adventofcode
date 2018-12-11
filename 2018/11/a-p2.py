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

    inp = int(inp)

    def get_power(x, y, q=inp):
        rack = x + 10
        power = rack * y
        power += q
        power *= rack
        power //= 100
        power %= 10
        power -= 5
        return power
    # assert(get_power(122, 79, 57) == -5)

    grid = [[get_power(i, j) for i in range(300)] for j in range(300)]
    csum = make_grid(301, 301, None)
    # csum[0][0] = grid[0][0]

    def rec(i, j):
        if i < 0:
            return 0
        if j < 0:
            return 0
        if csum[i][j] is not None:
            return csum[i][j]
        csum[i][j] = grid[i][j] + rec(i-1, j) + rec(i, j-1) - rec(i-1, j-1)
        return csum[i][j]
    
    def get_ans(x, y, size):
        x -= 1
        y -= 1
        sx = x + size
        sy = y + size
        return rec(sx, sy) - rec(sx, y) - rec(x, sy) + rec(x, y)
    
    out = (-1, -1, -1, -1)
    for x in range(300):
        for y in range(300):
            for size in range(300 - max(x, y)):
                out = max(out, (get_ans(x, y, size), x, y, size))
    
    print(out)
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
18
""",r"""
42
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
