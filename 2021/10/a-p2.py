import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0
    out2 = []

    WTF = {"(": ")", "{": "}", "<": ">", "[": "]"}
    WAT = {")": 3, "}": 1197, ">": 25137, "]": 57}
    WAT2 = {"(": 1, "{": 3, "<": 4, "[": 2}


    for line in lines:
        stack = []
        for x in line:
            if x in "([<{":
                stack.append(x)
            else:
                c = stack.pop()
                if WTF[c] != x:
                    out += WAT[x]
                    break
        else:
            w = 0
            stack.reverse()
            for x in stack:
                w *= 5
                w += WAT2[x]
            out2.append(w)
    
    out2.sort()
    print(out2[len(out2)//2 ])
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
