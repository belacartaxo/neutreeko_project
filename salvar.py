import numpy as np

SIZE = 5

class Board:

    def __init__(self, pieces): 
        # Initialize the board with pieces and current game state
        self.current_board = self.create_board(pieces)
        self.pieces = pieces
        self.current_player = 2
        self.winner = -1
        self.move_functions = [self.vertical_up, self.vertical_down, self.horizontal_left, self.horizontal_right, self.diagonal_up_left,
                             self.diagonal_up_right, self.diagonal_down_left, self.diagonal_down_right]
        self.consecutive_plays = []

    def __str__(self):
        # Return string representation of the current board
        return str(self.current_board)

    def create_board(self, pieces):
         # Create a new board based on the given pieces
        new_board = np.zeros((SIZE, SIZE))
        for i in range(len(pieces)):
            for p in pieces[i]:
                new_board[p[0],p[1]] = i + 1
        return new_board

    # MOVES
    def move(self, new_pieces):
        #print(self.current_board)
        print(new_pieces)
        # Update the board with the new pieces after a move
        self.pieces = new_pieces
        self.current_board = self.create_board(new_pieces)
        self.winner = self.update_winner()
        self.consecutive_plays = sorted(new_pieces)


    def available_moves(self):
        # Return a list of available moves for the current player
        possible_moves = []
        for move_pieces in self.pieces[self.current_player-1]:
            for func in self.move_functions:
                funct_move = func(move_pieces)
                if funct_move:
                    possible_moves.append(funct_move)
        return possible_moves


    # MOVE FUNCTIONS
    # VERTICAL
    def vertical_up(self, piece):
        # Attempt to move a piece upwards
        row, col = piece[0], piece[1]
        if row == 0 or self.current_board[ row-1, col] != 0 or self.current_player != self.current_board[row, col]:
            return None

        new_pieces = [piece[:] for piece in self.pieces] #LISTA COM TODAS AS PEÇAS DO TABULEIRO COM AS SUAS POSIÇÕES
        print(new_pieces)
        piece_index = new_pieces[self.current_player-1].index(piece) 

        for player_pieces in new_pieces:
            for p in player_pieces:
                if p[1] == col and p[0] < row-1:
                    new_pieces[self.current_player-1][piece_index] = (p[0]+1,col)
                    return new_pieces

        new_pieces[self.current_player-1][piece_index] = (0,col)
        return new_pieces



    def vertical_down(self, piece): 
        # Attempt to move a piece downwards
        row, col = piece[0], piece[1]
        if row == 4 or self.current_board[ row+1, col] != 0 or self.current_player != self.current_board[row, col]:
            return None

        new_pieces = [piece[:] for piece in self.pieces]
        piece_index = new_pieces[self.current_player-1].index(piece)

        for player_pieces in new_pieces:
            for p in player_pieces:
                if p[1] == col and p[0] > row+1:
                    new_pieces[self.current_player-1][piece_index] = (p[0]-1,col)
                    return new_pieces

        new_pieces[self.current_player-1][piece_index] = (4,col)
        return new_pieces



    #HORIZONTAL
    def horizontal_left(self, piece):
        # Attempt to move a piece to the left
        row, col = piece[0], piece[1]
        if col == 0 or self.current_board[ row, col-1] != 0 or self.current_player != self.current_board[row, col]: 
            return None

        new_pieces = [piece[:] for piece in self.pieces]
        piece_index = new_pieces[self.current_player-1].index(piece)

        for player_pieces in new_pieces:
            for p in player_pieces:
                if p[0] == row and p[1] < col-1:
                    new_pieces[self.current_player-1][piece_index] = (row, p[1]+1)
                    return new_pieces

        new_pieces[self.current_player-1][piece_index] = (row,0)
        return new_pieces



    def horizontal_right(self, piece):
        # Attempt to move a piece to the right
        row, col = piece[0], piece[1]
        if col == 4 or self.current_board[ row, col+1] != 0 or self.current_player != self.current_board[row, col]: 
            return None

        new_pieces = [piece[:] for piece in self.pieces]
        piece_index = new_pieces[self.current_player-1].index(piece)

        for player_pieces in new_pieces:
            for p in player_pieces:
                if p[0] == row and p[1] > col+1:
                    new_pieces[self.current_player-1][piece_index] = (row, p[1]-1)
                    return new_pieces

        new_pieces[self.current_player-1][piece_index] = (row,4)
        return new_pieces



    #DIAGONAL
    def diagonal_up_left(self, piece):
        # Attempt to move a piece diagonally up and to the left
        row, col = piece[0], piece[1]
        if row == 0 or col == 0 or self.current_board[row-1][col-1] != 0 or self.current_player != self.current_board[row, col]:
            return None

        new_pieces = [piece[:] for piece in self.pieces]
        piece_index = new_pieces[self.current_player-1].index(piece)

        while row != 0 and col != 0:
            row -= 1
            col -= 1
            if (row, col) in new_pieces[0] or (row, col) in new_pieces[1]:
                new_pieces[self.current_player-1][piece_index] = (row+1, col+1)
                return new_pieces

        new_pieces[self.current_player-1][piece_index] = (row, col)
        return new_pieces



    def diagonal_up_right(self, piece):
        # Attempt to move a piece diagonally up and to the right
        row, col = piece[0], piece[1]
        if row == 0 or col == 4 or self.current_board[row-1][col+1] != 0 or self.current_player != self.current_board[row, col]:
            return None

        new_pieces = [piece[:] for piece in self.pieces]
        piece_index = new_pieces[self.current_player-1].index(piece)

        while row != 0 and col != 4:
            row -= 1
            col += 1
            if (row, col) in new_pieces[0] or (row, col) in new_pieces[1]:
                new_pieces[self.current_player-1][piece_index] = (row+1, col-1)
                return new_pieces

        new_pieces[self.current_player-1][piece_index] = (row, col)
        return new_pieces



    def diagonal_down_left(self, piece):
        # Attempt to move a piece diagonally down and to the left
        row, col = piece[0], piece[1]
        if row == 4 or col == 0 or self.current_board[row+1][col-1] != 0 or self.current_player != self.current_board[row, col]:
            return None

        new_pieces = [piece[:] for piece in self.pieces]
        piece_index = new_pieces[self.current_player-1].index(piece)

        while row != 4 and col != 0:
            row += 1
            col -= 1
            if (row, col) in new_pieces[0] or (row, col) in new_pieces[1]:
                new_pieces[self.current_player-1][piece_index] = (row-1, col+1)
                return new_pieces

        new_pieces[self.current_player-1][piece_index] = (row, col)
        return new_pieces



    def diagonal_down_right(self, piece):
        # Attempt to move a piece diagonally down and to the right
        row, col = piece[0], piece[1]
        if row == 4 or col == 4 or self.current_board[row+1][col+1] != 0 or self.current_player != self.current_board[row, col]:
            return None

        new_pieces = [piece[:] for piece in self.pieces]
        piece_index = new_pieces[self.current_player-1].index(piece)

        while row != 4 and col != 4:
            row += 1
            col += 1
            if (row, col) in new_pieces[0] or (row, col) in new_pieces[1]:
                new_pieces[self.current_player-1][piece_index] = (row-1, col-1)
                return new_pieces

        new_pieces[self.current_player-1][piece_index] = (row, col)
        return new_pieces




    # ANALYZING WINNER
    def update_winner(self):
        #draw
        if len(self.consecutive_plays) == 5:
            if self.consecutive_plays[0] == self.consecutive_plays[2] and self.consecutive_plays[4]:
                return 0
            self.consecutive_plays.pop(0)

        pieces = sorted(self.pieces[self.current_player-1])
        if (pieces[0][0], pieces[0][1]+1) == pieces[1]:
            if (pieces[1][0], pieces[1][1]+1) == pieces[2]:
                return self.current_player
            return -1

        if (pieces[0][0]+1, pieces[0][1]) == pieces[1]:
            if (pieces[1][0]+1, pieces[1][1]) == pieces[2]:
                  return self.current_player
            return -1

        if (pieces[0][0]+1, pieces[0][1]+1) == pieces[1]:
            if (pieces[1][0]+1, pieces[1][1]+1) == pieces[2]:
                return self.current_player
            return -1

        if (pieces[0][0]+1, pieces[0][1]-1) == pieces[1]:
            if (pieces[1][0]+1, pieces[1][1]-1) == pieces[2]:
                return self.current_player
        return -1
'''

board = Board([[(4,4),(3,0),(1,4)],[(0,1),(4,0),(2,4)]])
print(board)
peça = board.vertical_up((4,4))
print(peça)
board.move(peça)
print(board)

'''