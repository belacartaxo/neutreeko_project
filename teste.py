def evaluate_blocking_heuristic(board, current_player):
    opponent = 3 - current_player
    score = 0
    threat_multiplier = 10 #calcular a pontuação relacionada ao número de ameaças 
    block_multiplier = 50 #pontuar posições no tabuleiro que, se ocupadas pelo jogador, bloqueariam imediatamente uma vitória iminente do oponente
    dual_threat_multiplier = 30 #Usado para avaliar movimentos que não apenas bloqueiam um potencial de vitória do oponente mas também criam uma ameaça de vitória para o jogador que está fazendo o movimento.
    mobility_reduction_multiplier = 5 #Este multiplicador é utilizado para pontuar movimentos que reduziriam a mobilidade do oponente, ou seja, diminuiriam as opções de movimento disponíveis para o oponente após o movimento ser feito.2

    #
    threat_count = board.check_imminent_victory(3-board.current_player)
    score += threat_count*threat_multiplier

    # Verifica cada célula no tabuleiro
    for x in range(board.size):
        for y in range(board.size):
            if board.is_empty(x, y): # se a posição no tabuleiro está vazia
                # Conta quantas linhas potenciais do oponente passam por (x, y)
                threat_count = board.count_opponent_threats(x, y, opponent)
                score += threat_count * threat_multiplier

                # Verifica se ocupar (x, y) bloqueia uma vitória iminente do oponente
                if board.blocks_imminent_victory(x, y, opponent):
                    score += block_multiplier

                # Verifica se ocupar (x, y) cria uma ameaça dupla
                if board.creates_dual_threat(x, y, current_player):
                    score += dual_threat_multiplier

                # Avalia a redução da mobilidade do oponente se (x, y) for ocupado
                if board.reduces_opponent_mobility(x, y, opponent):
                    score += mobility_reduction_multiplier

    return score

# Explicação do Código
# count_opponent_threats: Esta função calcula quantas linhas vencedoras potenciais do oponente incluem a célula especificada.
# blocks_imminent_victory: Verifica se ocupar uma determinada célula impediria uma vitória imediata do oponente.
# creates_dual_threat: Avalia se um movimento é ofensivamente e defensivamente vantajoso.
# reduces_oppon