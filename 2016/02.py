dirs = dict(zip("UDLR", [-1j, 1j, -1+0j, 1+0j]))
inp = """ULL
RRDDD
LURDL
UUUUD"""  # paste in your input

# part 1
to_digit = lambda c: int(c.real) + 3 * int(c.imag) + 1
pos = 1+1j
out = []
for line in inp.split():
    for char in line:
        pos += dirs[char]
        if not (0 <= pos.real <= 2 and 0 <= pos.imag <= 2):
            pos -= dirs[char]
    out.append(to_digit(pos))
print("".join(map(str,out)))

# part 2
keypad = "  1  | 234 |56789| ABC |  D  ".split("|")
to_new_digit = lambda c: keypad[int(c.imag)+2][int(c.real)+2] if (abs(pos.real) + abs(pos.imag) <= 2) else " "
pos = -2+0j  # When I solved this, I set this to 0+0j. I managed to get it somehow correct?
out = []
for line in inp.split():
    for char in line:
        pos += dirs[char]
        if to_new_digit(pos) == " ":
            pos -= dirs[char]
    out.append(to_new_digit(pos))
print("".join(map(str,out)))
