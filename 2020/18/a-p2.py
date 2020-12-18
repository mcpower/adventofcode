import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    out = 0


    def eval_this(l: list):
        sprint(l)
        while "+" in l:
            plus = l.index("+")
            l[plus-1:plus+2] = [str(int(l[plus-1]) + int(l[plus+1]))]
        
        cur = int(l[0])
        for op, n in every_n(l[1:], 2):
            sprint(n, op)
            cur = eval(str(cur) + op + str(n))
        # replace all + with thingy.
        
        return cur

    for line in lines:
        tokens = list(line[::-1].replace(" ", ""))
        stack = [[]]
        while tokens:
            popped = tokens.pop()
            if popped == "(":
                stack.append([])
            elif popped == ")":
                stackpop = stack.pop()
                # eval this
                stack[-1].append(str(eval_this(stackpop)))
            else:
                stack[-1].append(popped)
        out += eval_this(stack[-1])
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
1 + (2 * 3) + (4 * (5 + 6))
""",r"""
1 + (2 * 3) + (4 * (5 + 6))
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
