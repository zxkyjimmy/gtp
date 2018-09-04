#!/usr/bin/env python3
from engine import Engine, Arena
import os

p1 = Engine()
p2 = Engine()

p1_env = os.environ.copy()
p1_env["CUDA_VISIBLE_DEVICES"] = "0"
p1.env = p1_env
p1.args = ["./leelaz", "--weights", "b0841a68b4beae9314e47757b44dbe16c5d421dfadcba9ddfe25373e8c27b262", "--gtp"]

p2_env = os.environ.copy()
p2_env["CUDA_VISIBLE_DEVICES"] = "1"
p2.env = p2_env
p2.args = ["./leelaz-ewin", "--weights", "b0841a68b4beae9314e47757b44dbe16c5d421dfadcba9ddfe25373e8c27b262", "--gtp"]

arena = Arena(p1, p2)
arena.duel(100)