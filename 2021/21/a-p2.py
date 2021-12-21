import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    die = 1
    times_rolled = 0

    # def roll():
    #     nonlocal die, times_rolled
    #     if die == 101:
    #         die = 1
    #     out = die
    #     die += 1
    #     times_rolled += 1
    #     return out

    p1 = ints(lines[0])[-1]
    p2 = ints(lines[1])[-1]

    # p1score = 0
    # p2score = 0

    # while p1score < 1000 and p2score < 1000:
    #     p1 += roll()+roll()+roll()
        # p1 = ((p1-1)%10)+1
    #     # sprint(p1)
    #     p1score += p1
    #     if p1score >= 1000:
    #         break
    #     p2 += roll()+roll()+roll()

    #     p2 = ((p2-1)%10)+1
    #     p2score += p2
    
    # print(p1score, p2score, times_rolled)
    # out = min(p1score, p2score) * times_rolled

    @functools.lru_cache(maxsize=None)
    def copies(p1, p2, p1score, p2score, is_p1, cur_roll, rolls):
        if p1score >= 21:
            return (1, 0)
        if p2score >= 21:
            return (0, 1)
        out = (0, 0)
        if rolls != 3:
            for i in range(1,4):
                out = padd(out, copies(p1, p2, p1score, p2score, is_p1, cur_roll+i, rolls+1))
        else:
            cur = p1 if is_p1 else p2
            cur += cur_roll
            cur = ((cur-1)%10)+1
            if is_p1:
                out = padd(out, copies(cur, p2, p1score+cur, p2score, not is_p1, 0, 0))
            else:
                out = padd(out, copies(p1, cur, p1score, p2score+cur, not is_p1, 0, 0))
        return tuple(out)

    out = copies(p1, p2, 0, 0, True, 0, 0)
    if out:
        print("out:    ", out)
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
