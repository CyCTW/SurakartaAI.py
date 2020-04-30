from Board import Board
from Policy import Policy

if __name__=='__main__':
    b = Board()
    piece = 1
    while True:
        Policy.Human(b, piece)
        piece = -piece