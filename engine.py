#!/usr/bin/env python3
from subprocess import Popen, PIPE
from datetime import datetime

log_dir = "log/"

engine_count = 0
now = datetime.now()

class Engine(object):
  def __init__(self):
    self.env = None
    self.cwd = None
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
    self.process = Popen(self.args, stdin=PIPE, stdout=PIPE, stderr=self.log, cwd=self.cwd, env=self.env)

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
    data = self.send("genmove {}\n".format(color))
    assert data[0] == "="
    return data[1:].strip()

  def play(self, color, vertex):
    return self.send("play {} {}\n".format(color, vertex))

  def score(self):
    return self.send("final_score\n")

  def list_commands(self):
    return self.send("list_commands\n")
  
  def loadsgf(self, filename):
    return self.send("loadsgf {}\n".format(filename))


class Arena(object):
  def __init__(self, player1, player2, sgffilename=None):
    self.player1 = player1
    self.player2 = player2
    self.filename = sgffilename
  
  def duel(self, num):
    p1_count = 0
    p2_count = 0
    for i in range(num):
      if i % 2 == 0:
        result = self.one_game(self.player1, self.player2)
        if (result > 0):
          p1_count += 1
        elif (result < 0):
          p2_count += 1
      else:
        result = self.one_game(self.player2, self.player1)
        if (result > 0):
          p2_count += 1
        elif (result < 0):
          p1_count += 1
      print(i, p1_count, p2_count)

  def one_game(self, black, white):
    RESIGN = "resign"
    PASS = "pass"
    black.launch()
    white.launch()
    if self.filename:
      black.loadsgf(self.filename)
      white.loadsgf(self.filename)

    pass_count = 0
    result = 0
    while True:
      move = black.genmove("B")
      black.showboard()
      if move == RESIGN:
        result = -1
        break
      if move == PASS:
        pass_count += 1
      else:
        white.play("B", move)
        white.showboard()
        pass_count = 0
      if pass_count >= 2:
        break
      move = white.genmove("W")
      white.showboard()
      if move == RESIGN:
        result = 1
        break
      if move == PASS:
        pass_count += 1
      else:
        black.play("W", move)
        black.showboard()
        pass_count = 0
      if pass_count >= 2:
        break

    black.send("printsgf\n")
    white.send("printsgf\n")
    score = black.score()
    black.close()
    white.close()

    if pass_count >= 2:
      assert score[0] == "="
      winner = score[1:].strip()[0]
      if (winner == "B"):
        return 1
      if (winner == "W"):
        return -1
      return 0
    else:
      return result
