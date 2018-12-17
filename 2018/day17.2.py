#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from dataclasses import dataclass
from typing import List, Tuple

from PIL import Image

UNDERLINE = "\033[4m"
BOLD = "\033[1m"
DIM = "\033[90m"
BLUE = "\033[36m"
BLUE2 = "\033[96m"
BLUE3 = "\033[94m"
BLUE4 = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
MAGENTA = "\033[35m"
RED = "\033[91m"
NORMAL = "\033[0m"


@dataclass
class Range:
    x0: int
    x1: int
    y0: int
    y1: int

    def inside(self, x: int, y: int):
        return self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1


def get_two_coords(s: str) -> Tuple[int, int]:
    eq = s.index("=")
    if eq >= 0:
        s = s[eq + 1:]
    if "." in s:
        return tuple(map(int, s.split("..")))
    return int(s), int(s)


Ranges = List[Range]
Map = List[List[str]]

spring_x = 500
spring_y = 0

data = """
x=1, y=1..10
y=10, x=1..10
x=10, y=2..10
x=3, y=3..7
y=7, x=3..7
x=7, y=3..7
x=11, y=10
x=17, y=10
""".splitlines(keepends=False)

data = """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
""".splitlines(keepends=False)

# data = """
# x=502, y=1..4
# x=499, y=2..4
# y=3, x=500..500
# y=4, x=499..502
# """.splitlines(keepends=False)


# data = """
# x=1, y=1..10
# y=4, x=1..5
# x=3..5, y=2
# x=10, y=10
# """.splitlines(keepends=False)


with open("in17.txt") as f:
    data = f.read().splitlines(keepends=False)


def load(data):
    ranges = []
    for s in data:
        s = s.strip()
        if not s:
            continue
        x, y = s.split(", ")
        if x[0] == "y":
            x, y = y, x
        x0, x1 = get_two_coords(x)
        y0, y1 = get_two_coords(y)
        ranges.append(Range(x0, x1, y0, y1))
    return ranges


def create_map(w, h) -> Map:
    return [
        ["."] * w for _ in range(h)
    ]


def print_map(map: Map):
    for y, row in enumerate(map):
        print(f"{y:5} ", end="")
        for s in row:
            if s in "|~":
                print(s, end="")
            else:
                print(s, end="")
        print()
    print()


ranges: Ranges = load(data)
min_y = min(r.y0 for r in ranges)
max_y = max(r.y1 for r in ranges)
min_x = min(r.x0 for r in ranges) - 1
max_x = max(r.x1 for r in ranges) + 1

print(min_x, max_x, min_y, max_y)

map = create_map(max_x - min_x + 1, max_y - min_y + 1)
# normalize
spring_x = spring_x - min_x
spring_y = 0
for r in ranges:
    r.x0 -= min_x
    r.y0 -= min_y
    r.x1 -= min_x
    r.y1 -= min_y

for r in ranges:
    for x in range(r.x0, r.x1 + 1):
        for y in range(r.y0, r.y1 + 1):
            map[y][x] = "#"


# print_map(map)
# print()


def fill_left(map: Map, x0: int, y: int):
    count = 0
    for x in range(x0, -1, -1):
        if map[y][x] != "#":
            if map[y][x] == ".":
                count += 1
            map[y][x] = "~"
            if map[y + 1][x] != "#":
                c, forever = fill_down(map, x, y + 1)
                count += c
                if forever:
                    for x1 in range(x, x0 + 1):
                        map[y][x1] = "."
                    return count, True
        else:
            return count, False
    return count, True


def fill_right(map: Map, x0: int, y: int):
    count = 0
    for x in range(x0, len(map[0])):
        if map[y][x] != "#":
            if map[y][x] == ".":
                count += 1
            map[y][x] = "~"
            if map[y + 1][x] != "#" and (map[y + 1][x - 1] in "#" or x == x0):
                c, forever = fill_down(map, x, y + 1)
                count += c
                if forever:
                    for x1 in range(x0, x + 1):
                        map[y][x1] = "."
                    return count, True
        else:
            return count, False
    return count, True


cache = {}


def fill_down(map: Map, x: int, y0: int) -> (int, bool):
    if (x, y0) not in cache:
        cache[(x, y0)] = fill_down_impl(map, x, y0)
    return cache[(x, y0)]


def fill_down_impl(map: Map, x: int, y0: int) -> (int, bool):
    sys.stderr.write("down: %s %s\n" % (x, y0))
    count = 0
    max_y = len(map)
    for y in range(y0, len(map)):
        if map[y][x] != "#":
            if map[y][x] == ".":
                count += 1
            map[y][x] = "|"
            max_y = y
        else:
            break
    else:
        for y in range(y0, len(map)):
            map[y][x] = "."
        return count, True
    # fill
    # print_map(map)
    for y in range(max_y, y0 - 1, -1):
        forever = False
        if x > 0 and map[y][x - 1] != "#":
            c, f = fill_left(map, x - 1, y)
            forever |= f
            count += c
        if x < len(map[0]) and map[y][x + 1] != "#":
            c, f = fill_right(map, x + 1, y)
            forever |= f
            count += c
        if forever:
            for y1 in range(y0, y + 1):
                map[y1][x] = "."
            return count, True
    return count, False


c, f = fill_down(map, spring_x, spring_y)
print(c, f)


def cleanup_row(row):
    for i in range(len(row)):
        if row[i] in "~|" and (i > len(row) - 1 or row[i + 1] == "."):
            j = i
            sys.stderr.write("".join(row[i-10:i+1]))
            while row[j] in "~|":
                row[j] = "."
                j -= 1
            sys.stderr.write("Edge detected: %s, %s\n" % (i, j))
            sys.stderr.write("".join(row[i-10:i+1]))
        if row[i] in "." and i < len(row) - 1 and row[i + 1] in "~|":
            # sys.stderr.write("".join(row[i-10:i+10]))
            row[i + 1] = "."


for y, row in enumerate(map):
    sys.stderr.write("Clean %s\n" % y)
    cleanup_row(row)

count = 0
for row in map:
    for s in row:
        if s in "~|":
            count += 1

print("Result: ", count)

print_map(map)

img = Image.new("RGB", (len(map[0]), len(map)), 0x009999)

for y, row in enumerate(map):
    for x, s in enumerate(row):
        if s in "|":
            img.putpixel((x, y), 0xff0000)
        elif s in "~":
            img.putpixel((x, y), 0xff8888)
        elif s == '#':
            img.putpixel((x, y), 0x0000ff)
img.save("o17.png")

# 49608 > res
