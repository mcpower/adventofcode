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
    for c in x:
        if c.count("1") > c.count('0'):
            a += 1
        else:
            b += 1
        a *= 2
        b *= 2
    print(a*b // 4)
    
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
