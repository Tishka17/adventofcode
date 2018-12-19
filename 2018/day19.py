from dataclasses import dataclass, field
from typing import List
import time


@dataclass
class Device:
    registers: List[int] = field(default_factory=lambda: [0] * 6)
    ip: int = 0
    program: List = field(default_factory=list)
    instructions = {}

    @classmethod
    def instruction(self, proc):
        self.instructions[proc.__name__] = proc
        return proc

    def exec(self, name, a, b, c):
        # print(self.registers[self.ip], name, a,b,c, self.registers, end=' -> ')
        self.instructions[name](self, a, b, c)
        # print(self.registers[self.ip], name, a,b,c, self.registers[:-1])

    def run(self):
        ip = self.registers[self.ip]
        n = 0
        while ip >= 0 and ip < len(self.program):
            self.registers[self.ip] = ip
            self.exec(*self.program[ip])
            ip = self.registers[self.ip] + 1
            n += 1
            if n % 10000 == 0:
                print(n, self.registers)
            # time.sleep(0.1)


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
    # if a==5: return
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


cmds = []
with open("/sdcard/src/in19.py") as f:
    for s in f:
        if not s.startswith("#"):
            s = s.split(' ')
            cmds.append(s[:1] + [int(x) for x in s[1:]])

d = Device(program=cmds, ip=1)
d.run()
print(d.registers)