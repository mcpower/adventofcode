import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    grid = [lmap(int, x) for x in lines]
    rows, cols = dimensions(grid)
    rows = len(grid)
    cols = len(grid[0])

    # @functools.lru_cache(maxsize=None)
    # def lowest_risk(r, c):
    #     if r == rows - 1 and c == cols - 1:
    #         return grid[r][c]
    #     if r == rows or c == cols:
    #         return 9999999999999

    #     return grid[r][c] + min(lowest_risk(r+1, c), lowest_risk(r, c+1))
    # out = min(lowest_risk(r+1, c), lowest_risk(r, c+1))
    FINAL = (-1, -1)
    def expand(x):
        r, c = x
        if r == 5*rows - 1 and c == 5*cols - 1:
            return [(0, FINAL)]
        out = []
        # section1 ,r = divmod(r, rows)
        # section2, c = divmod(c, cols)
        for nr, nc in neighbours((r, c), (5*rows, 5*cols), GRID_DELTA):
            section1 ,nr1 = divmod(nr, rows)
            section2, nc1 = divmod(nc, cols)
            out.append(((((grid[nr1][nc1]+section2+section1) - 1) % 9) + 1, (nr, nc)))
        return out
    
    dist, path = a_star((0, 0), FINAL, expand)
    out = dist
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
