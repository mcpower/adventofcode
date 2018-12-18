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
    
    
    def to_hashable(grid):
        return "".join("".join(line) for line in grid)
    
    def generator():
        grid = lmap(list, lines)
        yield grid
        n = len(grid)
        while True:
            new_grid = copy.deepcopy(grid)

            for i in range(n):
                for j in range(n):
                    neighbours = get_neighbours(grid, i, j, OCT_DELTA)
                    trees = neighbours.count("|")
                    yards = neighbours.count("#")
                    if grid[i][j] == ".":
                        if trees >= 3:
                            new_grid[i][j] = "|"
                    elif grid[i][j] == "|":
                        if yards >= 3:
                            new_grid[i][j] = "#"
                    else:
                        if not (yards >= 1 and trees >= 1):
                            new_grid[i][j] = "."
            grid = new_grid
            yield grid

    seq = RepeatingSequence(generator(), to_hashable)
    grid = flatten(seq[1000000000])

    
    q = grid.count("|")
    w = grid.count("#")
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
