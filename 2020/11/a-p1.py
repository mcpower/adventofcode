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

    grid = lmap(list, lines)

    rows = len(grid)
    cols = len(grid[0])

    def next_grid(grid):
        new = copy.deepcopy(grid)

        for row in range(rows):
            for col in range(cols):
                cur = grid[row][col]
                neighbours = get_neighbours(grid, row, col, OCT_DELTA)
                if cur == "L" and neighbours.count("#") == 0:
                    new[row][col] = "#"
                
                if cur == "#" and neighbours.count("#") >= 4:
                    new[row][col] = "L"
        
        return new
    
    new_grid = next_grid(grid)
    while new_grid != grid:
        grid, new_grid = new_grid, next_grid(new_grid)
        # out += 1
    
    print(flatten(grid).count("#"))
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL

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
