def execute_negamax_alpha_beta_move(evaluate_func, depth):
    def execute_negamax_alpha_beta_move_aux(game):
        # This function updates the game state to the best possible move
        # determined by the Negamax algorithm with Alpha-Beta pruning.
        best_move = None
        best_eval = float('-inf')
        # Iterate over all available moves from the current game state
        for move in game.board.available_moves():
            # Apply the move to generate a new game state
            new_state = game.board.move(move[0], move[1])
            # Recursively calculate the evaluation of this new state by Negamax
            eval = -negamax_alpha_beta(new_state, depth - 1, float('-inf'), float('+inf'), game.board.current_player, evaluate_func)
            # Update best move if this state has a better evaluation
            if eval > best_eval:
                best_move = new_state
                best_eval = eval
        # Update the game board to the best move found
        game.board = best_move
        
    return execute_negamax_alpha_beta_move_aux

def negamax_alpha_beta(state, depth, alpha, beta, player, evaluate_func): #state - new state (estado atual do tabuleiro)
    # Base case: return the heuristic value of the state if the maximum depth is reached or the game is over
    if depth == 0 or state.winner != -1:
        return evaluate_func(state, depth) * (1 if player == 3-state.current_player else -1)
    
    max_eval = float('-inf')
    # Explore all possible moves from this state for the current player
    for move in state.available_moves():
        # Create new state by applying the move
        new_state = state.move(move[0], move[1])
        # Recursively evaluate the new state, switching players
        eval = -negamax_alpha_beta(new_state, depth - 1, -beta, -alpha, 3 - player, evaluate_func)
        # Find the maximum evaluation
        max_eval = max(max_eval, eval)
        # Update alpha value
        alpha = max(alpha, eval)
        # Alpha-Beta Pruning
        if beta <= alpha:
            break
    return max_eval