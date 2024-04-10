import numpy as np
from copy import deepcopy
SIZE = 5

class Board:
    def __init__(self, pieces): 
        self.current_board = self.create_board(pieces)
        self.pieces = pieces
        self.current_player = 1
        self.winner = -1
        self.move_functions = [self.vertical_up, self.vertical_down, self.horizontal_left, self.horizontal_right, self.diagonal_up_left,
                             self.diagonal_up_right, self.diagonal_down_left, self.diagonal_down_right]
        self.consecutive_plays = [self.sorted_list(self.pieces)]

    def __str__(self):
        return str(self.current_board)
    
    def sorted_list(self, list_of_lists):
        return [sorted(sublist, key=lambda x: sum(x)) for sublist in list_of_lists]

    def create_board(self, pieces):
        new_board = np.zeros((SIZE, SIZE))
        for i in range(len(pieces)):
            for p in pieces[i]:
                new_board[p[0],p[1]] = i + 1
        return new_board

    def move(self, old_piece, new_piece):
        board_copy = deepcopy(self)
        piece_index = board_copy.pieces[board_copy.current_player-1].index(old_piece)
        board_copy.pieces[board_copy.current_player-1][piece_index] = new_piece
        board_copy.current_board = board_copy.create_board(board_copy.pieces)
        board_copy.consecutive_plays.append(board_copy.sorted_list(board_copy.pieces))
        board_copy.winner = board_copy.update_winner()
        return board_copy

    def available_moves(self):
        possible_moves = []
        for piece in self.pieces[self.current_player-1]: 
            possible_moves.extend((piece, p) for p in self.piece_move(piece, self.current_player))
        return possible_moves

    def piece_move(self, piece, player):
        p_moves = []
        for func in self.move_functions:
            funct_move = func(piece, player)
            if funct_move:
                p_moves.append(funct_move)
        return p_moves

    def vertical_up(self, piece, player):
        row, col = piece[0], piece[1]
        if row == 0 or self.current_board[row-1, col] != 0 or player != self.current_board[row, col]:
            return None
     
        while row != 0:
            row -= 1
            if (row, col) in self.pieces[0] or (row, col) in self.pieces[1]:
                return (row+1, col)
        return (0,col)

    def vertical_down(self, piece, player): 
        row, col = piece[0], piece[1]
        if row == SIZE-1 or self.current_board[row+1, col] != 0 or player != self.current_board[row, col]:
            return None
        
        while row != SIZE-1:
            row += 1
            if (row, col) in self.pieces[0] or (row, col) in self.pieces[1]:
                return (row-1, col)
        return (SIZE-1,col)

    def horizontal_left(self, piece, player):
        row, col = piece[0], piece[1]
        if col == 0 or self.current_board[row, col-1] != 0 or player != self.current_board[row, col]: 
            return None

        while col != 0:
            col -= 1
            if (row, col) in self.pieces[0] or (row, col) in self.pieces[1]:
                return (row, col+1)
        return (row, 0)

    def horizontal_right(self, piece, player):
        row, col = piece[0], piece[1]
        if col == SIZE-1 or self.current_board[row, col+1] != 0 or player != self.current_board[row, col]: 
            return None

        while col != SIZE-1:
            col += 1
            if (row, col) in self.pieces[0] or (row, col) in self.pieces[1]:
                return (row, col-1)
        return (row,SIZE-1)

    def diagonal_up_left(self, piece, player):
        row, col = piece[0], piece[1]
        if row == 0 or col == 0 or self.current_board[row-1][col-1] != 0 or player != self.current_board[row, col]:
            return None
        
        while row != 0 and col != 0:
            row -= 1
            col -= 1
            if (row, col) in self.pieces[0] or (row, col) in self.pieces[1]:
                return (row+1, col+1)
        return (row, col)

    def diagonal_up_right(self, piece, player):
        row, col = piece[0], piece[1]
        if row == 0 or col == SIZE-1 or self.current_board[row-1][col+1] != 0 or player != self.current_board[row, col]:
            return None
        
        while row != 0 and col != SIZE-1:
            row -= 1
            col += 1
            if (row, col) in self.pieces[0] or (row, col) in self.pieces[1]:
                return (row+1, col-1)
        return (row, col)

    def diagonal_down_left(self, piece, player):
        row, col = piece[0], piece[1]
        if row == SIZE-1 or col == 0 or self.current_board[row+1][col-1] != 0 or player != self.current_board[row, col]:
            return None

        while row != SIZE-1 and col != 0:
            row += 1
            col -= 1
            if (row, col) in self.pieces[0] or (row, col) in self.pieces[1]:
                return (row-1, col+1)
        return (row, col)

    def diagonal_down_right(self, piece, player):
        row, col = piece[0], piece[1]
        if row == SIZE-1 or col == SIZE-1 or self.current_board[row+1][col+1] != 0 or player != self.current_board[row, col]:
            return None

        while row != SIZE-1 and col != SIZE-1:
            row += 1
            col += 1
            if (row, col) in self.pieces[0] or (row, col) in self.pieces[1]:
                return (row-1, col-1)
        return (row, col)

    def update_winner(self):
        if self.check_draw():
            return 0
        if self.check_victory(self.current_player):
            return self.current_player
        return -1

    def check_victory(self, player):
        pieces = sorted(self.pieces[player - 1])
        deltap1_p2 = (pieces[1][0] - pieces[0][0], pieces[1][1] - pieces[0][1])
        deltap2_p3 = (pieces[2][0] - pieces[1][0], pieces[2][1] - pieces[1][1])
        print(deltap1_p2, deltap2_p3)
        return deltap1_p2 == deltap2_p3 and deltap1_p2[0] <= 1 and deltap1_p2[1] <=1
   
    
    def check_imminent_victory(self, player):
        pieces = sorted(self.pieces[player - 1])
        deltap1_p2 = (pieces[1][0] - pieces[0][0], pieces[1][1] - pieces[0][1])
        deltap2_p3 = (pieces[2][0] - pieces[1][0], pieces[2][1] - pieces[1][1])
        deltap1_p3 = (pieces[2][0] - pieces[0][0], pieces[2][1] - pieces[0][1])
        valid_deltas = {(0, 1), (1, 0), (1, 1), (0, -1), (1, -1)}
        valid_deltas_with_space = {(0, 2), (2, 0), (2, 2), (0, -2), (2, -2)}
        cont = 0

        if deltap1_p2 in valid_deltas or deltap2_p3 in valid_deltas or deltap1_p3 in valid_deltas:
            cont += 1
            #TO DO - verificar se há espaços vazios antes ou depois das peças
            
        if deltap1_p2 in valid_deltas_with_space and self.current_board[((pieces[0][0] + pieces[1][0]) // 2, (pieces[0][1] + pieces[1][1]) // 2)] == 0:
            cont += 1
        elif deltap2_p3 in valid_deltas_with_space and self.current_board[((pieces[1][0] + pieces[2][0]) // 2, (pieces[1][1] + pieces[2][1]) // 2)] == 0:
             cont += 1
        elif deltap1_p3 in valid_deltas_with_space and self.current_board[((pieces[0][0] + pieces[2][0]) // 2, (pieces[0][1] + pieces[2][1]) // 2)] == 0:
             cont += 1

        return cont 
    
    def check_draw(self):
        state_counts = {}
        for pieces in self.consecutive_plays:
            pieces_str = str(pieces)
            if pieces_str in state_counts:
                state_counts[pieces_str] += 1
            else:
                state_counts[pieces_str] = 1

            if state_counts[pieces_str] >= 3:
                return 1
        return None


