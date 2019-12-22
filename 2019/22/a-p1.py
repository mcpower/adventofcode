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

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    cards = 10 if sample else 10007

    deck = list(range(cards))

    for line in lines:
        if line == "deal into new stack":
            deck.reverse()
        elif line.startswith("cut"):
            q, *_ = ints(line)
            left = deck[:q]
            right = deck[q:]
            deck = right + left
        elif line.startswith("deal with increment "):
            q, *_ = ints(line)
            new_deck = [None] * cards
            new_pos = 0
            for i in range(cards):
                new_deck[new_pos] = deck[i]
                new_pos += q
                new_pos %= cards
            deck = new_deck
    
    sprint(deck)
    if not sample:
        print(deck.index(2019))
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
deal with increment 7
deal into new stack
deal into new stack
""",r"""
cut 6
deal with increment 7
deal into new stack
""",r"""
deal with increment 7
deal with increment 9
cut -2
""",r"""
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
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
