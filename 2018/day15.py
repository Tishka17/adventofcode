#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum
from typing import List, Tuple, Dict, Optional
from copy import deepcopy

import itertools

import sys
from dataclasses import dataclass, field

cave = """
################################
###################..###########
#################.....##########
################.......#########
################......#####...##
#################.....G###.....#
###########.#####....#####..####
###########..####.#.###....#####
##########.GG#.....##......#####
###########.........#...G..#####
###########....GG..........#####
##########G.GG....G....GG..#####
#########.G...#####........#####
#######.G...G#######.E...E..####
###########.#########.......####
##########..#########......#####
##...#####..#########.G....#####
####..#..#..#########.#.....####
###.G.#.....#########..#..#.E###
#####........#######.......E.###
#####.........#####.......######
######............E....E..######
#G.###..G.................######
#..####...............#....#####
#....E#...G.......######...#####
#.............E..#######.#######
###.........E#....##############
######.E.....#..################
#######..........###############
#######......#.#################
#####...#...####################
################################
""".splitlines(keepends=False)

#
# with open("in15.txt") as f:
#     cave = f.read().splitlines(keepends=False)

UNDERLINE = "\033[4m"
BOLD = "\033[1m"
DIM = "\033[90m"
BLUE = "\033[36m"
BLUE2 = "\033[96m"
BLUE3 = "\033[94m"
BLUE4 = "\033[34m"
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


def print_map(cave: Cave, units: Units, curent: Unit = None, target: Tuple[int, int] = None, path: Path = []):
    for x, row in enumerate(cave):
        row_units = []
        for y, point in enumerate(row):
            for u in units:
                if u.x == x and u.y == y:
                    row_units.append(u)
                    if u == curent:
                        print(BOLD + u.nation.value + NORMAL, end="")
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
                    if (x, y) == target:
                        print(RED + BOLD + "+" + NORMAL, end="")
                    elif (x, y) in path:
                        print(GREEN + "+" + NORMAL, end="")
                    else:
                        print(DIM + point + NORMAL, end="")
                else:
                    if len(point) > 30:
                        print(BLUE4 + str(len(point) % 10) + NORMAL, end="")
                    elif len(point) > 20:
                        print(BLUE3 + str(len(point) % 10) + NORMAL, end="")
                    elif len(point) > 10:
                        print(BLUE2 + str(len(point) % 10) + NORMAL, end="")
                    else:
                        print(BLUE + str(len(point) % 10) + NORMAL, end="")
        for u in row_units:
            print(f"{str(u):20}", end="\t")
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

g1 = units[6]
print_map(cave, [])
print()
print_map(cave, units)
print()


def neighbours(x, y):
    return [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y), ]


def use_point(map: Cave, points: List[Tuple[int, int, Path]], enemy: Nation, units: Units,
              targets: Dict[Tuple[int, int], Path],
              x: int, y: int,
              path: Path) -> bool:
    neigh = neighbours(x, y)
    for u in units:
        if u.x == x and u.y == y and u.hit_points > 0:
            return True

    if map[x][y] == ".":
        path = deepcopy(path)
        path.append((x, y))
        points.append((x, y, path))
        map[x][y] = path

        for u in units:
            if u.hit_points > 0 and u.nation == enemy and (u.x, u.y) in neigh:
                targets[(x, y)] = path
        return False
    return True


def find_targets(unit: Unit, cave: Cave, units: Units) -> (Optional[Unit], Path):
    enemy = unit.nation.enemy()
    points: List[Tuple[int, int, Path]] = [(unit.x, unit.y, [(unit.x, unit.y)])]
    map = deepcopy(cave)
    map[unit.x][unit.y] = 0
    targets: Dict[Tuple[int, int], Path] = {}
    # calculate distances
    while points:
        points.sort(key=lambda p: p[2])
        new_points = []
        for x, y, path in points:
            res = False
            for x1, y1 in neighbours(x, y):
                res |= use_point(map, new_points, enemy, units, targets, x1, y1, path)
        points = new_points

    # print_map(map, units, u)
    # print()
    # select target
    selected_targets: List[Tuple[int, int]] = []
    distance = 0
    for k, v in targets.items():
        if not selected_targets or distance == len(v):
            selected_targets.append(k)
            distance = len(v)
        elif len(v) < distance:
            selected_targets = [k]
            distance = len(v)

    selected_targets.sort()
    if not selected_targets:
        return None, []
    return selected_targets[0], targets[selected_targets[0]][1:]


def find_attacked(unit: Unit, units: Units) -> Optional[Unit]:
    res = []
    neigh = neighbours(unit.x, unit.y)
    for u in units:
        if u.nation == unit.nation.enemy() and u.hit_points > 0 and (u.x, u.y) in neigh:
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
    # print_hp(units)
    for u in units:
        if u.hit_points <= 0:
            continue
        if not check_enemies(u, units):
            break
        # print(u)

        # try select to attack
        target = find_attacked(u, units)
        if not target:
            # search path to nearest target
            target, path = find_targets(u, cave, units)

            # move
            # print(u)
            # print_map(cave, units, u, target, path)
            if path:
                u.x, u.y = path[0]
            # print()
            # print(f"move {len(path)}:", target)

            # select to attack
            target = find_attacked(u, units)
        # print(f"attack:", target)
        if target:
            target.hit_points -= u.power
            if target.hit_points <= 0:
                print("Died: ", target, "at ", n)
            # print(f"after attack:", target)
        # print()
        # input("Next?")
    else:
        # input("Continue?")
        continue
    break

print()
print("Finish: ", u)
print_map(cave, units)
print_hp(units)
total_hp = sum(u.hit_points for u in units if u.hit_points > 0)
print(n, total_hp, n * total_hp)
