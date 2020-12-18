import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    out = 0

    active = set()

    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if c == "#":
                active.add((row, col, 0, 0))

    for _ in range(6):
        x_min = fst(min(active, key=fst))
        x_max = fst(max(active, key=fst))
        y_min = snd(min(active, key=snd))
        y_max = snd(max(active, key=snd))
        z_min = min(active, key=lambda x:x[2])[2]
        z_max = max(active, key=lambda x:x[2])[2]
        w_min = min(active, key=lambda x:x[3])[3]
        w_max = max(active, key=lambda x:x[3])[3]

        new_active = set()

        for x in range(x_min - 2, x_max + 2):
            for y in range(y_min - 2, y_max + 2):
                for z in range(z_min - 2, z_max + 2):
                    for w in range(w_min-2, w_max+2):
                        p = (x, y, z, w)
                        neighbours = []
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                for dz in [-1, 0, 1]:
                                    for dw in [-1, 0, 1]:
                                        if dx != 0 or dy != 0 or dz != 0 or dw != 0:
                                            neighbours.append((x+dx, y+dy,z+dz, w+dw))
                        active_neighbours = sum([x in active for x in neighbours])
                        if p in active and (active_neighbours == 2 or active_neighbours == 3):
                            new_active.add(p)
                        if p not in active and ( active_neighbours == 3):
                            new_active.add(p)
        active = new_active
    out = len(active)
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
.#.
..#
###

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
