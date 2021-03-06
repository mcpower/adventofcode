import sys; sys.dont_write_bytecode = True; from utils import *
"""
To do: ensure Code Runner works (in WSL), have preloaded the day and input in Chrome,
saved input into the folder, have utils on the side, collapse regions
Strings, lists, dicts:
lmap, ints, positive_ints, floats, positive_floats, words, keyvalues

Algorithms:
bisect, binary_search, hamming_distance, edit_distance

Data structures:
Linked, UnionFind
use deque for queue: q[0], q.append and q.popleft

List/Vector operations:
GRID_DELTA, OCT_DELTA
lget, lset, fst, snd
padd, pneg, psub, pmul, pdot, pdist1, pdist2sq, pdist2

Matrices:
matmat, matvec, matexp

Previous problems:
knot

Dict things:
dict.keys()
dict.values()
dict.items()
"""

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()

    scores = [3, 7]
    blah = lmap(int, inp)

    a, b = 0, 1

    while True:
        asd = str(scores[a] + scores[b])
        scores.extend(map(int, asd))
        a += scores[a] + 1
        b += scores[b] + 1
        a %= len(scores)
        b %= len(scores)
        if scores[-len(blah):] == blah or scores[-len(blah)-1:-1] == blah:
            break
    
    if scores[-len(blah):] == blah:
        print(len(scores) - len(blah))
    else:
        print(len(scores) - len(blah) - 1)
    
    # print(*scores[-10:], sep="")
    # print(*scores[n:n+10],sep="")
    # quit()


    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
51589
""",r"""
01245
""",r"""
92510
""",r"""
59414
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
