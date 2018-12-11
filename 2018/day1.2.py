#!/usr/bin/env python
# -*- coding: utf-8 -*-
f = open("in1.txt")
sums = {0}
s = 0

items = list(map(int, f))
while True:
    for i in items:
        s += int(i)
        if s in sums:
            print(s)
            raise StopIteration
        sums.add(s)
