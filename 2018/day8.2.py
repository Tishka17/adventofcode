#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List
from collections import deque

with open("in8.txt") as f:
    data = [int(x) for x in f.read().split(" ")]


def walk(data: List[int], start: int, level=0) -> (int, int):
    children, meta = data[start: start + 2]
    if children:
        print("|" * level + "\\")
    start += 2
    sum = 0
    children_data: List[int] = []
    for _ in range(children):
        child_sum, child_end, = walk(data, start, level + 1)
        children_data.append(child_sum)
        start = child_end

    print("|" * level + "-", end="     ------> ")
    for _ in range(meta):
        m = data[start]
        print(f"{m}.", end="")
        if children:
            if m-1 < children:
                sum += children_data[m-1]
        else:
            sum += m
        start += 1
    print()
    print("|" * level + "-", sum, start)
    return sum, start


print(walk(data, 0))
