import sys; sys.dont_write_bytecode = True; from utils import *
"""
To do: ensure Code Runner works (in WSL), have preloaded the day and input in Chrome,
saved input into the folder, have utils on the side, collapse regions
Strings, lists, dicts:
lmap, ints, positive_ints, floats, positive_floats, words, keyvalues

Algorithms:
bisect, binary_search, hamming_distance, edit_distance

Data structures:
Linked, UnionFind
use deque for queue: q[0], q.append and q.popleft

List/Vector operations:
GRID_DELTA, OCT_DELTA
lget, lset, fst, snd
padd, pneg, psub, pmul, pdot, pdist1, pdist2sq, pdist2

Matrices:
matmat, matvec, matexp

Previous problems:
knot

Dict things:
dict.keys()
dict.values()
dict.items()
"""

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()

    GENERATIONS = 20

    OFFSET = 500

    state = ["."] * OFFSET + list(lines[0][len("initial state: "):]) + ["."] * OFFSET
    # print(state)

    transitions = set()

    for thing in lines[2:]:
        left, right = thing.split(" => ")
        if right != "#":
            continue
        transitions.add(left)

    print(transitions)
    
    for _ in range(GENERATIONS):
        new_state = ["."] * len(state)
        for i in range(len(state)):
            if i - 2 < 0: continue
            if i + 2 >= len(state): continue
            
            asd = "".join(state[i-2:i+3])
            # print(asd)
            # quit()
            if asd in transitions:
                new_state[i] = "#"
        state = new_state

    print(state[OFFSET:OFFSET+50])
    print(len(state))
    out = 0

    for i,x in enumerate(state):
        if x == '#':
            out += i - OFFSET
    print(out)


    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
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
