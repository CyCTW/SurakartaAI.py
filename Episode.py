import time
import copy
from Board import Board
from Agent import Agent

class Episode():
  def __init__(self):
    self.ep_open = 0.0
    self.ep_close = 0.0
    self.ep_time = 0.0
    self.ep_moves = []
    self.ep_boards = []

    self.train_result = []
    self.train_boards = []
    self.who_win = ""
    self.win_piece = 0
    
    self.player_res = 0
    self.envir_res = 0


  def take_turns(self, play, env):
    self.ep_time = time.time()

    if env.get_piece() == 1:
      return env if ((self.step()+1)%2) else play
    else: 
      return play if ((self.step()+1)%2) else env

  def get_winner(self, play, env):
    if env.get_piece() == 1:
      return play if ((self.step()+1)%2) else env
    else: 
      return env if ((self.step()+1)%2) else play

  def open_episode(self):
    self.ep_open = time.time()
    return 

  def close_episode(self, winner, b):
    self.ep_close = time.time()
    self.who_win = winner.name()
    self.win_piece = winner.count_piece(b)

    if winner.name() == 'player':
      self.player_res = 1
      self.envir_res = -1
    elif winner.name() == 'envir':
      self.player_res = -1
      self.envir_res = 1
    # for i in self.train_boards:
    #   print(i)
    
  def train_close_episode(self, winner, b):
    if winner.name() == 'player':
      self.player_res = 1
      self.envir_res = -1
    elif winner.name() == 'envir':
      self.player_res = -1
      self.envir_res = 1

    win = self.player_res
    board_len = len(self.train_boards)

    for _i in range(board_len):
      self.train_result.append(win)
      win = -win



  def time(self, who = 'n'):
    time_cost = 0.0
    total_len = len(self.ep_moves)
    if who == 'p':
      for i in range(0, total_len, 2):
        time_cost += self.ep_moves[i][2]
        # print('p', time_cost)
    elif who == 'e':
      for i in range(1, total_len, 2):
        time_cost += self.ep_moves[i][2]
        # print('e', time_cost)
    else:
      time_cost = self.ep_close - self.ep_open
    
    time_cost *= 1000
    return time_cost

  def step(self, who = 'n'):
    total_len = len(self.ep_moves)
    if who == 'p':
      return (total_len/2) + (1 if total_len%2 else 0)
    elif who == 'e':
      return (total_len/2)
    else :
      return total_len

  def record(self, mv_prev, mv_next, prev_b, piece):
    self.ep_moves.append((mv_prev, mv_next, time.time() - self.ep_time))  
    # print(time.time() - self.ep_time)  
    self.ep_boards.append(prev_b)
  
  def record_train_boards(self, b, piece):
    b_ = copy.deepcopy(b)
    if piece == 1:
      b_.flip_color()
    self.train_boards.append(b_)
  
  def clear(self):
    del self.train_boards[:]
    del self.train_result[:]

