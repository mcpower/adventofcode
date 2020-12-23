import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    out = 0

    cups = lmap(int, inp)
    cups.extend(range(max(cups)+1, 1000000+1))

    # moves = 10 if sample else 100
    moves = 10000000

    # def gen(last):
    #     ...

    # one_index = cups.index(1)

    # after_one = cups[one_index+1:one_index+3]
    # sprint(after_one)
    # # return

    # for _ in range(moves):
    #     picked = cups[1:4]
    #     cups = [cups[0]] + cups[4:]

    #     current = cups[0]
    #     current -= 1
    #     while current not in cups:
    #         current -= 1
    #         if current < 1:
    #             current = 9
        
    #     dest = cups.index(current)
    #     cups = cups[:dest+1] + picked + cups[dest+1:]
    #     cups = cups[1:] + [cups[0]]
        
    #     sprint(cups)
    
    # while cups[0] != 1:
    #     cups = cups[1:] + [cups[0]]

    # print("".join(map(str, cups[1:])))

    linked = Linked.from_list(cups)
    number_to_linked = {}  # type: dict[int, Linked]
    for x in linked.iterate_nodes():
        number_to_linked[x.val] = x
    
    MAX = 1000000
    
    for _ in range(moves):
        cur = linked
        pick_start = linked.after
        pick_end = linked.after.after.after
        cur._join(pick_end.after)
        pick_end._join(pick_start)

        picked_list = pick_start.to_list()

        current = linked.val
        current -= 1
        if current == 0:
            current = MAX
        while current in picked_list:
            current -= 1
            if current < 1:
                current = MAX
        
        dest = number_to_linked[current]
        dest.concat_immediate(pick_start)
        linked = linked.after
        # cups = cups[:dest+1] + picked + cups[dest+1:]
        # cups = cups[1:] + [cups[0]]
        
        # sprint(cups)
    
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
