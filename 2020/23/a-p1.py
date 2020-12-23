import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    out = 0

    cups = lmap(int, inp)

    moves = 10 if sample else 100

    for _ in range(moves):
        picked = cups[1:4]
        cups = [cups[0]] + cups[4:]

        current = cups[0]
        current -= 1
        while current not in cups:
            current -= 1
            if current < 1:
                current = 9
        
        dest = cups.index(current)
        cups = cups[:dest+1] + picked + cups[dest+1:]
        cups = cups[1:] + [cups[0]]
        
        sprint(cups)
    
    while cups[0] != 1:
        cups = cups[1:] + [cups[0]]

    print("".join(map(str, cups[1:])))
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
389125467
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
