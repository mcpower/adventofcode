from itertools import *
import math

SAMPLE = 0

if SAMPLE:
    a = r"""
10
""".strip()
else:
    a = open("inp.txt").read().strip()


# l = [list(map(int, s.split())) for s in a.split("\n")] 
a = int(a)
i = 1
step = 1
togo = a - i
out = [0, 0]
while togo:
    n = min(togo, step)
    out[0] += n
    togo -= n


    n = min(togo, step)
    out[1] += n
    togo -= n

    step += 1

    n = min(togo, step)
    out[0] -= n
    togo -= n


    n = min(togo, step)
    out[1] -= n
    togo -= n

    step += 1
print(sum(map(abs,out)))

# grid[SIZE][SIZE] is middle
SIZE = 1000

s = SIZE * 2 + 1
grid = [[None]*(s) for i in range(s)]

i = 1
step = 1
cur = [SIZE, SIZE]

grid[cur[0]][cur[1]] = 1


while 1:
    for _ in range(step):
        cur[0] += 1
        grid[cur[0]][cur[1]] = sum(grid[x][y] for x in [cur[0]-1, cur[0]+0, cur[0]+1] for y in [cur[1]-1, cur[1]+0, cur[1]+1] if grid[x][y])
        if grid[cur[0]][cur[1]] > a:
            print(grid[cur[0]][cur[1]])
            quit()

    for _ in range(step):
        cur[1] += 1
        grid[cur[0]][cur[1]] = sum(grid[x][y] for x in [cur[0]-1, cur[0]+0, cur[0]+1] for y in [cur[1]-1, cur[1]+0, cur[1]+1] if grid[x][y])
        if grid[cur[0]][cur[1]] > a:
            print(grid[cur[0]][cur[1]])
            quit()

    step += 1


    for _ in range(step):
        cur[0] -= 1
        grid[cur[0]][cur[1]] = sum(grid[x][y] for x in [cur[0]-1, cur[0]+0, cur[0]+1] for y in [cur[1]-1, cur[1]+0, cur[1]+1] if grid[x][y])
        if grid[cur[0]][cur[1]] > a:
            print(grid[cur[0]][cur[1]])
            quit()

    for _ in range(step):
        cur[1] -= 1
        grid[cur[0]][cur[1]] = sum(grid[x][y] for x in [cur[0]-1, cur[0]+0, cur[0]+1] for y in [cur[1]-1, cur[1]+0, cur[1]+1] if grid[x][y])
        if grid[cur[0]][cur[1]] > a:
            print(grid[cur[0]][cur[1]])
            quit()

    step += 1
