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



        addr = bin(addr)[2:].zfill(36)
        assert len(addr) == 36
        out = ""
        for x, masked in zip(addr, mask):
            if masked == "X":
                out += "X"
            elif masked == "0":
                out += x
            else:
                out += "1"
        
        xes = out.count("X")
        for i in range(2**xes):
            b = bin(i)[2:].zfill(xes)
            cur = 0
            c = ""
            for char in out:
                if char == "X":
                    c += b[cur]
                    cur += 1
                else:
                    c += char
            memory[int(c, 2)] = thing


        # memory[addr] = out
    # sprint(memory)
    print(sum(memory.values()))

    # if out:
    #     print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1


""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
