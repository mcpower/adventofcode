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
    blah = ints(inp)

    programs = [Intcode(blah) for _ in range(50)]

    queue = [deque() for _ in range(50)]

    nat = None

    for i in range(50):
        _, out = programs[i].run(i)
        if out:
            for dest, x, y in every_n(out, 3):
                if dest == 255:
                    nat = (x, y)
                else:
                    queue[dest].append((x, y))
    
    last_y = None
    
    wtf = 0
    while True:
        wtf += 1
        not_sent = [False] * 50
        for i in range(50):
            # get the thing
            if queue[i]:
                blah = list(queue[i].popleft())
            else:
                blah = [-1]
                not_sent[i] = True
            _, out = programs[i].run_multiple(blah)
            for dest, x, y in every_n(out, 3):
                if dest == 255:
                    nat = (x, y)
                else:
                    queue[dest].append((x, y))
        
        if all(not_sent):
            assert nat, (not_sent, wtf)
            queue[0].append(nat)
            y = nat[1]
            if y == last_y:
                print(y)
                return
            else:
                last_y = y
        
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
