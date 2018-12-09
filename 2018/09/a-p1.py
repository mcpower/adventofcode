import sys; sys.dont_write_bytecode = True; from utils import *
"""
To do: ensure Code Runner works (in WSL), have preloaded the day and input in Chrome,
saved input into the folder, and have utils on the side

Strings, lists, dicts:
lmap, ints, positive_ints, floats, positive_floats, words, keyvalues

Algorithms:
bisect, binary_search, hamming_distance, edit_distance

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

    players, last_marble = ints(inp)

    marbles = [0]
    scores = [0] * players

    remaining = set(range(1, last_marble+1))

    cur_player = 0
    cur_index = 0
    # while remaining:
    #     to_add = min(remaining)
        # remaining.remove(to_add)
    for to_add in range(1, last_marble + 1):
        if to_add % 23 == 0:
            scores[cur_player] += to_add
            to_remove = (cur_index - 7) % len(marbles)
            scores[cur_player] += marbles[to_remove]
            del marbles[to_remove]
            cur_index = to_remove
            sprint(cur_player, marbles[to_remove])
        else:
            insert_pos = (cur_index + 2) % len(marbles)
            marbles.insert(insert_pos, to_add)
            cur_index = insert_pos

        # sprint(marbles, cur_index)
        cur_player += 1
        if cur_player == players:
            cur_player = 0
    
    print(max(scores))
    # quit()
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
9 25
""",
r"""
10 players; last marble is worth 1618 points
""",r"""
13 players; last marble is worth 7999 points
""",r"""
17 players; last marble is worth 1104 points
""",r"""
21 players; last marble is worth 6111 points
""",r"""
30 players; last marble is worth 5807 points
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
