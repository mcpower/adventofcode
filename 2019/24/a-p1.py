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

    def generator():
        grid = lmap(list, lines)
        # print_grid(grid)
        # print()

        yield tuple(lmap(tuple, grid))

        while True:
            new_grid = deepcopy(grid)

            for row in range(5):
                for col in range(5):
                    this = grid[row][col]
                    neighbours = get_neighbours(grid, row, col, GRID_DELTA, fill=".")

                    if this == "#":
                        # dies if exactly one bug
                        if neighbours.count("#") == 1:
                            pass
                        else:
                            new_grid[row][col] = "."
                    else:
                        # infested = one or two
                        if neighbours.count("#") in (1, 2):
                            new_grid[row][col] = "#"

            grid = new_grid
            yield tuple(lmap(tuple, grid))
            # print_grid(grid)
            # print()
            # quit()


    seq = RepeatingSequence(generator())
    print_grid(seq.first_repeated_result)
    res = flatten(seq.first_repeated_result)
    # print(res)

    i = 1
    out = 0

    for thing in res:
        if thing == "#":
            out += i
        i *= 2
    print(out)
    # quit()


    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
....#
#..#.
#..##
..#..
#....
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
