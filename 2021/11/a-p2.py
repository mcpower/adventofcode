import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0
    

    def step(grid):
        rows = len(grid)
        cols = len(grid[0])
        new_grid = copy.deepcopy(grid)
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                new_grid[row][col] += 1

        flashed = set()
        cont = True
        while cont:
            cont = False
            for row in range(rows):
                for col in range(cols):
                    if new_grid[row][col] > 9 and (row, col) not in flashed:
                        flashed.add((row, col))
                        cont = True

                        for drow, dcol in OCT_DELTA:
                            nr = row + drow
                            nc = col + dcol
                            if 0 <= nr < rows and 0 <= nc < cols:
                                new_grid[nr][nc] += 1
        
        for drow, dcol in flashed:
            new_grid[drow][dcol] = 0
        
        
        return new_grid, len(flashed) == rows * cols
    
    grid = [lmap(int, line) for line in lines]
    for i in range(10000000):
        grid, blah = step(grid)
        if blah:
            # I added the +1 after my submission
            print(i+1)
            break
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
