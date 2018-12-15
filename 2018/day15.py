#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum
from typing import List, Tuple, Dict, Optional
from copy import deepcopy

import itertools

import sys
from dataclasses import dataclass, field

cave = """
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
""".splitlines(keepends=False)

#
with open("in15.txt") as f:
    cave = f.read().splitlines(keepends=False)

BOLD = "\033[1m"
DIM = "\033[90m"
BLUE = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
MAGENTA = "\033[35m"
RED = "\033[91m"
NORMAL = "\033[0m"


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
    power: int = field(hash=False, default=3)
    hit_points: int = field(hash=False, default=200)

    def __str__(self):
        return f"{self.nation.value}[{self.id_}] at ({self.x},{self.y}): {self.hit_points}"


Cave = List[List[str]]
Units = List[Unit]
Path = List[Tuple[int, int]]


def sort_units(units: List[Unit], use_hp=False):
    return units.sort(key=lambda u: (u.hit_points if use_hp else 0, u.x, u.y))


def clear():
    print("\033c")


def print_map(cave: Cave, units: Units, curent: Unit = None, enemy: Unit = None, path: Path = []):
    for x, row in enumerate(cave):
        for y, point in enumerate(row):
            for u in units:
                if u.x == x and u.y == y:
                    if u == curent:
                        print(BOLD + u.nation.value + NORMAL, end="")
                    elif u == enemy:
                        print(RED + BOLD + u.nation.value + NORMAL, end="")
                    elif 50 <= u.hit_points < 100:
                        print(GREEN + u.nation.value + NORMAL, end="")
                    elif 10 <= u.hit_points < 50:
                        print(YELLOW + u.nation.value + NORMAL, end="")
                    elif 0 < u.hit_points < 10:
                        print(MAGENTA + u.nation.value + NORMAL, end="")
                    elif u.hit_points <= 0:
                        print(MAGENTA + "X" + NORMAL, end="")
                    else:
                        print(u.nation.value, end="")
                    break
            else:
                if isinstance(point, str):
                    if (x, y) in path:
                        print(GREEN + "+" + NORMAL, end="")
                    else:
                        print(DIM + point + NORMAL, end="")
                else:
                    print(BLUE + "?" + NORMAL, end="")
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


def use_point(map: Cave, points: List[Tuple[int, int, Path]], enemy: Nation, units: Units,
              targets: Dict[Units, Path],
              x: int, y: int,
              path: Path) -> bool:
    for u in units:
        if u.x == x and u.y == y:
            if u.nation == enemy and not u in targets:
                targets[u] = path
            return True

    if map[x][y] == ".":
        path = deepcopy(path)
        path.append((x, y))
        points.append((x, y, path))
        map[x][y] = path
        return False
    return True


def find_targets(unit: Unit, cave: Cave, units: Units) -> (Optional[Unit], Path):
    enemy = unit.nation.enemy()
    points: List[Tuple[int, int, Path]] = [(unit.x, unit.y, [(unit.x, unit.y)])]
    map = deepcopy(cave)
    map[unit.x][unit.y] = 0
    targets: Dict[Units, Path] = {}
    # calculate distances
    while points:
        points.sort(key=lambda p: p[2])
        new_points = []
        for x, y, path in points:
            res = False
            res |= use_point(map, new_points, enemy, units, targets, x - 1, y, path)
            res |= use_point(map, new_points, enemy, units, targets, x, y - 1, path)
            res |= use_point(map, new_points, enemy, units, targets, x, y + 1, path)
            res |= use_point(map, new_points, enemy, units, targets, x + 1, y, path)
        points = new_points

    # print_map(map, units, u)
    # print()
    # select target
    selected_targets: Units = []
    distance = 0
    for k, v in targets.items():
        if not selected_targets or distance == len(v):
            selected_targets.append(k)
            distance = len(v)
        elif len(v) < distance:
            selected_targets = [k]
            distance = len(v)

    sort_units(selected_targets)
    if not selected_targets:
        return None, []
    return selected_targets[0], targets[selected_targets[0]][1:]


def find_attacked(unit: Unit, units: Units) -> Unit:
    res = []
    for u in units:
        if u.nation == unit.nation.enemy() and u.hit_points > 0 and (
                (u.x == unit.x and abs(u.y - unit.y)) == 1 or (u.y == unit.y and abs(u.x - unit.x) == 1)
        ):
            res.append(u)
    if res:
        sort_units(res, use_hp=True)
        return res[0]
    return None


def check_enemies(unit: Unit, units: Units) -> bool:
    for u in units:
        if u.nation == unit.nation.enemy() and u.hit_points > 0:
            return True
    return False


def print_hp(units: Units):
    oldx = units[0].x
    for u in units:
        if u.x != oldx:
            print()
            oldx = u.x
        print(f"{str(u):20}", end="\t")
    print()


for n in itertools.count():
    print()
    print(n)
    print_map(cave, units)
    units = [u for u in units if u.hit_points > 0]
    sort_units(units)
    print_hp(units)
    for u in units:
        if u.hit_points <= 0:
            continue
        if not check_enemies(u, units):
            print("Finish")
            break
        # print(u)
        # search path to nearest target
        target, path = find_targets(u, cave, units)

        # move
        if path:
            u.x, u.y = path[0]
        # print(u)
        # print_map(cave, units, u, target, path)
        # print()
        # print(f"move {len(path)}:", target)

        # select to attack
        target = find_attacked(u, units)
        # print(f"attack:", target)
        if target:
            target.hit_points -= u.power
            # print(f"after attack:", target)
        # print()
    else:
        continue
    break

print()
print_map(cave, units)
print_hp(units)
total_hp = sum(u.hit_points for u in units if u.hit_points > 0)
print(n, total_hp, n * total_hp)
