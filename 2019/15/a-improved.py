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
    lines = inp.splitlines()
    prog = Intcode(ints(lines[0]))

    cur_pos = [0, 0]
    D = {
        1: (-1, 0),
        2: (1, 0),
        4: (0, -1),
        3: (0, 1),
    }
    REVERSE = {
        1: 2,
        2: 1,
        4: 3,
        3: 4,
    }

    grid = dict()
    grid[tuple(cur_pos)] = 1

    target = None

    def dfs():
        nonlocal cur_pos, grid, target
        original_pos = deepcopy(cur_pos)
        for i, dpos in D.items():
            new_pos = tuple(padd(cur_pos, dpos))
            if new_pos not in grid:
                _, [out] = prog.run(i)
                grid[new_pos] = out
                if out != 0:
                    cur_pos = list(new_pos)
                    if out == 2:
                        target = cur_pos
                    dfs()
                    reverse_i = REVERSE[i]
                    reverse_dpos = D[reverse_i]
                    _, [out] = prog.run(reverse_i)
                    cur_pos = padd(cur_pos, reverse_dpos)
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
            new_pos = (new_row, new_col)
            assert new_pos in grid
            if grid[new_pos] != 0:
                out.append(new_pos)
        return out

    part1, _ = bfs_single((0, 0), tuple(target), expand)
    print("part1:", part1)
    distances, _ = bfs(tuple(target), expand)
    print("part2:", max(distances.values()))
    
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
