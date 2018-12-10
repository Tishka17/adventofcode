from string import ascii_letters

with open("in6.txt") as f:
    coords = [x.split(', ') for x in f if x]

coords = [
    (int(x[0]), int(x[1])) for x in coords
]

w = max(map(lambda x: x[0], coords))
h = max(map(lambda x: x[1], coords))
print(f"w={w}, h={h}")


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


cnt = 0
for x in range(w):
    for y in range(h):
        s = sum(map(lambda c: dist(c, (x, y)), coords))
        if s < 10000:
            cnt += 1

print(f"{cnt}")
