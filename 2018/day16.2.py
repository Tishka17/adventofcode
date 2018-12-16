#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
from typing import List, Callable, Dict

from dataclasses import dataclass, field


@dataclass
class Device:
    registers: List[int] = field(default_factory=lambda: [0] * 4)
    instructions = {}

    @classmethod
    def instruction(self, proc):
        self.instructions[proc.__name__] = proc
        return proc

    def exec(self, name, a, b, c):
        self.instructions[name](self, a, b, c)


# Addition
@Device.instruction
def addr(self, a, b, c):
    self.registers[c] = self.registers[a] + self.registers[b]


@Device.instruction
def addi(self, a, b, c):
    self.registers[c] = self.registers[a] + b


# Multiplication
@Device.instruction
def mulr(self, a, b, c):
    self.registers[c] = self.registers[a] * self.registers[b]


@Device.instruction
def muli(self, a, b, c):
    self.registers[c] = self.registers[a] * b


# Bitwise AND
@Device.instruction
def banr(self, a, b, c):
    self.registers[c] = self.registers[a] & self.registers[b]


@Device.instruction
def bani(self, a, b, c):
    self.registers[c] = self.registers[a] & b


# Bitwise OR:
@Device.instruction
def borr(self, a, b, c):
    self.registers[c] = self.registers[a] | self.registers[b]


@Device.instruction
def bori(self, a, b, c):
    self.registers[c] = self.registers[a] | b


# Assignment
@Device.instruction
def setr(self, a, b, c):
    self.registers[c] = self.registers[a]


@Device.instruction
def seti(self, a, b, c):
    self.registers[c] = a


# Greater-than testing
@Device.instruction
def gtir(self, a, b, c):
    self.registers[c] = 1 if a > self.registers[b] else 0


@Device.instruction
def gtri(self, a, b, c):
    self.registers[c] = 1 if self.registers[a] > b else 0


@Device.instruction
def gtrr(self, a, b, c):
    self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0


# Equality testing
@Device.instruction
def eqir(self, a, b, c):
    self.registers[c] = 1 if a == self.registers[b] else 0


@Device.instruction
def eqri(self, a, b, c):
    self.registers[c] = 1 if self.registers[a] == b else 0


@Device.instruction
def eqrr(self, a, b, c):
    self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0


def check_opcodes(number, a, b, c, input, output):
    for name in Device.instructions:
        device = Device(registers=[i for i in input])
        device.exec(name, a, b, c)
        if device.registers == output:
            yield name


count = 0

possible_instructions = defaultdict(lambda: {x for x in Device.instructions})

with open("in16.txt") as f:
    cmd, a, b, c = 0, 0, 0, 0
    before = []
    after = []

    for s in f:
        s = s.strip()
        if s.startswith("Before: "):
            before = eval(s[8:])
        elif s.startswith("After: "):
            after = eval(s[7:])
            x = check_opcodes(cmd, a, b, c, before, after)
            possible_instructions[cmd] &= set(x)
        elif s:
            cmd, a, b, c = list(map(int, s.split(" ")))


def print_possible(possible):
    for i in sorted(possible):
        print(f"{i:2}: ", end="")
        for j in Device.instructions:
            if j in possible[i]:
                print(j, end=" ")
            else:
                print("     ", end="")
        print()


print_possible(possible_instructions)
print()

instructions = {}
while len(instructions) < len(Device.instructions):
    for i, vi in possible_instructions.items():
        if len(vi) == 1:
            instructions[i] = list(vi)[0]
            print(i, instructions[i])
            for j, vj in possible_instructions.items():
                if i != j:
                    vj -= vi
            del possible_instructions[i]
            break

    for i in Device.instructions:
        numbers = []
        for j, v in possible_instructions.items():
            if i in v:
                numbers.append(j)
        if len(numbers) == 1:
            print(numbers[0], i, )
            instructions[numbers[0]] = i
            x = possible_instructions[numbers[0]]
            del possible_instructions[numbers[0]]

print(instructions)

device = Device()
with open("in16-2.txt") as f:
    for s in f:
        s = s.strip()
        if s:
            cmd, a, b, c = list(map(int, s.split(" ")))
            device.exec(instructions[cmd], a, b, c)

print(device.registers)
