import hashlib


md5 = lambda x: hashlib.md5(bytes(x, "utf-8")).hexdigest()
SAMPLE = False
if SAMPLE:
	inp = "abc"
else:
	# this was my input apparently
	inp = "ugkcyxxp"

password = list("XXXXXXXX")
many = 0
cur = 0
while many < 8:
	m = md5(inp + str(cur))
	if m[:5] == "0"*5:
		print(m)
		print(password)
		pos = int(m[5], 16)
		if pos >= 8 or password[pos] != "X":
			print("bad!")
		else:
			password[pos] = m[6]
			many += 1
	cur += 1
print("".join(password))
