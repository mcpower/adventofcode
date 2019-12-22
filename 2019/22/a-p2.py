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
    cards = 10 if sample else 119315717514047
    repeats = 1 if sample else 101741582076661
    def inv(n):
        return pow(n, cards-2, cards)
    

    # cards = 10007
    # out = 2019


    def get(offset, increment, i):
        return (offset + i * increment) % cards
    
    REV = 0
    CUT = 1
    DEAL = 2
    actions = []
    for line in lines:
        if line == "deal into new stack":
            actions.append((REV, REV))
        elif line.startswith("cut"):
            q, *_ = ints(line)
            actions.append((CUT, q))
        elif line.startswith("deal with increment "):
            # new_deck[i*q] = deck[i]
            q, *_ = ints(line)
            actions.append((DEAL, inv(q)))
    
    increment_mul = 1 # how much things increment per index
    offset_diff = 0 # what's the first number?
    for (action, q) in actions:
        if action == REV:
            increment_mul *= -1
            increment_mul %= cards
            offset_diff += increment_mul
            offset_diff %= cards
        elif action == CUT:
            offset_diff += q * increment_mul
            offset_diff %= cards
        elif action == DEAL:
            increment_mul *= q
            increment_mul %= cards
    
    # increment changes by 86777610202610
    # 
    # one_increment = 86777610202610
    # offset_times_1_increment_diff = 81917208448684

    def get_magic(i):
        increment = pow(increment_mul, i, cards)
        # 1 + one_increment + one_increment^2 + ...
        offset = offset_diff * (1 - pow(increment_mul, i, cards)) * inv((1 - increment_mul) % cards)
        offset %= cards
        return increment, offset

    # increment = 1
    # offset = 0
    # for i in range(10):
    #     offset += increment * offset_times_1_increment_diff
    #     offset %= cards
    #     increment *= one_increment
    #     increment %= cards
    #     print(increment, offset)
    #     print(get_magic(i+1))
    
    increment, offset = get_magic(101741582076661)
    print(get(offset, increment, 2020))
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
    # Part 1
# r"""
# deal with increment 7
# deal into new stack
# deal into new stack
# """,r"""
# cut 6
# deal with increment 7
# deal into new stack
# """,r"""
# deal with increment 7
# deal with increment 9
# cut -2
# """,r"""
# deal into new stack
# cut -2
# deal with increment 7
# cut 8
# cut -4
# deal with increment 7
# cut 3
# deal with increment 9
# deal with increment 3
# cut -1
# """,
r"""

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
