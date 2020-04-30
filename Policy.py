

class Policy():
    @staticmethod
    def Human(board, piece):
        # inputmv = input()

        # inputmv.split(" ")
        act_list = board.check_action(piece)
        print("Available actions: ")
        print(act_list)
        if not act_list:
            return
        else:
            print(board)
            # print(act_list)
            print("Please input action from above actions:")
            act = input()
            act = act.split(" ")
            board.move( int(act[0]), int(act[1]), piece)
    
    @staticmethod
    def Greedy(board, piece):
        act_list = board.check_action(piece)

        if not act_list:
            return
        else:
            return act_list[0]

