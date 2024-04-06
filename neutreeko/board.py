import numpy as np
#from game import SIZE
SIZE = 5
class Board:

    def __init__(self, pieces): 
        # Initialize the board with pieces and current game state
        self.current_board = self.create_board(pieces)
        self.pieces = pieces
        self.current_player = 1
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
    def move(self, old_piece, new_piece):
        # Update the board with the new pieces after a move
        piece_index = self.pieces[self.current_player-1].index(old_piece)
        self.pieces[self.current_player-1][piece_index] = new_piece
        self.current_board = self.create_board(self.pieces)
        self.winner = self.update_winner()
        self.consecutive_plays = sorted(self.pieces)

    def available_moves(self):
        # Return a list of available moves for the current player
        possible_moves = []
        for piece in self.pieces[self.current_player-1]: 
            possible_moves.append((piece, p) for p in self.piece_move(piece))
            # peças, peças que poden ser mechidas
        return possible_moves

    def piece_move(self, piece):
        p_moves = []
        for func in self.move_functions:
            funct_move = func(piece)
            if funct_move:
                p_moves.append(funct_move)
        return p_moves


    # MOVE FUNCTIONS
    # VERTICAL
    def vertical_up(self, piece):
        # Attempt to move a piece upwards
        row, col = piece[0], piece[1]
        if row == 0 or self.current_board[ row-1, col] != 0 or self.current_player != self.current_board[row, col]:
            return None
     
        while row != 0:
            row -= 1
            if (row, col) in self.pieces[0] or (row, col) in self.pieces[1]:
                return (row+1, col)

        return (0,col)



    def vertical_down(self, piece): 
        # Attempt to move a piece downwards
        row, col = piece[0], piece[1]
        if row == SIZE-1 or self.current_board[ row+1, col] != 0 or self.current_player != self.current_board[row, col]:
            return None
        
        while row != SIZE-1:
            row += 1
            if (row, col) in self.pieces[0] or (row, col) in self.pieces[1]:
                return (row-1, col)

        return (SIZE-1,col)



    #HORIZONTAL
    def horizontal_left(self, piece):
        # Attempt to move a piece to the left
        row, col = piece[0], piece[1]
        if col == 0 or self.current_board[ row, col-1] != 0 or self.current_player != self.current_board[row, col]: 
            return None

        while col != 0:
            col -= 1
            if (row, col) in self.pieces[0] or (row, col) in self.pieces[1]:
                return (row, col+1)
            
        return (row, 0)



    def horizontal_right(self, piece):
        # Attempt to move a piece to the right
        row, col = piece[0], piece[1]
        if col == SIZE-1 or self.current_board[ row, col+1] != 0 or self.current_player != self.current_board[row, col]: 
            return None

        while col != SIZE-1:
            col += 1
            if (row, col) in self.pieces[0] or (row, col) in self.pieces[1]:
                return (row, col-1)

        return (row,SIZE-1)



    #DIAGONAL
    def diagonal_up_left(self, piece):
        # Attempt to move a piece diagonally up and to the left
        row, col = piece[0], piece[1]
        if row == 0 or col == 0 or self.current_board[row-1][col-1] != 0 or self.current_player != self.current_board[row, col]:
            return None
        
        while row != 0 and col != 0:
            row -= 1
            col -= 1
            if (row, col) in self.pieces[0] or (row, col) in self.pieces[1]:
                return (row+1, col+1)

        return (row, col)



    def diagonal_up_right(self, piece):
        # Attempt to move a piece diagonally up and to the right
        row, col = piece[0], piece[1]
        if row == 0 or col == SIZE-1 or self.current_board[row-1][col+1] != 0 or self.current_player != self.current_board[row, col]:
            return None
        
        while row != 0 and col != SIZE-1:
            row -= 1
            col += 1
            if (row, col) in self.pieces[0] or (row, col) in self.pieces[1]:
                return (row+1, col-1)

        return (row, col)



    def diagonal_down_left(self, piece):
        # Attempt to move a piece diagonally down and to the left
        row, col = piece[0], piece[1]
        if row == SIZE-1 or col == 0 or self.current_board[row+1][col-1] != 0 or self.current_player != self.current_board[row, col]:
            return None

        while row != SIZE-1 and col != 0:
            row += 1
            col -= 1
            if (row, col) in self.pieces[0] or (row, col) in self.pieces[1]:
                return (row-1, col+1)
            
        return (row, col)



    def diagonal_down_right(self, piece):
        # Attempt to move a piece diagonally down and to the right
        row, col = piece[0], piece[1]
        if row == SIZE-1 or col == SIZE-1 or self.current_board[row+1][col+1] != 0 or self.current_player != self.current_board[row, col]:
            return None

        while row != SIZE-1 and col != SIZE-1:
            row += 1
            col += 1
            if (row, col) in self.pieces[0] or (row, col) in self.pieces[1]:
                return (row-1, col-1)

        return (row, col)



    # ANALYZING WINNER
    def update_winner(self):
        #draw
        if len(self.consecutive_plays) == 5:
            if self.consecutive_plays[0] == self.consecutive_plays[2] and self.consecutive_plays[SIZE-1]:
                return 0
            self.consecutive_plays.pop(0)

        pieces = sorted(self.pieces[self.current_player-1])

        if (pieces[0][0], pieces[0][1]+1) == (pieces[1][0], pieces[1][1]):
            if (pieces[1][0], pieces[1][1]+1) == (pieces[2][0], pieces[2][1]):
                return self.current_player
            return -1

        if (pieces[0][0]+1, pieces[0][1]) == (pieces[1][0], pieces[1][1]):
            if (pieces[1][0]+1, pieces[1][1]) == (pieces[2][0], pieces[2][1]):
                  return self.current_player
            return -1

        if (pieces[0][0]+1, pieces[0][1]+1) == (pieces[1][0], pieces[1][1]):
            if (pieces[1][0]+1, pieces[1][1]+1) == (pieces[2][0], pieces[2][1]):
                return self.current_player
            return -1

        if (pieces[0][0]+1, pieces[0][1]-1) == (pieces[1][0], pieces[1][1]):
            if (pieces[1][0]+1, pieces[1][1]-1) == (pieces[2][0], pieces[2][1]):
                return self.current_player
        return -1 
