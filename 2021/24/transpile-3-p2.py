def lmao(inputs):
    # w=x=z=0
    z = []
    w = 1
    z.append(w + 12)
    w = 1
    z.append(w + 10)
    w = 8
    z.append(w + 8)
    w = 1
    z.append(w + 4)
    w = 5 # l11
    x = z[-1] != w
    z.pop()
    if x:
        z.append(w + 3)
    w = 6
    z.append(w + 10)
    w = 7
    z.append(w + 6)
    w = 1 #l20
    x = z[-1] != w + 12
    z.pop()
    if x:
        z.append(w + 13)
    w = 1 #l18
    x = z[-1] != w + 15
    z.pop()
    if x:
        z.append(w + 8)
    w = 1 #l9
    x = z[-1] != w + 15
    z.pop()
    if x:
        z.append(w + 1)
    w = 7 #l7
    x = z[-1] != w + 4
    z.pop()
    if x:
        z.append(w + 7)
    w = 1
    z.append(w + 6)
    w = 2 # above lol
    x = z[-1] != w + 5
    z.pop()
    if x:
        z.append(w + 9)
    w = 1 #l5
    x = z[-1] != w + 12
    z.pop()
    if x:
        z.append(w + 9)
    return z == 0