import sys; sys.dont_write_bytecode = True; from utils import *
"""
Strings, lists, dicts:
lmap, ints, positive_ints, floats, positive_floats, words

Data structures:
Linked, UnionFind
dict: d.keys(), d.values(), d.items()
deque: q[0], q.append and q.popleft

List/Vector operations:
GRID_DELTA, OCT_DELTA
lget, lset, fst, snd
padd, pneg, psub, pmul, pdot, pdist1, pdist2sq, pdist2

Matrices:
matmat, matvec, matexp
"""
from intcodev1 import *
def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    prog = Intcode(ints(inp))
    # prog.run_interactive()
    BAD = "escape pod infinite loop giant electromagnet photons molten lava"
    CHECKPOINT = "Security Checkpoint"

    DIRECTIONS = {
        "north": CHAR_TO_DELTA["N"],
        "east": CHAR_TO_DELTA["E"],
        "south": CHAR_TO_DELTA["S"],
        "west": CHAR_TO_DELTA["W"],
    }

    next_command = None
    import random

    my_items = list()

    for _ in range(1000):
        if next_command is None:
            _, out = prog.run()
        else:
            _, out = prog.run_ascii(next_command)
        output = "".join(map(chr, out))
        print(output)
        output = output.strip().splitlines()
        name = output[0].strip(" =")
        
        doors = output.index("Doors here lead:") + 1
        directions = []
        while True:
            asd = output[doors]
            if asd:
                directions.append(asd.strip("- "))
            else:
                break
            doors += 1
        
        items_list = []
        if "Items here:" in output:
            items = output.index("Items here:") + 1
            while True:
                asd = output[items]
                if asd:
                    items_list.append(asd.strip("- "))
                else:
                    break
                items += 1
        
        items_list = [item for item in items_list if item not in BAD]
        if items_list:
            next_command = "\n".join("take " + item for item in items_list) + "\n"
            for item in items_list: my_items.append(item)
        else:
            next_command = ""
        next_command += random.choice(directions)
    

    for _ in range(1000):
        if next_command is None:
            _, out = prog.run()
        else:
            _, out = prog.run_ascii(next_command)
        output = "".join(map(chr, out))
        output = output.strip().splitlines()
        name = output[0].strip(" =")
        if name == "Security Checkpoint":
            print(output)
            break
        
        doors = output.index("Doors here lead:") + 1
        directions = []
        while True:
            asd = output[doors]
            if asd:
                directions.append(asd.strip("- "))
            else:
                break
            doors += 1
        
        items_list = []
        if "Items here:" in output:
            items = output.index("Items here:") + 1
            while True:
                asd = output[items]
                if asd:
                    items_list.append(asd.strip("- "))
                else:
                    break
                items += 1
        
        items_list = [item for item in items_list if item not in BAD]
        if items_list:
            next_command = "\n".join("take " + item for item in items_list) + "\n"
            for item in items_list: my_items.append(item)
        else:
            next_command = ""
        next_command += random.choice(directions)

    
    for i in range(2**len(my_items)):
        bitset = bin(i)[2:].zfill(len(my_items))

        my_prog = deepcopy(prog)
        for item_ind, to_drop in enumerate(bitset):
            if to_drop == "1":
                _, _ = my_prog.run_ascii("drop " + my_items[item_ind])

        _, out = my_prog.run_ascii("north")

        output = "".join(map(chr, out))
        if "Alert!" not in output:
            print(output)
            # my_prog.run_interactive()
        

        
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""],[
# Part 2
r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
