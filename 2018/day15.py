#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum
from typing import List, Tuple, Dict, Optional
from copy import deepcopy
from dataclasses import dataclass, field

cave = """
#######
#.G.E.#
#E.G.E#
#.G.E.#
#######
""".splitlines(keepends=False)


# with open("in15.txt") as f:
#     cave = f.read().splitlines(keepends=False)


class Nation(Enum):
    Goblin = "G"
    Elf = "E"

    def enemy(self):
        if self is self.Goblin:
            return self.Elf
        return self.Goblin


@dataclass(unsafe_hash=True)
class Unit:
    id_: int = field(hash=True)
    nation: Nation = field(hash=False)
    x: int = field(hash=False)
    y: int = field(hash=False)


Cave = List[List[str]]
Units = List[Unit]


def sort_units(units: List[Unit]):
    return units.sort(key=lambda u: (u.x, u.y))


def print_map(cave: Cave, units: Units):
    for x, row in enumerate(cave):
        for y, point in enumerate(row):
            for u in units:
                if u.x == x and u.y == y:
                    print(u.nation.value, end="")
                    break
            else:
                print(point, end="")
        print()


### clean map
units: Units = []
cave: Cave = list(list(x) for x in cave if x)
for x, row in enumerate(cave):
    for y, point in enumerate(row):
        try:
            nation = Nation(point)
            row[y] = "."
            units.append(Unit(len(units), nation, x, y))
        except:
            pass

print_map(cave, [])
print()
print_map(cave, units)
print()


def use_point(map: Cave, points: List[Tuple[int, int, int]], enemy: Nation, units: Units, targets: Dict[Units, int],
              x: int, y: int,
              distance: int) -> bool:
    for u in units:
        if u.x == x and u.y == y:
            if u.nation == enemy and not u in targets:
                targets[u] = distance
            return True

    if map[x][y] == ".":
        points.append((x, y, distance))
        map[x][y] = distance
        return False
    return True


def find_targets(unit: Unit, cave: Cave, units: Units) -> (Optional[Unit], int):
    enemy = unit.nation.enemy()
    points: List[Tuple[int, int, int]] = [(unit.x, unit.y, 0)]
    map = deepcopy(cave)
    map[unit.x][unit.y] = 0
    targets: Dict[Units, int] = {}
    # calculate distances
    while points:
        new_points = []
        for p in points:
            res = use_point(map, new_points, enemy, units, targets, p[0] + 1, p[1], p[2] + 1)
            res |= use_point(map, new_points, enemy, units, targets, p[0] - 1, p[1], p[2] + 1)
            res |= use_point(map, new_points, enemy, units, targets, p[0], p[1] + 1, p[2] + 1)
            res |= use_point(map, new_points, enemy, units, targets, p[0], p[1] - 1, p[2] + 1)
        points = new_points

    print_map(map, units)
    # select target
    selected_targets: Units = []
    distance = 0
    for k, v in targets.items():
        if not selected_targets or distance == v:
            selected_targets.append(k)
            distance = v
        elif v < distance:
            selected_targets = [k]
            distance = v

    sort_units(selected_targets)
    if not selected_targets:
        return None, 0
    return selected_targets[0], distance


sort_units(units)
for u in units:
    print(u)
    target, distance = find_targets(u, cave, units)
    print(f"{distance}:", target)
    print()
