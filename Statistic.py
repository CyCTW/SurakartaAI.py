from Episode import Episode

class Statistic():
  def __init__(self, total, block):
    self.total = total
    self.block = block if block else total
    self.blk_id = 0
    self.count = 0
    self.data = []
  
  def is_finished(self):
    return self.count >= self.total

  def open_episode(self):
    self.count += 1
    self.data.append(Episode())
    self.data[-1].open_episode()
    print(self.data[-1].time())

  def close_episode(self, winner, b):
    self.data[-1].close_episode(winner, b)
    if self.count % self.block == 0 :
      self.show()


  def show(self):
    attributes = ["Game", "Winner", "Left_pieces", "Moves", "Player_time", "Env_time"]
    for x in zip(*[iter(attributes)]):
      print('{:<15}'.format(*x), end = '')
    print()

    pop, eop = 0, 0
    pdu, edu = 0.0, 0.0
    player_win = 0

    game_id = self.blk_id * self.block + 1 
    for i in range(game_id-1, len(self.data)):
      print('{:<15}'.format(game_id), end = '')
      print('{:<15}'.format(self.data[i].who_win), end = '')
      print('{:<15}'.format(self.data[i].win_piece), end = '')
      print('{:<15}'.format(len(self.data[i].ep_moves)), end = '')
      print('{:<15.7}'.format(self.data[i].time('p')), end = '')
      print('{:<15.7}'.format(self.data[i].time('e')))

      player_win += 1 if self.data[i].who_win == 'player' else 0
      pop += self.data[i].step('p')
      eop += self.data[i].step('e')
       
      pdu += self.data[i].time('p')
      edu += self.data[i].time('e')
      
      game_id += 1
    print()
    print("In " + str(self.block) + " games:", end='\n\n')
    print("Player win: " + str(player_win) + " games")
    print("Envir win: " + str(self.block - player_win) + " games", end = '\n\n')
    print("Player win rate: " + str(float(player_win)/float(self.block) * 100.0) + " %")
    print("Envir win rate: " + str(float(self.block - player_win)/float(self.block) * 100.0) + " %", end='\n\n')
    print("ops: ( "+'{:.7}'.format(str(float(pop)/pdu))+" | "+'{:.7}'.format(str(float(eop)/edu))+" )(Player_op | Envir_op)" )

    self.blk_id += 1


  def back(self):
    return self.data[-1]