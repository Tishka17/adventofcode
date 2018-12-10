from collections import defaultdict
from dataclasses import dataclass, field
from typing import List


@dataclass
class Step:
    requires: List["Step"]
    required_by: List["Step"]
    name: str = None
    time: int = field(init=False)

    def set_name(self, name):
        self.name = name
        self.time = ord(self.name[0]) - ord("A") + 61


steps = defaultdict(lambda: Step(requires=[], required_by=[]))


def sort_ready(ready: List[Step]):
    ready.sort(key=lambda x: x.name)


def sort_working(working: List[Step]):
    working.sort(key=lambda x: (x.time, x.name))


with open("in7.txt") as f:
    for s in f:
        s = s.strip()
        if s:
            name_a, name_b = s[5], s[-12]
            a, b = steps[name_a], steps[name_b]
            a.set_name(name_a)
            b.set_name(name_b)
            a.required_by.append(b)
            b.requires.append(a)
            print(name_a, name_b)

res = []
ready = []
working = []

for x in steps.values():
    if not x.requires:
        ready.append(x)
sort_ready(ready)
time = 0

while steps or working:
    if len(working) < 5 and ready:
        cnt = 5 - len(working)
        working.extend(ready[:cnt])
        ready = ready[cnt:]
        sort_working(working)
    print(f"time = {time}, Working ({len(working)}): ", *(f"{w.name}: {w.time}" for w in working))
    r = working[0]
    time += r.time
    print(r.name, r.time)
    working.remove(r)
    for w in working:
        w.time -= r.time

    del steps[r.name]
    res.append(r.name)
    for x in r.required_by:
        x.requires.remove(r)
        if not x.requires:
            ready.append(x)
            print("append ready: ", x.name)
    sort_ready(ready)

print("".join(res))
print(f"Total: {time}")
