from copy import deepcopy

# Heuristic functions
def evaluate_f1(board, depth): #Analise apenas vas vitorias / EASY
    return board.check_victory(3-board.current_player) * depth

def evaluate_f2(board, depth): #Analise das vitorias e das vitórias iminentes / MEDIUM
    return evaluate_f1(board, depth) * 100 + board.check_imminent_victory(board.current_player) - board.check_imminent_victory(3-board.current_player)

def evaluate_f3(board, depth): #HARD
    if evaluate_f1(board, depth): return 1000
    if board.winner == 0: return 0
    opponent_imminent_victory = board.check_imminent_victory(board.current_player)
    if opponent_imminent_victory:
        return check_for_blocking_moves(board) + board.check_imminent_victory(3-board.current_player)*15 - board.check_imminent_victory(board.current_player) * 30

    player_imminent_victory = board.check_imminent_victory(3-board.current_player)
    return player_imminent_victory * 10

def check_for_blocking_moves(board):
    new_board = deepcopy(board)
    new_board.current_player = board.current_player
    for move in board.available_moves(board.current_player):
        moved_board = new_board.move(move[0], move[1])
        if moved_board.winner != -1:
            return -400
    return 400
