import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    for line in lines:
        l, r = line.split(' | ')
        left = l.split()
        left.sort(key=len)
        sprint(left)

        one = left[0]
        seven = left[1]
        four = left[2]
        five_ons = left[3:6]
        six_ons = left[6:9]

        # figure out top
        a = set(left[1]) - set(left[0])
        assert len(a) == 1
        a = next(iter(a))

        for five_on in five_ons:
            if set(five_on).issuperset(set(one)):
                three = five_on
                break
        else:
            assert False
        five_ons.remove(three)

        for six_on in six_ons:
            if not set(six_on).issuperset(set(one)):
                six = six_on
                break
        else:
            assert False
        six_ons.remove(six)

        # need 2590
        eight = left[9]

        c = set(one) - set(six)
        assert len(c) == 1
        c = next(iter(c))
        
        for five_on in five_ons:
            if c not in set(five_on):
                five = five_on
                break
        else:
            assert False
        five_ons.remove(five)

        # need 90
        assert len(five_ons) == 1
        two = five_ons[0]
        # need 90

        for six_on in six_ons:
            if set(six_on).issuperset(set(five)):
                nine = six_on
                break
        else:
            assert False
        six_ons.remove(nine)

        assert len(six_ons) == 1
        zero = six_ons[0]

        lmao = lmap(set, [zero, one, two, three, four, five, six, seven, eight, nine])

        temp = 0
        for what in r.split():
            temp *= 10
            # sprint(lmao)
            # sprint(what)
            for i, x in enumerate(lmao):
                if set(what) == set(x):
                    temp += i
                    break
            else:
                assert False
        out += temp

    
    
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
