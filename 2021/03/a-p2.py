import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    x = list(zip(*lines))
    
    a = 0
    b = 0

    def doit(most_common):
        indices = set(range(len(x[0])))
        for c in x:
            filtered_c = [c[i] for i in indices]
            ones = filtered_c.count('1')
            zeroes = filtered_c.count('0')
            if not most_common:
                target = '1' if zeroes > ones else '0'
            else:
                target = '0' if zeroes > ones else '1'
            new_indices = set()
            for i, asdf in enumerate(c):
                if i not in indices:
                    continue
                if asdf != target:
                    continue
                new_indices.add(i)
            indices = new_indices
            if len(indices) == 1:
                return lines[next(iter(indices))]
    print(doit(False))
    print(int(doit(False), 2) * int(doit(True), 2))
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
