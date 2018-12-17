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

    max_coord = max(ints(inp))    

    asd = [] # type, fst, snd, third
    for line in lines:
        asd.append([line[0]] + ints(line))

    # x=500, y=0
    max_y = 0
    min_y = 10000
    for t, c, lo, hi in asd:
        if  t == "x":
            max_y = max(max_y, hi)
            min_y = min(min_y, lo)
        else:
            max_y = max(max_y, c)
            min_y = min(min_y, c)

    

    grid = make_grid(max_y+1, max_coord+1, ".")
    n, m = len(grid), len(grid[0])
    #grid[y][x]
    for t, c, lo, hi in asd:
        for i in range(lo, hi+1):
            if t == "x":
                grid[i][c] = "#"
            else:
                grid[c][i] = "#"

    out = 0

    def solid(x, y):
        if not (0 <= x < m and 0 <= y < n):
            return False
        return grid[y][x] in "#~"

    def fill(x, y, fromleft=False,fromright=False):
        # returns if it settles
        nonlocal out, grid
        if not (0 <= x < m and 0 <= y < n):
            return False
        # try:
        #     grid[y][x]
        # except Exception:
        #     return False
        
        if grid[y][x] in "#~":
            return True
        if grid[y][x] == "|":
            return False

        to_add = y >= min_y
        # left_x = x
        # right_x = x
        # while fill()
        
        grid[y][x] = "|"
        out += to_add
        # print(out)
        fill(x, y+1)


        if solid(x, y+1):
            left = x-1
            while not solid(left, y) and fill(left, y+1):
                grid[y][left] = "|"
                out += to_add
                left -= 1
            right = x+1
            while not solid(right, y) and fill(right, y+1):
                grid[y][right] = "|"
                out += to_add
                right += 1
            
            left_good = solid(left, y)
            right_good = solid(right, y)

            if left_good and right_good:
                for i in range(left+1, right):
                    grid[y][i] = "~"
                return True
            else:
                if not right_good:
                    grid[y][right] = "|"
                    out += to_add
                    fill(right, y+1)
                if not left_good:
                    grid[y][left] = "|"
                    out += to_add
                    fill(left, y+1)
                return False

            # go left and right
            # asd = []
            # if not fromleft:
            #     asd.append(fill(x-1, y,fromright=True))
            # if not fromright:
            #     asd.append(fill(x+1, y,fromleft=True))
            # sprint(asd, x, y)
            # if all(asd):
            #     grid[y][x] = "~"
            #     return True
            # else:
            #     return False
        else:
            # can't settle
            return False


    fill(500, 0)
    if False:
        print_grid([row[300:]for row in grid])
    print(out)
    print(sum(x in "~" for i, row in enumerate(grid) for x in row if min_y <= i <= max_y))
    print(min_y, max_y)
    # quit()
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
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
