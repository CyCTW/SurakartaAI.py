import random
import copy
import torch
from NN import generate_states, Net

class Policy():
    @staticmethod
    def Human(board, piece):
        # inputmv = input()

        # inputmv.split(" ")
        act_list = board.check_action(piece)
        print("Available actions: ")
        print(act_list)
        if not act_list:
            return -1, -1
        else:
            print(board)
            # print(act_list)
            print("Please input action from above actions:")
            act = input()
            act = act.split(" ")

            return int(act[0]), int(act[1])
    
    @staticmethod
    def Greedy(board, piece):
        eat_list, act_list = board.check_action(piece)
        print(board)
        if not act_list:
            return -1, -1
        elif not eat_list:
            random.shuffle(act_list)
            return act_list[0]
        else:
            random.shuffle(eat_list)
            return eat_list[0]

    @staticmethod
    def NN(board, piece):
        eps = 10
        print(board)
        prob = random.randint(0, 100)

        if prob >= eps:
            now = board

            if piece == -1:
                now.flip_color()

            best_prev, best_next = -1, -1
            eat_list, act_list = board.check_action(1)
            max_val = -2.0

            for x, y in act_list:
                nextb = copy.deepcopy(now)
                nextb.move(x, y, 1)

                tensor_stack = torch.FloatTensor(1, 36).zero_()

                generate_states(tensor_stack, nextb)
                # print(tensor_stack)
                boards = tensor_stack.view(1, 1, 6, 6)
                # print(boards)
                pred_val = Net.forward(boards)
                pred = pred_val[0].item()
                # print(pred)

                if pred > max_val:
                    max_val = pred
                    best_prev, best_next = x, y 
            
            return best_prev, best_next

        else:
            eat_list, act_list = board.check_action(piece)
            if not act_list:
                return -1, -1
            else:
                random.shuffle(act_list)
                return act_list[0]



