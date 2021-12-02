import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = lmap(str.splitlines, inp.split("\n\n"))
    x = 0
    y = 0
    aim = 0

    for line in lines:
        a, b = line.split()
        b = int(b)
        if a == 'forward':
            x -= b
            y += b * (-aim)
        elif a == 'backward':
            x += b
        elif a =='up':
            aim += b
        else:
            aim -= b
        sprint(x,y,aim)
    
    out = x * y
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
forward 5
down 5
forward 8
up 3
down 8
forward 2
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
