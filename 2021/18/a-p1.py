import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0


    # def explode(x, depth=0, to_add=0):
    #     # Returns (left add, cur, right add)
    #     if isinstance(x, list):
    #         if depth == 4:
    #             assert len(x) == 2
    #             a, b = x
    #             return a, 0, b
            
    #         new_out = []
    #         for i in x:
    #             left, cur, right = explode(i, depth+1, to_add)
    #             to_add += right
    #             new_out.append(cur)
    #         return 
    #     else:
    #         return x + to_add

    def to_i_depth(nested, depth=0):
        if isinstance(nested, list):
            return [y for x in nested for y in to_i_depth(x, depth+1)]
        else:
            return [(nested, depth)]
        
    def explode(i_depths):
        new_i_depths = []
        to_add = 0
        seen = 0
        for i, (n, depth) in enumerate(i_depths):
            if depth >= 5:
                if seen == 1:
                    to_add = n
                    new_i_depths.append((0, depth-1))
                elif seen == 0:
                    if new_i_depths:
                        new_i_depths[-1] = list(new_i_depths[-1])
                        new_i_depths[-1][0] += n
                        new_i_depths[-1] = tuple(new_i_depths[-1])
                else:
                    new_i_depths.append((n+to_add, depth))
                    to_add = 0
                seen += 1
            else:
                new_i_depths.append((n+to_add, depth))
                to_add = 0
        if seen:
            assert seen >= 2
        return new_i_depths, seen > 0

    def split(i_depths):
        new_i_depths = []
        seen = False
        for i, (n, depth) in enumerate(i_depths):
            if n >= 10 and not seen:
                new_i_depths.append(((n)//2, depth+1))
                new_i_depths.append(((n+1)//2, depth+1))
                seen = True
            else:
                new_i_depths.append((n, depth))
        return new_i_depths, seen
    
    def simplify(x):
        x, a = explode(x)
        # sprint(x)
        if not a:
            x, a = split(x)
            # sprint(x)
        while a:
            x, a = explode(x)
            # sprint(x)
            if not a:
                x, a = split(x)
                # sprint(x)
        return x

    
    def deepify(x):
        return [(n, depth+1) for n, depth in x]
    def add(a, b):
        return deepify(a) + deepify(b)
    
    def to_pair(x):
        out = []
        for n, depth in x:
            while len(out) < depth:
                out.append([])
            while len(out) > depth:
                popped = out.pop()
                out[-1].append(popped)
            
                while len(out[-1]) == 2 and len(out) != 1:
                    popped = out.pop()
                    out[-1].append(popped)
            while len(out[-1]) == 2 and len(out) != 1:
                popped = out.pop()
                out[-1].append(popped)
            out[-1].append(n)
            while len(out[-1]) == 2 and len(out) != 1:
                popped = out.pop()
                out[-1].append(popped)
        while len(out) > 1:
            popped = out.pop()
            out[-1].append(popped)
        return out[0]

    def mag(x):
        if isinstance(x, int):
            return x
        else:
            sprint(x)
            a, b = x
            return 3*mag(a) + 2*mag(b)
            
    
    cur = to_i_depth(eval(lines[0]))
    cur = simplify(cur)
    # sprint(cur)
    # sprint(lmap(fst, cur))


    for line in lines[1:]:
        cur = add(cur, to_i_depth(eval(line)))
        cur = simplify(cur)
        # sprint(lmap(fst, cur))
    # sprint(to_pair(cur))
    out = mag(to_pair(cur))
    
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
