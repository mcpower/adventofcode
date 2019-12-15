import sys; sys.dont_write_bytecode = True; from utils_old import *
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
    lines = inp.splitlines()
    prog = Intcode(ints(lines[0]))

    cur_pos = [0, 0]

    UP = 1
    DOWN = 2
    LEFT = 4
    RIGHT = 3

    UP_D = (-1, 0)
    DOWN_D = (1, 0)
    LEFT_D = (0, -1)
    RIGHT_D = (0, 1)

    # (row, col) -> is_wall
    grid = dict()
    grid[tuple(cur_pos)] = 1

    target = None

    def dfs():
        nonlocal cur_pos, grid, target
        original_pos = deepcopy(cur_pos)
        # print(original_pos)
        # move up
        if tuple(padd(cur_pos, UP_D)) not in grid:
            _, out = prog.run(UP)
            grid[tuple(padd(cur_pos, UP_D))] = out[0]
            if out[0] != 0:
                cur_pos = padd(cur_pos, UP_D)
                if out[0] == 2:
                    target = cur_pos
                # we went up
                dfs()
                _, out = prog.run(DOWN)
                assert out[0] != 0
                cur_pos = padd(cur_pos, DOWN_D)
            assert cur_pos == original_pos
        if tuple(padd(cur_pos, DOWN_D)) not in grid:
            _, out = prog.run(DOWN)
            grid[tuple(padd(cur_pos, DOWN_D))] = out[0]
            if out[0] != 0:
                cur_pos = padd(cur_pos, DOWN_D)
                if out[0] == 2:
                    target = cur_pos
                dfs()
                _, out = prog.run(UP)
                assert out[0] != 0
                cur_pos = padd(cur_pos, UP_D)
            assert cur_pos == original_pos
        if tuple(padd(cur_pos, LEFT_D)) not in grid:
            _, out = prog.run(LEFT)
            grid[tuple(padd(cur_pos, LEFT_D))] = out[0]
            if out[0] != 0:
                cur_pos = padd(cur_pos, LEFT_D)
                if out[0] == 2:
                    target = cur_pos
                dfs()
                _, out = prog.run(RIGHT)
                assert out[0] != 0
                cur_pos = padd(cur_pos, RIGHT_D)
            assert cur_pos == original_pos
        if tuple(padd(cur_pos, RIGHT_D)) not in grid:
            _, out = prog.run(RIGHT)
            grid[tuple(padd(cur_pos, RIGHT_D))] = out[0]
            if out[0] != 0:
                cur_pos = padd(cur_pos, RIGHT_D)
                if out[0] == 2:
                    target = cur_pos
                dfs()
                _, out = prog.run(LEFT)
                assert out[0] != 0
                cur_pos = padd(cur_pos, LEFT_D)
            assert cur_pos == original_pos

    dfs()

    assert target is not None
    print(target)

    def expand(p):
        out = []
        row, col = p
        for drow, dcol in GRID_DELTA:
            new_row = row + drow
            new_col = col + dcol
            blah = (new_row, new_col)
            if blah in grid and grid[blah] != 0:
                out.append(blah)
        return out

    dist, path = bfs((0, 0), tuple(target), expand)
    print(dist)
    
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
