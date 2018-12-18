import sys; sys.dont_write_bytecode = True; from utils_improved import *
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

    starting_state = lines[0][len("initial state: "):]

    state_transitions = set()
    for line in lines[2:]:
        left, right = line.split(" => ")
        if right == "#":
            state_transitions.add(left)
    
    def to_hashable(s):
        return "".join(s[0])

    def generator():
        state = list(starting_state)
        offset = 0

        def fix():
            nonlocal state, offset
            while state and state[0] == ".":
                state.pop(0)
                offset += 1
            while state and state[-1] == ".":
                state.pop()
        
        fix()
        yield (state, offset)

        while True:
            state = ["."] * 100 + state + ["."] * 100
            offset -= 100
            old_state = list(state)
            for i in range(2,len(state)-2):
                if "".join(old_state[i-2:i+3]) in state_transitions:
                    state[i] = "#"
                else:
                    state[i] = "."
            fix()

            yield (state, offset)
    
    N = 50000000000
    sequence = RepeatingSequence(generator(), to_hashable)
    pattern, offset = sequence[N]
    offset_offset = sequence.second_repeated_result[1] - sequence.first_repeated_result[1]
    offset += offset_offset * sequence.cycle_number(N)

    out = 0
    for i, c in enumerate(pattern):
        if c == "#":
            out += offset + i
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
