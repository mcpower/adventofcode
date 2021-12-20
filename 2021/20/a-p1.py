import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    enhancement, grid = paras
    enhancement: str = enhancement[0]
    assert len(enhancement) == 512
    
    ons = set()
    for r, row in enumerate(grid):
        for c, x in enumerate(row):
            if x == "#":
                ons.add((r, c))
    # future mcpower: this should be 1
    WTF = 3
    print(enhancement[0])
    print(enhancement[-1])
    def process(points: set, is_on: bool):
        new_ons = set()
        # get 5x5 neighbour of all ons
        to_process = {tuple(padd(p, (r, c))) for p in points for r in range(-WTF, WTF+1) for c in range(-WTF, WTF+1)}
        for r, c in to_process:
            bits = []
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    # sprint((dr, dc))
                    if sample:
                        bits.append(int(((r+dr, c+dc) in points)))
                    else:
                        bits.append(int((not is_on == ((r+dr, c+dc) in points))))
                        
            # sprint("wat")
            # quit()
            assert len(bits) == 9
            index = int("".join(map(str, bits)), 2)
            if enhancement[index] == ("#" if is_on else "."):
                new_ons.add((r, c))
        return new_ons
    if sample:
        print_grid(points_to_grid(list(ons), flip=False))
    is_on = True if sample else False
    for _ in range(2):
        ons = process(ons, is_on)
        if not sample:
            is_on = not is_on
        if sample:
            print_grid(points_to_grid(list(ons), flip=False))
    out = len(ons)
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
