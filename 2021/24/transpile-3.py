def lmao(inputs):
    # w=x=z=0
    z = []
    w = inputs.pop()
    z.append(w + 12)
    w = inputs.pop()
    z.append(w + 10)
    w = inputs.pop()
    z.append(w + 8)
    w = inputs.pop()
    z.append(w + 4)
    w = inputs.pop()
    x = z[-1] != w
    z.pop()
    if x:
        z.append(w + 3)
    w = inputs.pop()
    z.append(w + 10)
    w = inputs.pop()
    z.append(w + 6)
    w = inputs.pop()
    x = z[-1] != w + 12
    z.pop()
    if x:
        z.append(w + 13)
    w = inputs.pop()
    x = z[-1] != w + 15
    z.pop()
    if x:
        z.append(w + 8)
    w = inputs.pop()
    x = z[-1] != w + 15
    z.pop()
    if x:
        z.append(w + 1)
    w = inputs.pop()
    x = z[-1] != w + 4
    z.pop()
    if x:
        z.append(w + 7)
    w = inputs.pop()
    z.append(w + 6)
    w = inputs.pop()
    x = z[-1] != w + 5
    z.pop()
    if x:
        z.append(w + 9)
    w = inputs.pop()
    x = z[-1] != w + 12
    z.pop()
    if x:
        z.append(w + 9)
    return z == 0