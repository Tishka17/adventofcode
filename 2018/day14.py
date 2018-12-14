#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

import itertools
from dataclasses import dataclass

opens = "([{"
closes = ")]}"

inp = list("37")  # list("323081")
steps = 323081  # 323081


@dataclass
class Elf:
    pos: int
    current: int
    open: str
    close: str


elves: List[Elf] = []
elves_count = 2

for i in range(elves_count):
    elves.append(
        Elf(pos=i, current=int(inp[i]), open=opens[i], close=closes[i])
    )


def move(elf: Elf, inp):
    # print("Move dbg:", len(inp), (elf.pos + elf.current + 1) % (len(inp)))
    # print("Move: ", elf, end=" -> ")
    elf.pos = (elf.pos + elf.current + 1) % (len(inp))
    elf.current = int(inp[elf.pos])
    # print(elf)


def print_cur(step, inp, elves):
    print(f"Step {step}({len(inp)}):\t", end="")
    for i, s in enumerate(inp):
        op = ""
        cl = ""
        for e in elves:
            if e.pos == i:
                op = op + e.open
                cl = e.close + cl
        if not op:
            op = cl = " "
        print(op + s + cl, end=" ")
    print()


for step in itertools.count():
    # print_cur(step, inp, elves)

    if len(inp) >= steps + 10:
        print("".join(inp[steps:steps + 10]))
        break

    inp.extend(str(sum(e.current for e in elves)))
    for e in elves:
        move(e, inp)
