import sys
import torch
from Board import Board
from Policy import Policy
from Agent import Player, Envir
from Episode import Episode
from Statistic import Statistic
from Train import train_net

if __name__=='__main__':

    total, block = 1, 0
    load_module = ""
    for arg in sys.argv:
        if arg.find("--total=") != -1:
            total = int(arg[arg.find("--total=")+8:])
        elif arg.find("--block=") != -1:
            block = int(arg[arg.find("--block=")+8:])
        elif arg.find("--load=") != -1:
            load_module = arg[arg.find("--load=")+7:]

    if load_module :
        NotImplemented
    
    if torch.cuda.is_available():
        NotImplemented

    stat = Statistic(total, block)

    play = Player(1) #Black
    env = Envir(-1) #White
    trainset = Episode()

    while not stat.is_finished():

        b = Board()

        stat.open_episode()
        game = stat.back()

        while True:
            # player first
            who = game.take_turns(play, env)
            prev_b = b

            mv_prev, mv_next = who.take_action(b)
            
            # end game
            if mv_prev == -1:
                break

            game.record(mv_prev, mv_next, prev_b, who.get_piece())
            trainset.record_train_boards(b, who.get_piece())


        win = game.get_winner(play, env)
        stat.close_episode(win, b)
        trainset.train_close_episode(win, b)

        # train_net(trainset)
        # trainset.clear()