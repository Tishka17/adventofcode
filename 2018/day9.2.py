#!/usr/bin/env python
# -*- coding: utf-8 -*-

players = 465
last = 7194000

scores = [0] * players
current_player = 0


class Item:
    value: int
    next: "Item"
    prev: "Item"

    def __init__(self, value, prev, next):
        self.value = value
        self.next = next
        if next:
            next.prev = self
        self.prev = prev
        if prev:
            prev.next = self

    def remove(self) -> "Item":
        self.next.prev = self.prev
        self.prev.next = self.next
        return self.next


current: Item = Item(0, None, None)
current.prev = current
current.next = current

for i in range(1, last):
    ##
    # c = current
    # print(f"({c.value})", end=" ")
    # c = c.next
    # while c.value != current.value:
    #     print(f" {c.value} ", end=" ")
    #     c = c.next
    # print()
    ##
    current_player = (current_player + 1) % players
    if i and not i % 23:
        for _ in range(7):
            current = current.prev
        scores[current_player] += i + current.value
        # print("Add: ", i, current.value)
        current = current.remove()
    else:
        current = Item(i, current.next, current.next.next)
    if not i % (last // 100):
        print(i, i // (last // 100), last)

print("Max:", max(scores))
