import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    out = 0

    cups = lmap(int, inp)
    cups.extend(range(max(cups)+1, 1000000+1))

    MOVES = 10000000

    linked = Linked.from_list(cups)
    number_to_linked = {}  # type: dict[int, Linked[int]]
    for x in linked.iterate_nodes():
        number_to_linked[x.val] = x
    
    MAX = 1000000
    
    for _ in range(MOVES):
        picked = linked.pop_after(after=1, n=3)
        picked_list = picked.to_list()

        current = linked.val
        current -= 1
        if current < 1:
            current = MAX
        while current in picked_list:
            current -= 1
            if current < 1:
                current = MAX
        
        dest = number_to_linked[current]
        dest.concat_immediate(picked)
        linked = linked.after
    
    one = number_to_linked[1]
    out = one.after.val * one.after.after.val
    

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
