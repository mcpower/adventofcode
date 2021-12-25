import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    rows = len(lines)
    cols = len(lines[0])

    def move(lefts, downs):
        nl = set()
        nd = set()
        moved = False
        for x in lefts:
            new = padd(x, (0, 1))
            new[1] %= cols
            new = tuple(new)
            if new not in lefts and new not in downs:
                nl.add(new)
                moved = True
            else:
                nl.add(x)
        for x in downs:
            new = padd(x, (1, 0))
            new[0] %= rows
            new = tuple(new)
            if new not in nl and new not in downs:
                nd.add(new)
                moved = True
            else:
                nd.add(x)
        return nl, nd, moved
    
    lefts = set()
    downs = set()
    for row in range(rows):
        for col in range(cols):
            if lines[row][col] == "v":
                downs.add((row, col))
            elif lines[row][col] == ">":
                lefts.add((row, col))

    
    for _ in range(1000000):
        lefts, downs, moved = move(lefts, downs)
        # sprint(lefts, downs)
        if not moved:
            break
        out += 1
    
    out += 1
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
