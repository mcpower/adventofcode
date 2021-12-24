def lmao(inputs):
    w=x=z=0
    w = inputs.pop()
    x = ((z % 26) + 10) != w
    if x:
        z *= 26
        z += (w + 12)
    w = inputs.pop()
    x = ((z % 26) + 10) != w
    if x:
        z *= 26
        z += (w + 10)
    w = inputs.pop()
    x = ((z % 26) + 12) != w
    if x:
        z *= 26
        z += (w + 8)
    w = inputs.pop()
    x = ((z % 26) + 11) != w
    if x:
        z *= 26
        z += (w + 4)
    w = inputs.pop()
    x = (z % 26) != w
    z //= 26
    if x:
        z *= 26
        z += (w + 3)
    w = inputs.pop()
    x = ((z % 26) + 15) != w
    if x:
        z *= 26
        z += (w + 10)
    w = inputs.pop()
    x = ((z % 26) + 13) != w
    if x:
        z *= 26
        z += (w + 6)
    w = inputs.pop()
    x = ((z % 26) + -12) != w
    z //= 26
    if x:
        z *= 26
        z += (w + 13)
    w = inputs.pop()
    x = ((z % 26) + -15) != w
    z //= 26
    if x:
        z *= 26
        z += (w + 8)
    w = inputs.pop()
    x = ((z % 26) + -15) != w
    z //= 26
    if x:
        z *= 26
        z += (w + 1)
    w = inputs.pop()
    x = ((z % 26) + -4) != w
    z //= 26
    if x:
        z *= 26
        z += (w + 7)
    w = inputs.pop()
    x = ((z % 26) + 10) != w
    if x:
        z *= 26
        z += (w + 6)
    w = inputs.pop()
    x = ((z % 26) + -5) != w
    z //= 26
    if x:
        z *= 26
        z += (w + 9)
    w = inputs.pop()
    x = ((z % 26) + -12) != w
    z //= 26
    if x:
        z *= 26
        z += (w + 9)
    return z == 0