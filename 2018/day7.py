from collections import defaultdict
from dataclasses import dataclass
from typing import List


@dataclass
class Step:
    requires: List["Step"]
    required_by: List["Step"]
    name: str = None


steps = defaultdict(lambda: Step(requires=[], required_by=[]))


def sort_ready(ready: List[Step]):
    ready.sort(key=lambda x: x.name)


with open("in7.txt") as f:
    for s in f:
        name_a, name_b = s[5], s[-13]
        a, b = steps[name_a], steps[name_b]
        a.name = name_a
        b.name = name_b
        a.required_by.append(b)
        b.requires.append(a)

res = []
ready = []

for x in steps.values():
    if not x.requires:
        ready.append(x)

while steps:
    sort_ready(ready)
    r = ready[0]
    ready.remove(r)
    del steps[r.name]
    res.append(r.name)
    for x in r.required_by:
        x.requires.remove(r)
        if not x.requires:
            ready.append(x)

print("".join(res))
