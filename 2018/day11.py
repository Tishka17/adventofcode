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


def square_sum(x, y):
    return sum(grid[x][y:y + 3]) + sum(grid[x + 1][y:y + 3]) + sum(grid[x + 2][y:y + 3])


sm = square_sum(0, 0)
xm, ym = 0, 0

for x in range(size - 3):
    for y in range(size - 3):
        s = square_sum(x, y)
        if s > sm:
            xm, ym = x, y
            sm = s

print(f"Sum={sm}, coords={xm + 1},{ym + 1}")
