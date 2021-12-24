def lmao(inputs):
    # w=x=z=0
    z = []
    w = 9
    z.append(w + 12)
    w = 3
    z.append(w + 10)
    w = 9
    z.append(w + 8)
    w = 5
    z.append(w + 4)
    w = 9
    x = z[-1] != w
    z.pop()
    if x:
        z.append(w + 3)
    w = 9
    z.append(w + 10)
    w = 9
    z.append(w + 6)
    w = 3 #l19
    x = z[-1] != w + 12
    z.pop()
    if x:
        z.append(w + 13)
    w = 4 #l17
    x = z[-1] != w + 15
    z.pop()
    if x:
        z.append(w + 8)
    w = 2 #l9
    x = z[-1] != w + 15
    z.pop()
    if x:
        z.append(w + 1)
    w = 9 #l7
    x = z[-1] != w + 4
    z.pop()
    if x:
        z.append(w + 7)
    w = 8
    z.append(w + 6)
    w = 9
    x = z[-1] != w + 5
    z.pop()
    if x:
        z.append(w + 9)
    w = 9 #l5
    x = z[-1] != w + 12
    z.pop()
    if x:
        z.append(w + 9)
    return z == 0