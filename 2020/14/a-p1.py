import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    # out = 0
    memory = {}

    mask = ""

    for line in lines:
        if "mask" in line:
            mask = line.split()[-1]
            assert len(mask) == 36
            continue
        addr, thing = ints(line)
        thing = bin(thing)[2:].zfill(36)
        assert len(thing) == 36
        out = ""
        for x, masked in zip(thing, mask):
            if masked == "X":
                out += x
            else:
                out += masked
        out = int(out, 2)


        memory[addr] = out
    # sprint(memory)
    print(sum(memory.values()))

    # if out:
    #     print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
