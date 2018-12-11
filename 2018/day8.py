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
    for _ in range(children):
        child_sum, child_end, = walk(data, start, level + 1)
        sum += child_sum
        start = child_end
    for _ in range(meta):
        sum += data[start]
        start += 1
    print("|" * level+"-", sum, start)
    return sum, start


print(walk(data, 0))
