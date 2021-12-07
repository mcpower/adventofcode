import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    def cost(move):
        return move * (move + 1) // 2

    l = ints(inp)
    l.sort()
    mid = l[len(l)//2]
    out = sum(cost(abs(x-mid)) for x in l)

    for mid in range(min(l), max(l)+1):
        out = min(out, sum(cost(abs(x-mid)) for x in l))

    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
16,1,2,0,4,2,7,1,2,14
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
