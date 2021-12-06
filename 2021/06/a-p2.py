import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    def generation(l):
        new_l = [0] * 9
        for i, c in enumerate(l):
            if i == 0:
                new_l[6] += c
                new_l[8] += c
            else:
                new_l[i-1] += c
        return new_l

    l = ints(inp)
    actual = [0] * 9
    for x in l:
        actual[x] += 1
    for _ in range(256):
        sprint(actual)
        actual = generation(actual)
    out = sum(actual)
    
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
