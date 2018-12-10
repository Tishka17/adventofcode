from collections import defaultdict
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


infinites = defaultdict(lambda: False)
cc = defaultdict(lambda: 0)
for x in range(w):
    for y in range(h):
        cnt = 0
        best_d = None
        best_i = 0
        for i, c in enumerate(coords):
            d = dist(c, (x, y))
            if best_d is None or d < best_d:
                best_d = d
                cnt = 1
                best_i = i
            elif best_d == d:
                cnt += 1
        if cnt == 1:
            cc[best_i] += 1
            if x == 0 or y == 0 or x == w - 1 or y == h - 1:
                infinites[best_i] = True
    #         print(ascii_letters[best_i], end="")
    #     else:
    #         print(".", end="")
    # print()
for i in sorted(list(cc.keys())):
    print(f"{i}({ascii_letters[i]}): {cc[i]} \tat {coords[i]}")
res = max((x for x in cc.items() if not infinites[x[0]]), key=lambda x: x[1])
print(f"max_i={res[0]}, count={res[1]}, point={coords[res[0]]}, letter={ascii_letters[res[0]]}")
