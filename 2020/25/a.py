import sys; sys.dont_write_bytecode = True; from utils import *

MOD = 20201227
TO_POW = 7

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    card, door = ints(inp)
    def decode(x):
        q = 1
        for i in range(1,10000000000):
            q *= TO_POW
            q %= MOD
            if q == x:
                return i
        else:
            print("damn :(")
            return
    
    print(pow(door, decode(card), 20201227))
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
5764801
17807724
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
