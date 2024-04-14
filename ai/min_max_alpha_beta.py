def execute_minimax_alpha_beta_move(evaluate_func, depth):
    def execute_minimax_alpha_beta_move_aux(game):
        # This function updates the game state to the best possible move
        # determined by the Minimax algorithm with Alpha-Beta pruning.
        best_move = None
        best_eval = float('-inf')
        # Iterate over all available moves from the current game state
        for move in game.board.available_moves():
            # Apply the move to generate a new game state
            new_state = game.board.move(move[0], move[1])
            # Recursively calculate the evaluation of this new state by Minimax
            # False indicates it's the opponent's turn next (minimizing player)
            new_state_eval = minimax_alpha_beta(new_state, depth - 1, float('-inf'), float('+inf'), False, game.board.current_player, evaluate_func)
            # Update best move if this state has a better evaluation
            if new_state_eval > best_eval:
                best_move = new_state
                best_eval = new_state_eval
        # Update the game board to the best move found
        game.board = best_move
        
    return execute_minimax_alpha_beta_move_aux

def minimax_alpha_beta(state, depth, alpha, beta, maximizing, player, evaluate_func): #state - new state (estado atual do tabuleiro)
    # Base case: return the heuristic value of the state if the maximum depth is reached or the game is over
    if depth == 0 or state.winner != -1:
        return evaluate_func(state, depth) * (1 if player == 3-state.current_player else -1)
    
    if maximizing:
        max_eval = float('-inf')
        # Explore all possible moves from this state for maximizing player
        for move in state.available_moves():
            # Create new state by applying the move
            new_state = state.move(move[0], move[1])
            # Recursively evaluate the new state, switching to minimizing
            eval = minimax_alpha_beta(new_state, depth - 1, alpha, beta, False, player, evaluate_func)
            # Find the maximum evaluation
            max_eval = max(max_eval, eval)
            # Update alpha value
            alpha = max(alpha, eval)
            # Alpha-Beta Pruning
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        # Explore all possible moves from this state for minimizing player
        for move in state.available_moves():
            # Create new state by applying the move
            new_state = state.move(move[0], move[1])
            # Recursively evaluate the new state, switching to maximizing
            eval = minimax_alpha_beta(new_state, depth - 1, alpha, beta, True, player, evaluate_func)
            # Find the minimum evaluation
            min_eval = min(min_eval, eval)
            # Update beta value
            beta = min(beta, eval)
            # Alpha-Beta Pruning
            if beta <= alpha:
                break
        return min_eval
    