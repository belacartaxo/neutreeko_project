def execute_negamax_alpha_beta_move(evaluate_func, depth):
    def execute_negamax_alpha_beta_move_aux(game):
        # updates the game state to the best possible move (uses negamax to determine it)
        best_move = None
        best_eval = float('-inf')
        for move in game.board.available_moves():
            new_state = game.board.move(move[0], move[1])
            # using negamax recursion with alpha-beta pruning
            new_state_eval = -negamax_alpha_beta(new_state, depth - 1, -float('inf'), -float('inf'), game.board.current_player, evaluate_func)
            if new_state_eval > best_eval:
                best_move = new_state
                best_eval = new_state_eval
        game.board = best_move
        
    return execute_negamax_alpha_beta_move_aux

def negamax_alpha_beta(state, depth, alpha, beta, player, evaluate_func):
    if depth == 0 or state.winner != -1:
        return evaluate_func(state, depth) * (1 if player == 3-state.current_player else -1)
    
    max_eval = float('-inf')
    for move in state.available_moves():
        new_state = state.move(move[0], move[1])
        eval = -negamax_alpha_beta(new_state, depth - 1, -beta, -alpha, player, evaluate_func)
        max_eval = max(max_eval, eval)
        alpha = max(alpha, eval)
        if alpha >= beta:
            break
    return max_eval
