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
    out = 0
    REQUIRED= {"byr",
"iyr",
"eyr",
"hgt",
"hcl",
"ecl",
"pid"}

    seen = dict()

    def check():
        nonlocal seen, out
        diff = REQUIRED - set(seen)
        if diff != set():
            return
        
        if not (1920 <= int(seen["byr"]) <= 2002 and
            2010 <= int(seen["iyr"]) <= 2020 and
            2020 <= int(seen["eyr"]) <= 2030):
            return
        
        height = seen["hgt"]
        lol = ints(height)[0]
        if not height.endswith(("cm", "in")):
            return
        
        if height.endswith("cm") and not (150 <= lol <= 193):
            return
        if height.endswith("in") and not (59 <= lol <= 76):
            return
        
        if not re.match(r"#[0-9a-f]{6}", seen["hcl"]):
            return
        
        if seen["ecl"] not in "amb blu brn gry grn hzl oth".split():
            return
        
        if len(seen["pid"]) != 9 or not seen["pid"].isnumeric():
            return

        out += 1


    for line in lines:
        if not line:
            check()
            seen.clear()
        q = line.split()
        for i in q:
            a,b = i.split(":")
            assert a not in seen
            seen[a] = b
    
    check()
    
    print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
""",r"""
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
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
