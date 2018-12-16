#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
            if len(list(x)) >= 3:
                count += 1
        elif s:
            cmd, a, b, c = list(map(int, s.split(" ")))

print(count)
