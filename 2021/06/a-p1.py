import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    def generation(l):
        new_l = []
        for i in l:
            if i == 0:
                new_l.append(8)
                new_l.append(6)
            else:
                new_l.append(i-1)
        return new_l

    l = ints(inp)
    for _ in range(80):
        l = generation(l)
    out = len(l)
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
3,4,3,1,2
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
