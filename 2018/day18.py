map = """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
""".splitlines()

with open('in18.txt') as f:
    map = list(f)

map = [x.strip() for x in map if x.strip()]


def get(s, *a):
    if s == '.':
        if sum(x == '|' for x in a) > 2:
            return '|'
    if s == '|':
        if sum(x == '#' for x in a) > 2:
            return "#"
    if s == '#':
        if sum(x == '#' for x in a) == 0 or sum(x == '|' for x in a) == 0:
            return '.'
    return s


def print_map(map):
    for s in map:
        print(*s, sep='')


print_map(map)


def step(map):
    new = []
    mx = len(map)
    my = len(map[0])
    for x in range(mx):
        row = []
        for y in range(my):
            a = map[x - 1][y] if x > 0 else ''
            b = map[x][y - 1] if y > 0 else ''
            c = map[x][y + 1] if y + 1 < my else ''
            d = map[x + 1][y] if x + 1 < mx else ''
            e = map[x - 1][y - 1] if x > 0 and y > 0 else ''
            f = map[x - 1][y + 1] if x > 0 and y + 1 < my else ''
            g = map[x + 1][y - 1] if x + 1 < mx and y > 0 else ''
            h = map[x + 1][y + 1] if x + 1 < mx and y + 1 < my else ''
            n = get(map[x][y], a, b, c, d, e, f, g, h)
            # print((x,y), map[x][y], (a,b,c,d,e,f,g,h), '->', n)
            row.append(n)
        new.append(row)
    return new


results = []
for i in range(28 * 20 + 1000000000 % 28 + 1):
    map = step(map)

    res = (
        sum(x == '|' for r in map for x in r)
        ,
        sum(x == '#' for r in map for x in r)
    )

    print(f'{i:4}', res, res[0] * res[1])
    if res[0] * res[1] == 180725:
        print(i, res)

    results.append(res[0] * res[1])
