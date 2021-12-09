# This is verbatim from my phone, written entirely in vim using a touch
# keyboard. There was no sample running, so I got a wrong answer for part 1 :P
inp = open("input.txt").read().splitlines()
out = 0
rows = len(inp)
cols = len(inp[0])
for r in range(rows):
    for c in range(cols):
        q = inp[r][c]
        adj=[]
        for dr, dc in [[-1, 0], [1, 0], [0, 1], [0, -1]]:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                adj.append(inp[nr][nc])
        if all(i > q for i in adj):
            out += 1 + int(q)
print(out)

seen = [[False]*cols for _ in range(cols)]
def dfs(r, c):
    if not (0 <= r < rows and 0 <= c < cols):
        return 0
    if seen[r][c]:
        return 0
    seen[r][c] = True
    if inp[r][c] == '9':
        return 0
    out = 1
    for dr, dc in [[-1, 0], [1, 0], [0, 1], [0, -1]]:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            out += dfs(nr, nc)
    return out

sizes = []
for r in range(rows):
    for c in range(cols):
        sizes.append(dfs(r, c))
sizes.sort()
out = 1
for x in (sizes[-3:]):
    out *= x
print(out)
