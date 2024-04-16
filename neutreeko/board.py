import numpy as np
from copy import deepcopy
SIZE = 5  # Defines the size of the board (5x5).

class Board:
    def __init__(self, pieces): 
        # Initializes the board with the current layout of pieces.
        self.current_board = self.create_board(pieces) # Creates a matrix representation of the board.
        self.pieces = pieces # List of pieces positions for each player.
        self.current_player = 1 # Tracks the current player (player 1 starts).
        self.winner = -1  # Indicates the winner of the game (-1 means no winner yet)
        # List of all possible movement functions for a piece.
        self.move_functions = [self.vertical_up, self.vertical_down, self.horizontal_left, self.horizontal_right, self.diagonal_up_left,
                             self.diagonal_up_right, self.diagonal_down_left, self.diagonal_down_right]
        # List to track the states of pieces across moves to detect draws.        
        self.consecutive_plays = [self.sorted_list(self.pieces)]

    def __str__(self):
        # Returns a string representation of the board matrix.
        return str(self.current_board)
    
    def sorted_list(self, list_of_lists):
        # Sorts and returns the lists of pieces based on their position sums.
        return [sorted(sublist, key=lambda x: sum(x)) for sublist in list_of_lists]

    def create_board(self, pieces):
        # Creates a 2D numpy array to represent the board and places pieces accordingly.
        new_board = np.zeros((SIZE, SIZE))
        for i in range(len(pieces)):
            for p in pieces[i]:
                new_board[p[0],p[1]] = i + 1
        return new_board

    def move(self, old_piece, new_piece):
        # Returns a new board state after moving a piece.
        board_copy = deepcopy(self) # Deep copy to avoid modifying the original board.
        piece_index = board_copy.pieces[board_copy.current_player-1].index(old_piece)
        board_copy.pieces[board_copy.current_player-1][piece_index] = new_piece
        board_copy.current_board = board_copy.create_board(board_copy.pieces)
        # Append the new state of pieces to track repeats (for draw detection).
        board_copy.consecutive_plays.append(board_copy.sorted_list(board_copy.pieces))
        # Update the winner and switch the current player.
        board_copy.winner = board_copy.update_winner()
        board_copy.current_player= 3 - self.current_player
        return board_copy

    def available_moves(self, player = None):
        # Returns a list of all possible moves for the current or specified player.
        if player == None: player = self.current_player
        possible_moves = []
        for piece in self.pieces[player-1]: 
            possible_moves.extend((piece, p) for p in self.piece_move(piece, player))
        return possible_moves

    def piece_move(self, piece, player):
        # Determines all potential moves for a given piece by player using defined move functions.
        p_moves = []
        for func in self.move_functions:
            funct_move = func(piece, player)
            if funct_move:
                p_moves.append(funct_move)
        return p_moves
    # Movement methods are defined here for each direction a piece can move.
    # Each method checks boundary conditions and other pieces' positions before determining the new possible position.

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
        # Checks for a winner or a draw. Updates the winner if a winning condition is met.
        if self.check_draw():
            return 0  # 0 indicates a draw.
        if self.check_victory(self.current_player):
            return self.current_player # Returns the current player as the winner.
        return -1 # -1 indicates that there is no winner yet.

    def check_victory(self, player):
        # Checks if the current player has achieved a winning configuration (three aligned pieces).
        pieces = sorted(self.pieces[player - 1])
        deltap1_p2, deltap2_p3, _ = self.calculate_deltas(pieces)
        # Checks if the pieces are aligned straight with allowed movement deltas.
        return deltap1_p2 == deltap2_p3 and deltap1_p2[0] <= 1 and deltap1_p2[1] >= -1 and deltap1_p2[1] <=1
    
    def check_imminent_victory(self, player):
        # Checks for positions where victory is one move away.
        pieces = sorted(self.pieces[player - 1])
        deltas = self.calculate_deltas(pieces)
        ind_pieces_delta=[(0,1), (1, 2), (0, 2)]
        valid_deltas = {(0, 1), (1, 0), (1, 1), (1, -1)}
        valid_deltas_with_space = {(0, 2), (2, 0), (2, 2), (2, -2)}
        cont = 0
        #block = 0

        for i in range(len(pieces)):
            if deltas[i] in valid_deltas or deltas[i] in valid_deltas_with_space:
                cont += self.check_spaces(pieces[ind_pieces_delta[i][0]], pieces[ind_pieces_delta[i][1]], deltas[i])
                #block += self.blocked_pieces(pieces[ind_pieces_delta[i][0]], pieces[ind_pieces_delta[i][1]], deltas[i], player)
        return cont #[cont, block]
    
    def check_spaces(self, p1, p2, delta):
    # Check if the move involves skipping over a space (a delta of 2 in any direction).
        if delta[0] == 2 or delta[1] == 2:
        # If yes, check the midpoint between the two pieces for emptiness,
        # and return twice the result (since an empty midpoint is critical for a potential win).
            return 2* (self.current_board[((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)] == 0)
        # If the delta is not 2, calculate potential positions for moving before p1 and after p2.        
        other_points = [(p1[0] - delta[0], p1[1] - delta[1]), (p2[0] + delta[0], p2[1] + delta[1])]
        space = 0 # Initialize a counter for empty spaces.
        # Loop through the calculated points to see if they are within board boundaries and are empty.
        for p in other_points:
            # Check each point for boundary adherence and emptiness.
            if p[0] >= 0 and p[0] <= SIZE-1 and p[1] >= 0 and p[1] <= SIZE-1 and self.current_board[p] == 0:
                space +=1 # Increment the counter for each valid, empty space.
        return space # Return the total count of empty spaces around the pieces.
    

    def check_draw(self):
        # Checks for repeated board states to determine a draw.
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

    def calculate_deltas(self, pieces):
        # Calculates the differences between the positions of the player's pieces.
        deltap1_p2 = (pieces[1][0] - pieces[0][0], pieces[1][1] - pieces[0][1])
        deltap2_p3 = (pieces[2][0] - pieces[1][0], pieces[2][1] - pieces[1][1])
        deltap1_p3 = (pieces[2][0] - pieces[0][0], pieces[2][1] - pieces[0][1])
        return deltap1_p2, deltap2_p3, deltap1_p3
