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
from intcodev1 import *
def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    # lines = inp.splitlines()
    prog = Intcode(ints(inp))
    prog[0] = 2
    grid = [[0] * 44 for _ in range(44)]
    last_run = prog.run()
    score = 0

    paddle_col = -1
    ball_col = -1

    def update():
        nonlocal score,paddle_col,ball_col,grid
        for a,b,c in every_n(last_run[1], 3):
            if a == -1:
                score = c
            else:
                grid[b][a] = c
                if c == 4:
                    ball_col = a
                elif c == 3:
                    paddle_col = a

    update()

    while not last_run[0]:
        pos = 0
        if paddle_col < ball_col:
            pos = 1
        elif paddle_col > ball_col:
            pos = -1
        last_run = prog.run(pos)
        update()
    print(score)
    
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
