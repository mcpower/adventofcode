import re

import string
al = string.ascii_lowercase

SAMPLE = False

if SAMPLE:
	inp = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""
else:
	inp = """paste
your
input"""


shifter = lambda n: lambda c: chr((ord(c)-ord("a") + n)%26 + ord("a")) if c != " " else " "
filtered = []
out = 0
for line in inp.split():
	h = line[-6:-1]
	*l, x = line[:-7].split("-")
	l2 = "".join(l)
	#print(l2)
	should = "".join(sorted(al, key = lambda c: (-l2.count(c), c))[:5])
	# print(should, h, x, should == h)
	if should == h:
		out += int(x)
		s = "".join(map(shifter(int(x)), " ".join(l)))
		if "north" in s:
			print(s, x)

print(out)
# not sure where this came from - probably my data?
print("".join(map(shifter(343), " ".join("qzmt-zixmtkozy-ivhz".split("-")))))
