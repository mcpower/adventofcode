import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    out = 0

    estimate = int(lines[0])

    buses = ints(lines[1])
    o = 99999999999999999, -1
    
    for i in buses:
        o = min(o, (math.ceil(estimate/i)*i, i))
    print((o[0]-estimate) * o[1])
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
939
7,13,x,x,59,x,31,19

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
