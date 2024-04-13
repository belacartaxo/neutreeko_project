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

    def available_moves(self, player = None):
        if player == None: player = self.current_player
        possible_moves = []
        for piece in self.pieces[player-1]: 
            possible_moves.extend((piece, p) for p in self.piece_move(piece, player))
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
        deltap1_p2, deltap2_p3, _ = self.calculate_deltas(pieces)
        return deltap1_p2 == deltap2_p3 and deltap1_p2[0] <= 1 and deltap1_p2[1] >= -1 and deltap1_p2[1] <=1
    
    def check_imminent_victory(self, player):
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
        if delta[0] == 2 or delta[1] == 2:
            return 2* (self.current_board[((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)] == 0)
        other_points = [(p1[0] - delta[0], p1[1] - delta[1]), (p2[0] + delta[0], p2[1] + delta[1])]
        space = 0
        for p in other_points:
            if p[0] >= 0 and p[0] <= SIZE-1 and p[1] >= 0 and p[1] <= SIZE-1 and self.current_board[p] == 0:
                space +=1
        return space
    
    # def blocked_pieces(self, p1, p2, delta, player):
    #     if delta[0] == 2 or delta[1] == 2:
    #         return self.current_board[((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)] == 3-player
    #     other_points = [(p1[0] - delta[0], p1[1] - delta[1]), (p2[0] + delta[0], p2[1] + delta[1])]
    #     block = 0
    #     for p in other_points:
    #         if p[0] >= 0 and p[0] <= SIZE-1 and p[1] >= 0 and p[1] <= SIZE-1 and self.current_board[p] == 3-player:
    #             block +=1

    #     return block

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

    def calculate_deltas(self, pieces):
        """Calcula e retorna as diferenças entre as peças de um jogador."""
        deltap1_p2 = (pieces[1][0] - pieces[0][0], pieces[1][1] - pieces[0][1])
        deltap2_p3 = (pieces[2][0] - pieces[1][0], pieces[2][1] - pieces[1][1])
        deltap1_p3 = (pieces[2][0] - pieces[0][0], pieces[2][1] - pieces[0][1])
        return deltap1_p2, deltap2_p3, deltap1_p3




    # def is_within_bounds(self, x, y):
    #     return 0 <= x < self.size and 0 <= y < self.size

    # def is_empty(self, x, y):
    #     return self.current_board[x][y] == 0  # Suponhamos que 0 representa uma célula vazia.

    # def get_cell(self, x, y):
    #     """Retorna o valor em uma célula específica do tabuleiro."""
    #     if self.is_within_bounds(x, y):
    #         return self.current_board[x][y]
    #     return None  # Retorna None se a célula estiver fora dos limites

    # def set_cell(self, x, y, value):
    #     """Define o valor de uma célula específica do tabuleiro."""
    #     if self.is_within_bounds(x, y):
    #         self.current_board[x][y] = value

    # def count_possible_moves(self, player):
    #     """
    #     Conta todos os movimentos possíveis para um dado jogador considerando as regras de movimento de Neutreeko.
    #     """
    #     count = 0
    #     # Varre o tabuleiro em busca de peças do jogador
    #     for i in range(self.size):
    #         for j in range(self.size):
    #             if self.current_board[i][j] == player:
    #                 # Verifica todas as direções possíveis de movimento
    #                 directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    #                 for dx, dy in directions:
    #                     # Continua na direção enquanto houver espaço vazio
    #                     step = 1
    #                     while True:
    #                         new_x, new_y = i + step * dx, j + step * dy
    #                         if not self.is_within_bounds(new_x, new_y) or self.current_board[new_x][new_y] != 0:
    #                             break
    #                         count += 1
    #                         step += 1
    #     return count

    # def count_opponent_threats(self, x, y, opponent):
    #     directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # Horizontal, Vertical, Diagonal, Anti-diagonal
    #     threat_count = 0
    #     for dx, dy in directions:
    #         for step in range(-2, 3):  # Verifica uma linha de 5 células centrada em (x, y)
    #             line = [self.get_cell(x + i*dx, y + i*dy) for i in range(step, step + 3) if self.is_within_bounds(x + i*dx, y + i*dy)]
    #             if len(line) == 3 and all(cell == opponent or (i == -step and cell == 0) for i, cell in enumerate(line)):
    #                 threat_count += 1
    #     return threat_count

    # def blocks_imminent_victory(self, x, y, opponent):
    #     directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    #     for dx, dy in directions:
    #         for step in range(-2, 3):
    #             line = [self.get_cell(x + i*dx, y + i*dy) for i in range(step, step + 3) if self.is_within_bounds(x + i*dx, y + i*dy)]
    #             if len(line) == 3 and line.count(opponent) == 2 and line.count(0) == 1:
    #                 return True
    #     return False

    # def creates_dual_threat(self, x, y, current_player):
    #     self.set_cell(x, y, current_player)  # Temporariamente coloca a peça do jogador atual
    #     threat_created = self.count_opponent_threats(x, y, current_player) >= 2
    #     self.set_cell(x, y, 0)  # Remove a peça após a verificação
    #     return threat_created

    # def reduces_opponent_mobility(self, x, y, opponent):
    #     original_moves = self.count_possible_moves(opponent)
    #     self.set_cell(x, y, 1)  # Bloqueia a célula temporariamente
    #     new_moves = self.count_possible_moves(opponent)
    #     self.set_cell(x, y, 0)  # Restaura a célula
    #     return new_moves < original_moves
