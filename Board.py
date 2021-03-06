import numpy as np
import random

class Board():
    def __init__(self):
        tiles = np.zeros(36, dtype=int) 
        # tiles[:2, :] = 1
        # tiles[4:,:] = -1
        tiles[:2*6] = 1
        tiles[4*6:] = -1
        self.tiles = tiles
        
        self.mapping_ring = (
        { 1: [ 6, 'R'],  2: [12, 'R'],  3: [17, 'L'],  4: [11, 'L'],
          6: [ 1, 'D'], 12: [ 2, 'D'], 18: [32, 'U'], 24: [31, 'U'],
         31: [24, 'R'], 32: [18, 'R'], 33: [23, 'L'], 34: [29, 'L'],
         29: [34, 'U'], 23: [33, 'U'], 17: [ 3, 'D'], 11: [ 4, 'D']
        })

        self.mp_dir4 = { 'R': 1, 'D': 6, 'L': -1, 'U':-6 }
        self.rep_act = { 1 : [[-1, -1], 0], -1 : [[-1, -1], 0] }

    def __getitem__(self, index):
        return self.tiles[index]
    def __str__(self):
        lin0 = lin1 = lin2 = lin3 = lin4 = lin5 = str()
        for i in self.tiles[:6]:
            lin0 += '{:>2d}'.format(int(i))
        for i in self.tiles[6:12]:
            lin1 += '{:>2d}'.format(int(i))
        for i in self.tiles[12:18]:
            lin2 += '{:>2d}'.format(int(i))
        for i in self.tiles[18:24]:
            lin3 += '{:>2d}'.format(int(i))
        for i in self.tiles[24:30]:
            lin4 += '{:>2d}'.format(int(i))
        for i in self.tiles[30:36]:
            lin5 += '{:>2d}'.format(int(i))
        return ("+-------------------+ \n" + 
                "      0 1 2 3 4 5     \n" + 
                "  ┏━━━━━━━┓ ┏━━━━━━━┓ \n" + 
                "  ┃ ┏━━━┓ ┃ ┃ ┏━━━┓ ┃ \n" + 
                "0 ┃ ┃" + lin0 + " ┃ ┃ \n" + 
                "1 ┃ ┗" + lin1 + " ┛ ┃ \n" + 
                "2 ┗━━" + lin2 + " ━━┛ \n" + 
                "3 ┏━━" + lin3 + " ━━┓ \n" + 
                "4 ┃ ┏" + lin4 + " ┓ ┃ \n" + 
                "5 ┃ ┃" + lin5 + " ┃ ┃ \n" + 
                "  ┃ ┗━━━┛ ┃ ┃ ┗━━━┛ ┃ \n" + 
                "  ┗━━━━━━━┛ ┗━━━━━━━┛ \n" + 
                "+-------------------+ \n"
            )   
                
    def move_a_step(self, pos, dir_):
        pos += self.mp_dir4[dir_]
        if (dir_=='U' and pos < 0 
         or dir_=='R' and pos%6==0
         or dir_=='D' and pos >=36
         or dir_=='L' and pos%6==5 ):
            pos -= self.mp_dir4[dir_]
            return pos, False
        else:
            return pos, True
        
    def search(self, *args):
        # print('search')
        dir_, piece, pos = args
        pass_ring = False
        count_step = 0
        # print("search for {}".format(pos))
        while True:
            # collide with same piece
            if self.tiles[pos] == piece or count_step >= 25:
                return -1, False
            
            # collide with rival's piece
            if self.tiles[pos] == -piece:
                if pass_ring:
                    return pos, True
                else: 
                    return -1, False

            pos, rt = self.move_a_step(pos, dir_)
            # print("now search pos is: {}".format(pos))
            if not rt:
                if not self.mapping_ring.get(pos):
                    return -1, False
                pos, dir_ = self.mapping_ring[pos]
                pass_ring = True
            count_step += 1
    
    def check_eat(self, piece, pos):
        # print('check_eat')
        self.tiles[pos] = 0
        eat_list = []
        for d in self.mp_dir4.keys():
            eat_pos, st = self.search(d, piece, pos)
            if st and eat_pos not in eat_list:
                eat_list.append([pos, eat_pos])
            
        self.tiles[pos] = piece

        return eat_list
    
    def check_move(self, piece, pos):
        
        # print('check_move')
        forbid_move = [-1 , -1]
        if self.rep_act[piece][1] >= 2:
            forbid_move = self.rep_act[piece][0]
            forbid_move = forbid_move[::-1]
            # print("Repeated move! {}".format(forbid_move))
        
        dir8 = [-7, -6, -5, -1, 1, 5, 6, 7]
        if pos <= 5 and pos >= 0:
            dir8[0] = dir8[1] = dir8[2] = 0
        if pos%6 == 0:
            dir8[0] = dir8[3] = dir8[5] = 0
        if (pos+1)%6 == 0:
            dir8[2] = dir8[4] = dir8[7] = 0
        if pos <= 35 and pos >= 30:
            dir8[5] = dir8[6] = dir8[7] = 0
        
        move_list = []
        for d in dir8:
            if d==0: continue

            next_pos = pos+d
            # print(next_pos)
            if self.tiles[next_pos] == 0 and forbid_move != [pos, next_pos]:
                move_list.append([pos, next_pos])
        
        return move_list
    
    def check_action(self, piece):
        move_list = []
        eat_list = []
        for pos, val in enumerate(self.tiles):
            if val==piece:
                # print(idx)
                mv = self.check_move(piece, pos)
                # print(mv)
                move_list.extend(mv)
                ea = self.check_eat(piece, pos)
                eat_list.extend(ea)

        # random.shuffle(move_list)
        # random.shuffle(eat_list)
        print("Move actions: ")
        print(move_list)
        print()
        print("Eat actions: ")
        print(eat_list)
        print()

        move_list.extend(eat_list)
        return eat_list, move_list
    
    def add_repeated(self, prevp, nextp):
        piece = self.tiles[prevp]
        # repeat and place pos is empty
        # print(piece, nextp, prevp)
        if self.rep_act[piece][0] == [nextp, prevp] and self.tiles[nextp] == 0:
            self.rep_act[piece][0] = [prevp, nextp]
            self.rep_act[piece][1]+=1
        # clear and append
        else:
            self.rep_act[piece][0] = [prevp, nextp]
            self.rep_act[piece][1] = 1
        print("repeated act: {}".format(self.rep_act))
        print()

    def move(self, prevp, nextp, piece):
        # check repeated move
        self.add_repeated(prevp, nextp)
        print("1 :" +str(prevp))
        print("2 :" +str(nextp))
        self.tiles[nextp] = piece
        self.tiles[prevp] = 0
    

    def flip_color(self):
        for i in range(36):
            if self.tiles[i] == 1:
                self.tiles[i] = -1
            elif self.tiles[i] == -1:
                self.tiles[i] = 1