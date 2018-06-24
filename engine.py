#!/usr/bin/env python3
from subprocess import Popen, PIPE
from datetime import datetime

log_dir = "log/"

engine_count = 0
now = datetime.now()

class Engine(object):
  def __init__(self):
    self.cwd = "../leela-zero"
    self.args = ["./play.sh", "0"]
    self.log = None
    self.process = None
    global engine_count
    self.no = engine_count
    engine_count += 1

  def create_log(self):
    global now
    global log_dir
    time_mark = "{:04}{:02}{:02}-{:02}{:02}{:02}".format(
      now.year, now.month, now.day, now.hour, now.minute, now.second)
    log_name = log_dir + time_mark + "-{}.log".format(self.no)
    return open(log_name, "w")

  def launch(self):
    if self.log == None:
      self.log = self.create_log()
    self.process = Popen(self.args, stdin=PIPE, stdout=PIPE, stderr=self.log, cwd=self.cwd)

  def send(self, data):
    self.process.stdin.write(data.encode())
    self.process.stdin.flush()
    result = ""
    while True:
      res = self.process.stdout.readline().decode()
      if not res.strip():
        break
      result += res
    return result

  def quit(self):
    return self.send("quit\n")
  
  def close(self):
    self.quit()
    self.log.close()
    self.log = None

  def name(self):
    return self.send("name\n")

  def version(self):
    return self.send("version\n")

  def showboard(self):
    return self.send("showboard\n")

  def clearboard(self):
    return self.send("clear_board\n")

  def boardsize(self, size):
    return self.send("boardsize {}\n".format(size))

  def komi(self, komi):
    return self.send("komi {}\n".format(komi))

  def genmove(self, color):
    return self.send("genmove {}\n".format(color))

  def play(self, color, vertex):
    return self.send("play {} {}\n".format(color, vertex))

  def score(self):
    return self.send("final_score\n")

  def list_commands(self):
    return self.send("list_commands\n")

