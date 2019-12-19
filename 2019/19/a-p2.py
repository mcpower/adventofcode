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

from intcodev1 import *
def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    prog = Intcode(ints(lines[0]))

    # blah = []
    # grid = make_grid(50, 50, fill=2)
    rows = [] # (row, start, end noninclusive)
    for i in range(4, 10000):
        seen = False
        start = None
        end = None

        for j in range(i, 100000):
            asd = deepcopy(prog)
            halted, out = asd.run_multiple([i, j])
            # print(out)
            found = out[0] == 1
            if found and not seen:
                seen = True
                start = j
            if not found and seen:
                end = j
                break
            # blah += out
        rows.append((i, start, end))

        if len(rows) > 100:
            old_row, old_start, old_end = rows[-100]
            if old_end - start >= 100:
                print(old_row * 10000 + start)
                return

    # print_grid(grid)
    # print(sum(blah))

    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""

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
