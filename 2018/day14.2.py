# -*- coding: utf-8 -*-
from typing import List

import itertools
from dataclasses import dataclass

opens = "([{"
closes = ")]}"

inp = list("37")  # list("323081")
expected = "323081"


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

def cmp(expected, inp, offset):
    start=len(inp)-offset -len(expected)
    start=max(0, start)
    for i in range(start, len(inp)-len(expected)+1):
        for j in range(len(expected)):
            if expected[j]!=inp[i+j]:
                break
        else:
                return i
    return False
    
assert cmp("12", "345123", 3)
assert not cmp("12", "34523", 0)


prev=0
cnt = 0
for step in itertools.count():
    #print_cur(step, inp, elves)
    if step%10000==0: 
        print_cur(step, inp[-20:], elves)

    i = cmp(expected, inp, prev)
    if i:
        print(step,i, len(inp)-len(expected),  "".join(inp[-len(expected)-10:]))
        break

    s =str(sum(e.current for e in elves))
    prev = len(s)
    cnt += prev
    inp.extend(s)
    for e in elves:
        move(e, inp)
