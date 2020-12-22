import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    out = 0

    one, two = paras
    one = ints(one)[1:]
    two = ints(two)[1:]

    while one and two:
        one_card = one.pop(0)
        two_card = two.pop(0)

        if one_card > two_card:
            one.append(one_card)
            one.append(two_card)
        else:
            assert one_card != two_card
            two.append(two_card)
            two.append(one_card)
    
    winner = one or two
    for i, x in enumerate(winner[::-1]):
        out += (i+1) * x

    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
