import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict

from dataclass_factory import ParserFactory


class Action(Enum):
    wake = "wakes up"
    asleep = "falls asleep"
    start = "begins shift"


@dataclass
class Step:
    date: datetime
    guard: Optional[int]
    action: Action


p_factory = ParserFactory(type_factories={datetime: lambda d: datetime.strptime(d, "%Y-%m-%d %H:%M")})
parser = p_factory.get_parser(Step)

regex = re.compile(r'^\[(?P<date>[^]]+)] (?:(?:Guard #)(?P<guard>\d+) )?(?P<action>.*)$')

steps: List[Step] = []
with open("input.txt") as f:
    for i in f:
        i = i.strip()
        if i:
            g = parser(regex.match(i).groupdict())
            steps.append(g)
steps.sort(key=lambda s: s.date)

guards_sleep: Dict[int, List[int]] = defaultdict(lambda: [0] * 60)


def upd_minutes(start, stop, lst):
    for i in range(start, stop):
        lst[i] += 1


guard = None
last = None
days = 0
for s in steps:
    if s.guard:
        days += 1
        guard = s.guard
        last = None
    else:
        if s.action == Action.asleep:
            last = s.date
        if s.action == Action.wake:
            upd_minutes(last.minute, s.date.minute, guards_sleep[guard])
            last = None

m = max(list(guards_sleep.items()), key=lambda k: sum(k[1]))[0]
best = max(enumerate(guards_sleep[m]), key=lambda x: x[1])[0]

for k, v in guards_sleep.items():
    print("%4s: " % k, ".".join(map(lambda x: "%2s" % x, v)), "", sum(v))

print()
print("%4s: " % m, ".".join(map(lambda x: "%2s" % x, guards_sleep[m])))
print("Days:", days)
print("Guard:", m)
print("Best minute:", best, " with value", guards_sleep[m][best])
print("Result: ", best * m)

print()
print("Part 2:")
m = max(list(guards_sleep.items()), key=lambda k: max(k[1]))[0]
best = max(enumerate(guards_sleep[m]), key=lambda x: x[1])[0]
print("Guard:", m)
print("Best minute:", best, " with value", guards_sleep[m][best])
print("Result: ", best * m)
