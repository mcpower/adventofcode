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
import copy
def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    grid = []
    for line in lines:
        grid.append(list(line))
    n = len(grid)

    def get_neighbour(i, j):
        p = (i, j)
        x = []
        for d in OCT_DELTA:
            try:
                asd = padd(d, p)
                if asd[0] < 0 or asd[1] < 0:
                    continue
                x.append(lget(grid, asd))
            except Exception:
                pass
        return x
    for _ in range(10):
        new_grid = copy.deepcopy(grid)

        for i in range(n):
            for j in range(n):
                neighbours = get_neighbour(i, j)
                if grid[i][j] == ".":
                    # open
                    if sum(n == "|" for n in neighbours)  >= 3:
                        new_grid[i][j] = "|"
                elif grid[i][j] == "|":
                    if sum(n == "#" for n in neighbours)  >= 3:
                        new_grid[i][j] = "#"
                else:
                    if sum(n == "#" for n in neighbours)  >= 1 and sum(n == "|" for n in neighbours)  >= 1:
                        pass
                    else:
                        new_grid[i][j] = "."
        grid = new_grid
        if sample:
            print_grid(grid)
            print()
    
    q = sum(line.count("|") for line in grid)
    w = sum(line.count("#") for line in grid)
    print(q,w,q*w)


    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
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
