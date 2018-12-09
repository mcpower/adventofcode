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

def highest_score(players: int, last_marble: int) -> int:
    marbles = Linked(0)
    scores = [0] * players

    cur_player = 0
    cur_index = 0
    for to_add in range(1, last_marble + 1):
        if to_add % 23 == 0:
            scores[cur_player] += to_add
            marbles = marbles.move(-7)

            scores[cur_player] += marbles.item
            to_delete = marbles
            marbles = marbles.move(1)
            to_delete.delete()
            del to_delete
        else:
            marbles = marbles.move(1)
            marbles.append_immediate(to_add)
            marbles = marbles.move(1)

        cur_player += 1
        if cur_player == players:
            cur_player = 0
    
    return max(scores)
    

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    players, last_marble = ints(inp)

    print(highest_score(players, last_marble))
    print(highest_score(players, last_marble*100))
    
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
