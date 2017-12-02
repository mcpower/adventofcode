from copy import deepcopy
from pprint import pprint
SAMPLE = False
if SAMPLE:
	inp = """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1"""
else:
	inp = """paste
your
input"""

board = [[False]*50 for i in range(6)]

for line in inp.split("\n"):
	first, *rest = line.split()
	if first == "rect":
		x, y = map(int, rest[0].split("x"))
		for i in range(x):
			for j in range(y):
				board[j][i] = True
	elif first == "rotate":
		ty, pos, _, num = rest
		pos = int(pos[2:])
		num = int(num)
		old = deepcopy(board)
		if ty == "column":
			for i in range(6):
				board[i][pos] = old[(i-num) % 6][pos]
		else:
			for i in range(50):
				board[pos][i] = old[pos][(i-num) % 50]
	"""
	for i in range(6):
		for j in range(50):
			print(".#"[board[i][j]], end="")
		print()
	"""

print(sum(sum(i) for i in board))
for i in range(6):
	for j in range(50):
		print(".#"[board[i][j]], end="")
	print()
