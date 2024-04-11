# Heuristic functions
def evaluate_f1(board): #Analise apenas vas vitorias
    return board.check_victory(board.current_player) - board.check_victory(3-board.current_player)

def evaluate_f2(board): #Analise das vitorias e das vitórias iminentes
    return evaluate_f1(board) * 100 + board.check_imminent_victory(board.current_player) - board.check_imminent_victory(3-board.current_player)

def evaluate_f3(board): #Analise das vitorias, das vitórias iminentes e analise das tentativas de bloqueio
    return evaluate_f1(board) * 100  + (board.check_imminent_victory(board.current_player) +  board.check_imminent_victory(3-board.current_player) * 50)

def evaluate_f4(board): #Avalia a mobilidade
    return evaluate_f3(board) + (len(board.available_moves()) - len(board.available_moves(3-board.current_player))) *10

