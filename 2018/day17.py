#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Tuple

from dataclasses import dataclass


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
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
""".splitlines(keepends=False)


# with open("in17.txt") as f:
#     data = f.read().splitlines(keepends=False)

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
        print(f"{y:3} ", *row, sep="")
    print()


ranges: Ranges = load(data)
min_y = min(r.y0 for r in ranges)
max_y = max(r.y1 for r in ranges)
min_x = min(r.x0 for r in ranges)
max_x = max(r.x1 for r in ranges)

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

print_map(map)
print()


def fill_left(map: Map, x: int, y: int):
    count = 0
    for x in range(x, -1, -1):
        if map[y][x] == ".":
            map[y][x] = "~"
            count += 1
            if map[y + 1][x] == ".":
                c, forever = fill_down(map, x, y + 1)
                count += c
                if forever:
                    return count, True
        else:
            return count, False
    return count, True


def fill_right(map: Map, x: int, y: int):
    count = 0
    for x in range(x, len(map)):
        if map[y][x] == ".":
            map[y][x] = "~"
            count += 1
            if map[y + 1][x] == ".":
                c, forever = fill_down(map, x, y + 1)
                count += c
                if forever:
                    return count, True
        else:
            return count, False
    return count, True


def fill_down(map: Map, x: int, y0: int) -> (int, bool):
    count = 0
    max_y = len(map)
    for y in range(y0, len(map)):
        if map[y][x] == ".":
            map[y][x] = "|"
            count += 1
            max_y = y
        else:
            break
    else:
        return count, True
    # fill
    print_map(map)
    for y in range(max_y, y0, -1):
        forever = False
        if map[y][x - 1] == ".":
            c, f = fill_left(map, x - 1, y)
            forever |= f
            count += c
        if map[y][x + 1] == ".":
            c, f = fill_right(map, x + 1, y)
            forever |= f
            count += c
        if forever:
            return count, True
    return count, False


c, f = fill_down(map, spring_x, spring_y)
print(c, f)
print_map(map)
