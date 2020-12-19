from re import match
import sys; sys.dont_write_bytecode = True; from utils import *
# sys.setrecursionlimit(100)

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
    rule_dict[8] = [[42]*i for i in range(1, 80)]
    rule_dict[11] = [[42]*i + [31]*i for i in range(1, 80)]
    # sprint(rule_dict)
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
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
