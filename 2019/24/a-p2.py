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

    iterations = 10 if sample else 200

    grid = lmap(list, lines)
    grid[2][2] = "."
    grids = [[["."] * 5 for _ in range(5)] for _ in range(500)]
    grids[0] = grid
    del grid

    for iteration in range(iterations):
        new_grids = list(grids)

        for level in range(-(iteration+3), (iteration+3)+1):
            new_level = deepcopy(grids[level])
            for row in range(5):
                for col in range(5):
                    pair = (row, col)
                    if pair == (2, 2):
                        continue
                    this = grids[level][row][col]
                    neighbours = get_neighbours(grids[level], row, col, GRID_DELTA, fill=None)

                    if row == 0:
                        # get (1, 2) from above
                        neighbours.append(grids[level-1][1][2])
                    if row == 4:
                        # get (3, 2) from above
                        neighbours.append(grids[level-1][3][2])
                    if col == 0:
                        # get (2, 1) from above
                        neighbours.append(grids[level-1][2][1])
                    if col == 4:
                        # get (2, 3) from above
                        neighbours.append(grids[level-1][2][3])
                    
                    if pair == (1, 2):
                        # add below top row
                        neighbours.extend(grids[level+1][0])
                    if pair == (3, 2):
                        # add below bottom row
                        neighbours.extend(grids[level+1][-1])
                    if pair == (2, 1):
                        # add below left col
                        neighbours.extend(grids[level+1][row][0] for row in range(5))
                    if pair == (2, 3):
                        neighbours.extend(grids[level+1][row][-1] for row in range(5))
                    # assert len(neighbours) == 8 or len(neighbours) == 4, (row, col, len(neighbours), neighbours)

                    if this == "#":
                        # dies if exactly one bug
                        if neighbours.count("#") == 1:
                            pass
                        else:
                            new_level[row][col] = "."
                    else:
                        # infested = one or two
                        if neighbours.count("#") in (1, 2):
                            new_level[row][col] = "#"
            
            new_grids[level] = new_level

        grids = new_grids
    # print_grid(grids[-1])
    # print()
    # print_grid(grids[0])
    # print()
    # print_grid(grids[1])
    print(sum(sum(row.count("#") for row in grid) for grid in grids))
    # quit()


    # seq = RepeatingSequence(generator())
    # print_grid(seq.first_repeated_result)
    # res = flatten(seq.first_repeated_result)
    # # print(res)

    # i = 1
    # out = 0

    # for thing in res:
    #     if thing == "#":
    #         out += i
    #     i *= 2
    # print(out)
    # # quit()


    
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
