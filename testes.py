from .neutreeko.board import Board
 
class Teste:
    def __init__(self):
            # Initial positions for pieces on the board
            self.initial_position = [(4, 1),(1, 2), (4, 3)], [(0,1), (3, 2), (0,3)]
            self.board = Board(self.initial_position) 