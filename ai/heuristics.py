# Heuristic functions
def evaluate_f1(board): #Analise apenas vas vitorias
    return board.check_victory(board.current_player)

def evaluate_f2(board): #Analise das vitorias e das vitórias iminentes
    if board.winner == -1:
        board.check_imminent_victory2()
    #print(evaluate_f1(board) * 100 , board.check_imminent_victory(board.current_player) , board.check_imminent_victory(3-board.current_player))
    return evaluate_f1(board) * 100 + board.check_imminent_victory(board.current_player) - board.check_imminent_victory

def evaluate_f3(board): #Analise das vitorias, das vitórias iminentes e analise das tentativas de bloqueio
    return evaluate_f1(board) * 500  + (board.check_imminent_victory(board.current_player) -  board.check_imminent_victory(3-board.current_player) * 10)

def evaluate_f4(board): #Avalia a mobilidade
    return evaluate_f3(board) + (len(board.available_moves()) - len(board.available_moves(3-board.current_player))) *10



# def heuristic_value(board):
#     opponent = 3 - board.current_player  # Assume que os jogadores são 1 e 2
#     score = 0

#     # Funcão para verificar as condições de vitória em uma linha
#     def check_line(line):
#         if line.count(board.current_player) == 2 and line.count(0) == 1:
#             return 100  # Linha quase completa para o jogador
#         if line.count(opponent) == 2 and line.count(0) == 1:
#             return -100  # Linha quase completa para o oponente
#         return 0

#     # Verifica todas as linhas, colunas e diagonais
#     for i in range(board.size):
#         # Linhas
#         row = board.current_board[i, :]
#         score += check_line(row)
#         # Colunas
#         col = board.current_board[:, i]
#         score += check_line(col)

#     # Diagonais
#     diag1 = board.current_board.diagonal()
#     score += check_line(diag1)
#     diag2 = np.fliplr(board.current_board).diagonal()
#     score += check_line(diag2)

#     # Mobilidade: número de movimentos possíveis
#     mobility = len(board.available_moves(board.current_player)) - len(board.available_moves(opponent))
#     score += mobility * 10  # Dá uma pequena vantagem para mais mobilidade

#     return score

# # Exemplo de uso
# # player = 1  # Assume que estamos avaliando para o jogador 1
# # score = heuristic_value(board_instance, player)
# # print(f"Heuristic score for player {player}: {score}")


