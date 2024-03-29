import sys; sys.dont_write_bytecode = True; from utils import *

import mcparser

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    bits = "".join(bin(int(h, 16))[2:].zfill(4) for h in inp)
    MAP = {0: sum, 1: lambda s: reduce(operator.mul, s), 2: min, 3: max, 5: lambda x: x[0] > x[1], 6: lambda x: x[0] < x[1], 7:lambda x: x[0] == x[1]}
    
    bits_parser = lambda n: mcparser.char.filter(lambda c: c in "01").timesstr(n)
    int_parser = lambda n: bits_parser(n).map(lambda s: int(s, 2))

    @mcparser.DoParser
    def parse() -> typing.Generator[mcparser.Parser[typing.Any], typing.Any, int]:
        nonlocal out
        version: int = yield int_parser(3)
        out += version
        type: int = yield int_parser(3)
        if type != 4:
            length_type: int = yield int_parser(1)
            if length_type == 0:
                bit_length: int = yield int_parser(15)
                sout: typing.List[int] = yield parse.rep_until_chars(bit_length)
            else:
                subs: int = yield int_parser(11)
                sout: typing.List[int] = yield parse.times(subs)
            assert type in MAP
            sout2 = int(MAP[type](sout))
            
            return sout2
        else:
            num = []
            while True:
                five: str = yield bits_parser(5)
                num.append(five[1:])
                if five[0] == '0':
                    break
            return int("".join(num), 2)
    
    # Might have leading zeroes.
    print(parse.parse_partial(bits, 0))
    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
r"""
38006F45291200
""",r"""
EE00D40C823060
""",r"""
8A004A801A8002F478
""",r"""
620080001611562C8802118E34
""",r"""
C0015000016115A2E0802F182340
""",r"""
A0016C880162017C3686B18A3D4780
""",r"""
9C0141080250320F1802104A08
"""], do_case)
