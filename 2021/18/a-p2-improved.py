import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    def to_i_depth(nested, depth=0):
        if isinstance(nested, list):
            return [y for x in nested for y in to_i_depth(x, depth+1)]
        else:
            return [(nested, depth)]
        
    def explode(n_depths):
        out = []
        to_add = 0
        seen = 0
        for n, depth in n_depths:
            if depth >= 5:
                if seen == 1:
                    to_add = n
                elif seen == 0:
                    if out:
                        out[-1] = list(out[-1])
                        out[-1][0] += n
                        out[-1] = tuple(out[-1])
                    out.append((0, depth-1))
                else:
                    out.append((n+to_add, depth))
                    to_add = 0
                seen += 1
            else:
                out.append((n+to_add, depth))
                to_add = 0
        if seen:
            assert seen >= 2
        return out, seen > 0

    def split(n_depths):
        out = []
        seen = False
        for n, depth in n_depths:
            if n >= 10 and not seen:
                out.append(((n)//2, depth+1))
                out.append(((n+1)//2, depth+1))
                seen = True
            else:
                out.append((n, depth))
        return out, seen
    
    def simplify(n_depths):
        a = True
        while a:
            n_depths, a = explode(n_depths)
            if not a:
                n_depths, a = split(n_depths)
        return n_depths

    def add(a, b):
        return simplify([(n, depth+1) for n, depth in a+b])
    
    def to_nested_lists(n_depths):
        out = []
        for n, depth in n_depths:
            while len(out) < depth:
                out.append([])
            while len(out) > depth:
                popped = out.pop()
                out[-1].append(popped)
            out[-1].append(n)
            while len(out[-1]) == 2 and len(out) != 1:
                popped = out.pop()
                out[-1].append(popped)
        assert len(out) == 1
        return out[0]

    def mag(x):
        if isinstance(x, int):
            return x
        else:
            a, b = x
            return 3*mag(a) + 2*mag(b)
    
    def process_line(line):
        return to_i_depth(eval(line))


    numbers = lmap(process_line, lines)

    part1 = mag(to_nested_lists(reduce(add, numbers)))
    print(part1)

    part2 = 0
    for i, x in enumerate(numbers):
        for j, y in enumerate(numbers):
            if i != j:
                part2 = max(part2, mag(to_nested_lists(add(x, y))))
    print(part2)
        
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
[1,1]
[2,2]
[3,3]
[4,4]


""",r"""
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]

""",r"""
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]

""",r"""
[[[[[9,8],1],2],3],4]
""",r"""
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]


""",r"""
[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]
""",r"""
[[[[4,3],4],4],[7,[[8,4],9]]]
[1,1]
""",
r"""
[7,[6,[5,[4,[3,2]]]]]

""",
"""
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]

"""
], do_case)
