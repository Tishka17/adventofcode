#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, List

from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class Directon(Enum):
    up = "^"
    right = ">"
    left = "<"
    down = "v"

    def rotate_left(self):
        return {
            self.left: self.down,
            self.down: self.right,
            self.right: self.up,
            self.up: self.left
        }[self]

    def rotate_right(self):
        return {
            self.left: self.up,
            self.down: self.left,
            self.right: self.down,
            self.up: self.right
        }[self]

    def next(self, pos):
        if self is self.up:
            return Position(pos.x - 1, pos.y)
        elif self is self.down:
            return Position(pos.x + 1, pos.y)
        elif self is self.left:
            return Position(pos.x, pos.y - 1)
        elif self is self.right:
            return Position(pos.x, pos.y + 1)

    def track(self):
        if self in (self.left, self.right):
            return "-"
        return "|"


@dataclass(frozen=True)
class Position:
    x: int
    y: int


# crosses: Dict[Position, int] = defaultdict(lambda: 0)


@dataclass
class Cart:
    direction: Directon
    pos: Position
    start: Position
    count = 0

    def rotate(self, symbol):
        if symbol == "+":
            count = self.count  # crosses[self.pos]
            # print("cross before:", self, count)
            if count == 0:
                self.direction = self.direction.rotate_left()
            elif count == 2:
                self.direction = self.direction.rotate_right()
            # crosses[self.pos] = (count + 1) % 3
            self.count = (count + 1) % 3
            # print("cross after:", self, self.count)
        elif symbol == "/":
            if self.direction in (Directon.up, Directon.down):
                self.direction = self.direction.rotate_right()
            elif self.direction in (Directon.left, Directon.right):
                self.direction = self.direction.rotate_left()
        elif symbol == "\\":
            if self.direction in (Directon.up, Directon.down):
                self.direction = self.direction.rotate_left()
            elif self.direction in (Directon.left, Directon.right):
                self.direction = self.direction.rotate_right()


with open("in13.txt") as f:
    tracks = list(list(s) for s in f)

carts: List[Cart] = []

for x in range(len(tracks)):
    for y in range(len(tracks[x])):
        symbol = tracks[x][y]
        try:
            d = Directon(symbol)
            cart = Cart(
                direction=d,
                pos=Position(x, y),
                start=Position(x, y)
            )
            carts.append(cart)
        except Exception as e:
            pass

print(*carts, sep="\n", end="\n\n")

for time in range(1, 20000):
    # print(time)
    i = 0
    while i < len(carts):
        cart = carts[i]
        new = cart.direction.next(cart.pos)
        j = 0
        while j < len(carts):
            c = carts[j]
            if c.pos == new:
                print("crash at", time, f"{new.y},{new.x}")
                print("Crashed:", cart)
                print("Crashed:", c)
                carts.remove(cart)
                carts.remove(c)
                if j < i:
                    i -= 1
                if len(carts) == 1:
                    print("Res:", carts)
                    1 // 0
                break
            j += 1
        else:
            i += 1
        cart.pos = new
        # if not (0 <= new.x < len(tracks)) or not (0 <= new.y < len(tracks[0])):
        #     print("error:", cart)
        #     1 // 0
        symbol = tracks[new.x][new.y]
        cart.rotate(symbol)

    # print(*carts, sep="\n", end="\n\n")
