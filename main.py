#!/usr/bin/env python3
from engine import Engine, Arena
import os

p1 = Engine()
p2 = Engine()

p1_env = os.environ.copy()
p1_env["CUDA_VISIBLE_DEVICES"] = "0"
p1.env = p1_env
p1.cwd = "/home/jimmy/Documents/phoenixgo"
p1.args = ["./scripts/start.sh", "etc/mcts_1gpu_notensorrt.conf"]

p2_env = os.environ.copy()
p2_env["CUDA_VISIBLE_DEVICES"] = "1"
p2.env = p2_env
p1.cwd = "/home/jimmy/Documents/phoenixgo-ewin"
p2.args = ["./scripts/start.sh", "etc/mcts_1gpu_notensorrt.conf"]

arena = Arena(p1, p2)
arena.duel(50)