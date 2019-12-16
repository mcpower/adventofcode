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
    start = lmap(int, lines[0] * 10000 )

    def get_base(pos):
        # pos is 0-ondexed
        repeat = pos + 1
        pat = [0] * repeat + [1] * repeat + [0] * repeat + [-1] * repeat
        x = itertools.cycle(pat)
        next(x)
        return x
    
    # n = 100
    # out = [0] * n
    # # for index i
    # # consider i % 4, i % 8, i % 16, ...
    # for i in range(n):
    #     q = list(itertools.islice(get_base(i), n))
    #     out = padd(q, out)
    # print(out)

    # OOOOOPS
    # def magic(n):
    #     out = [0] * (n + 1)

    #     for i in range(n+1):
    #         for j in range(n+1):
    #             width = j+1
    #             modulus = width * 4
    #             # 0 1 2 3
    #             block = (i % modulus) // width
    #             if block == 1:
    #                 out[i] += 1
    #             elif block == 3:
    #                 out[i] -= 1

    #     return out[1:]

    def partial_sums(inp):
        out = [0]
        for i in inp:
            out.append(out[-1] + i)
        return out
    
    def sum_between(sums, i, j):
        # inc, exc
        return sums[min(j, len(sums)-1)] - sums[i]

    def phase(inp):
        # inp is list of ints
        out = []
        sums = partial_sums(inp)
        n = len(inp)
        for i in range(n):
            width = i + 1
            blah = 0
            for j in range(n):
                # 0 1 0 -1 0 1  0 -1
                # 0 0 1  1 0 0 -1 -1
                start = (j*2 + 1) * width - 1
                end = start + width
                # sprint("??")
                if start > n:
                    break
                to_mod = sum_between(sums, start, end)
                # sprint(to_mod)
                if j % 2 == 0:
                    blah += to_mod
                else:
                    blah -= to_mod
            blah = abs(blah)
            out.append(blah % 10)

        return out
    
    offset = int("".join(map(str,start[:7])))
    # sprint(start)
    for _ in range(100):
        start = phase(start)
        
    
    print("".join(lmap(str, start))[offset:offset+8])
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
03036732577212944063491565474664
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
