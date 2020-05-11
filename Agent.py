from Board import Board
from Policy import Policy

class Agent():
  def __init__(self, piece):
    self._piece = piece

  def get_piece(self):
    return self._piece  

  def count_piece(self, b):
    cnt = 0
    for i in range(36):
      if b[i] == self.get_piece():
        cnt += 1
    return cnt

  def take_action(self, b):
    return NotImplemented

  def name(self):
    return "agent"

class Player(Agent):
  def __init__(self, piece):
    super().__init__(piece)

  def take_action(self, before):
    mv_prev, mv_next = Policy.NN(before, self.get_piece())
    if not mv_prev == -1:
      before.move(mv_prev, mv_next, self.get_piece())
    return mv_prev, mv_next

  def name(self):
    return "player"

class Envir(Agent):
  def __init__(self, piece):
    super().__init__(piece)

  def take_action(self, before):
    mv_prev, mv_next = Policy.Greedy(before, self.get_piece())
    if not mv_prev == -1:
      before.move(mv_prev, mv_next, self.get_piece())
    return mv_prev, mv_next

  def name(self):
    return "envir"