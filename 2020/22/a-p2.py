import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    out = 0

    one, two = paras
    one = ints(one)[1:]
    two = ints(two)[1:]

    def score(winner):
        out = 0
        for i, x in enumerate(list(winner)[::-1]):
            out += (i+1) * x
        return out
    
    # @functools.lru_cache(maxsize=None)
    def one_won_and_winner(one, one_card, two, two_card):
        # print(one, one_card, two, two_card)
        if len(one) >= one_card and len(two) >= two_card:
            pass
        else:
            if one_card > two_card:
                return True, score(one)
            else:
                return False, score(two)
        one = one[:one_card]
        two = two[:two_card]
        one = deque(one)
        two = deque(two)
        seen = set()  # (tuple(one), tuple(two))
        while one and two:
            hashed = (tuple(one), tuple(two))
            if hashed in seen:
                return True, score(one)
            seen.add(hashed)
            one_card = one.popleft()
            two_card = two.popleft()

            if one_won_and_winner(tuple(one), one_card, tuple(two), two_card)[0]:
                one.append(one_card)
                one.append(two_card)
            else:
                two.append(two_card)
                two.append(one_card)
        if one:
            return True, score(one)
        else:
            return False, score(two)
            


    print(one_won_and_winner(one, len(one), two, len(two)))



    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10

""",r"""
Player 1:
43
19

Player 2:
2
29
14

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
