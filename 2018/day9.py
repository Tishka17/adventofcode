#!/usr/bin/env python
# -*- coding: utf-8 -*-

players = 465
last = 71940

circle = [0]
current = 0
scores = [0] * players
current_player = 0

for i in range(1, last):
    current_player = (current_player + 1) % players
    if i and not i % 23:
        current = current - 7
        if current < 0:
            current += len(circle)
        marble = circle.pop(current)
        scores[current_player] += i + marble
        # print("Add: ", i , marble)
    else:
        current = (current + 1) % len(circle) + 1
        circle.insert(current, i)
    if not i % (last // 100):
        print(i, i // (last // 100), last)

print("Max:", max(scores))
