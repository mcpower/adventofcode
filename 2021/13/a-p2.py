import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    grid = set()
    points, folds = paras

    for line in points:
        grid.add(tuple(ints(line)))
    
    for fold in folds:
        _, _, blah = fold.split()
        dim = blah[0]
        coord = ints(blah)[0]
        to_change = 0 if dim == "x" else 1
        new_grid = set()
        for point in grid:
            l = list(point)
            if l[to_change] >= coord:
                l[to_change] = coord - (l[to_change] - coord)
            new_grid.add(tuple(l))
        grid = new_grid
        
    grid = list(grid)
    print_grid(points_to_grid(grid))

    out = len(grid)
    sprint(grid)
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
