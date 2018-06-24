#!/usr/bin/env python3
from engine import Engine

p1 = Engine()
p2 = Engine()
p2.args = ["./play.sh", "1"]

print(p1.no)
print(p2.no)

p1.launch()
p2.launch()

print(p1.genmove("B"))
print(p2.name())
p1.showboard()
p2.showboard()
p1.close()
p2.close()