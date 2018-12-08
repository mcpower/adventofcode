import sys; sys.dont_write_bytecode = True; from utils import *
"""
Strings, lists, dicts:
lmap, ints, positive_ints, floats, positive_floats, words, keyvalues

Algorithms:
bisect, binary_search, hamming_distance, edit_distance

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

    inp = ints(inp)
    out = 0

    i = 0

    def get_value():
        nonlocal inp, i, out
        children = inp[i]
        i += 1
        metadata = inp[i]
        i += 1

        values = [get_value() for _ in range(children)]
        m = []
        for _ in range(metadata):
            m.append(inp[i])
            i += 1
        
        if children == 0:
            return sum(m)
        else:
            res  = 0
            for x in m:
                ind = x - 1
                try:
                    res += values[ind]
                except Exception:
                    pass
            return res


    print(get_value())


    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
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
