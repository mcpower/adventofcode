import sys; sys.dont_write_bytecode = True; from utils import *

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    def sprint(*a, **k): sample and print(*a, **k)
    lines: typing.List[str] = inp.splitlines()
    paras: typing.List[typing.List[str]] = lmap(str.splitlines, inp.split("\n\n"))
    out = 0

    bits = "".join(bin(int(h, 16))[2:].zfill(4) for h in inp)
    # sprint(bits)
    # return
    MAP = {0: sum, 1: lambda s: reduce(operator.mul, s), 2: min, 3: max, 5: lambda x: x[0] > x[1], 6: lambda x: x[0] < x[1], 7:lambda x: x[0] == x[1]}
    
    def parse(i):
        nonlocal out
        version = int(bits[i:i+3], 2)
        out += version
        i += 3
        type = int(bits[i:i+3], 2)
        i += 3
        if type != 4:
            length_type = int(bits[i:i+1], 2)
            i += 1
            if length_type == 0:
                bit_length = int(bits[i:i+15], 2)
                i += 15
                sout = []
                target = i + bit_length
                while i < target:
                    sprint(i, target, bit_length)
                    a, i = parse(i)
                    sout.append(a)
                assert i == target
            else:
                subs = int(bits[i:i+11], 2)
                i += 11
                sout = []
                for _ in range(subs):
                    a, i = parse(i)
                    sout.append(a)
            assert type in MAP
            sout = int(MAP[type](sout))
            
            return sout, i
        else:
            num = []
            sprint(i)
            while bits[i] != '0':
                five = bits[i:i+5]
                i += 5
                num.append(five[1:])
            five = bits[i:i+5]
            i += 5
            num.append(five[1:])
            return int("".join(num), 2), i
    
    print(parse(0))
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
