import sys; sys.dont_write_bytecode = True; from utils import *

DIFF_COUNTS = list(Counter(i+j+k for i in range(1, 4) for j in range(1, 4) for k in range(1, 4)).items())

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()

    p1 = int(lines[0].split()[-1])
    p2 = int(lines[1].split()[-1])

    @functools.lru_cache(maxsize=None)
    def wins(p1, p2, p1score=0, p2score=0):
        if p1score >= 21:
            return (1, 0)
        if p2score >= 21:
            return (0, 1)
        p1_wins = 0
        p2_wins = 0
        for diff, count in DIFF_COUNTS: 
            new_p1 = ((p1+diff-1)%10)+1
            p2_child_wins, p1_child_wins = wins(p2, new_p1, p2score, p1score+new_p1)
            p1_wins += count*p1_child_wins
            p2_wins += count*p2_child_wins
        return (p1_wins, p2_wins)

    print(max(wins(p1, p2)))
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
Player 1 starting position: 4
Player 2 starting position: 8

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
