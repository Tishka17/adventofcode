#!/usr/bin/env python
# -*- coding: utf-8 -*-

serial = 9005
size = 300


def get_level(x, y, serial=serial):
    x = x + 1
    y = y + 1
    rack = x + 10
    fuel = rack * y + serial
    fuel = fuel * rack
    fuel = fuel // 100 % 10
    return fuel - 5


assert get_level(121, 78, 57) == -5
assert get_level(216, 195, 39) == 0
assert get_level(100, 152, 71) == 4

grid = []

for x in range(size):
    grid.append([get_level(x, y) for y in range(size)])
    # for y in grid[x]:
    #     print("%3d" % int(y), end=" ")
    # print()


def square_sum(x, y, size):
    s = 0
    for i in range(size):
        s += sum(grid[x + i][y:y + size])
    return s


sm = square_sum(0, 0, 1)
xm, ym = 0, 0
sizem = 1

for s in range(size):
    for x in range(size - s):
        for y in range(size - s):
            ss = square_sum(x, y, s)
            if ss > sm:
                xm, ym = x, y
                sm = ss
                sizem=s

    print(f"Sum={sm}, coords={xm + 1},{ym + 1},{sizem}, try {s}")
print("Done")
