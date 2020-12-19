from re import match
import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines = inp.splitlines()
    paras = inp.split("\n\n")
    out = 0

    rules, messages = paras

    rule_dict = {}

    for rule in rules.splitlines():
        num, rule = rule.split(": ")
        thing = None
        if '"' in rule:
            thing = rule[1]
        else:
            thing = [ints(x) for x in rule.split(" | ")]
            # thing = every_n(ints(rule), 2)
        rule_dict[int(num)] = thing
    sprint(rule_dict)
    def matches(s: str, i: int, rule_num: int):
        # sprint(i)
        if i >= len(s):
            return set()
        rule = rule_dict[rule_num]
        out = set()
        if type(rule) == str:
            if s[i] == rule:
                return {i+1}
        else:
            for variation in rule:
                cur = {i}
                for new_rule in variation:
                    cur = set(y for x in cur for y in matches(s, x, new_rule))
                out.update(cur)
        
        return out
    
    def match_all(s):
        return len(s) in matches(s, 0, 0)
    
    for message in messages.splitlines():
        # print(message)
        if match_all(message):
            out += 1
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
