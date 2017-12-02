PART2 = False
inp = "paste your input"
inp2 = [(s[0], int(s[1:])) for s in inp.split(", ")]
cur_dir = 0+1j
cur_pos = 0+0j
seen = {cur_pos}
for direction, num in inp2:
    cur_dir *= 1j * (2*(direction == "L") - 1)
    for i in range(num):
        cur_pos += cur_dir
        if PART2 and cur_pos in seen:
            break
        seen.add(cur_pos)
    else:
        continue
    break
print(abs(cur_pos.imag) + abs(cur_pos.real))
