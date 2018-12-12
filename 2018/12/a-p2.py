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

    GENERATIONS = 50000000000

    OFFSET = 0

    state = list(lines[0][len("initial state: "):])
    while state[0] == '.':
        state.pop(0) # yuck
        OFFSET += 1
    while state[-1] == '.':
        state.pop()

    transitions = set()

    for thing in lines[2:]:
        left, right = thing.split(" => ")
        if right != "#":
            continue
        transitions.add(left)

    def get():
        out = 0
        for i, x in enumerate(state):
            if x == '#':
                out += i + OFFSET
        return out
    
    def g(i):
        if 0 <= i < len(state):
            return state[i]
        return "."

    # print(transitions)

    states_seen = {}
    states_seen["".join(state)] = (0, OFFSET)
    
    for gen in range(GENERATIONS):
        OFFSET -= 5
        new_state = ["."] * 5 + ["."] * len(state) + ["."] * 5
        for i in range(len(new_state)):
            asd = "".join(g(i + j-5) for j in [-2, -1, 0, 1, 2])
            # print(asd)
            # quit()
            if asd in transitions:
                new_state[i] = "#"
        # print(*state[OFFSET-10:OFFSET+110], sep="")
        # print(get())
        state = new_state
        while state[0] == '.':
            state.pop(0) # yuck
            OFFSET += 1
        while state[-1] == '.':
            state.pop()
        q = "".join(state)
        if q in states_seen:
            the_one = q
            new_gen = gen + 1
            new_offset = OFFSET
            break
        else:
            states_seen[q] = (gen+1, OFFSET)
    
    print(the_one)
    print(states_seen[q])
    print(new_gen, new_offset)
    # This uses the fact that new_offset and states_seen[q][1] are off by one.
    # May not work for all inputs!
    things_to_simulate = GENERATIONS - new_gen
    OFFSET += things_to_simulate

        

    # print(len(state))
    out = 0

    print(get())
    # print(out)


    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD

def dif(x):
    return [a-b for a, b in zip(x, x[1:])]

# Trying some things (didn't work)
asd = """2408 2318 2702 2492 2953 2651 2969 2976 3131 3084 3447 3694 3006 3843 3154 3327 3786 3538 4001 4264 3890 4450 4126 4127 3841 4504 4100 4380 4549 4452 4730 4650 5008 4569 5085 4798 5290 5270 4963 5225 5402 5001 5224 5513 5329 5709 5861 5671 5637 5865""".split()
asd = lmap(int, asd)
# print(asd)
# print(dif(asd))
# print(dif(dif(asd)))
# quit()


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
