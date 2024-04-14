def execute_minimax_move(evaluate_func, depth):
    def execute_minimax_move_aux(game):
        # This function updates the game state to the best possible move as determined by the Minimax algorithm.
        best_move = None
        best_eval = float('-inf')
        # Iterate through all available moves to explore possible game states.
        for move in game.board.available_moves():
            # Create a new game state by applying the current move.
            new_state = game.board.move(move[0], move[1])
            # Since this move has just been made, it's now the opponent's turn to play.
            # We therefore call the minimax function with maximizing set to False.            
            new_state_eval = minimax(new_state, depth - 1, False, game.board.current_player, evaluate_func)
            # Update the best move and evaluation if the current move leads to a better evaluation.
            if new_state_eval > best_eval:
                best_move = new_state
                best_eval = new_state_eval
        # Update the actual game board to reflect the best move determined.
        game.board = best_move
    # Return the auxiliary function to be called with the actual game instance.    
    return execute_minimax_move_aux

def minimax(state, depth, maximizing, player, evaluate_func):
    # Base case: if the depth limit is reached or the game is over (a player wins), return the evaluated score.
    if depth == 0 or state.winner != -1:
        # The score is modified by whether the player is the current player or the opponent.
        return evaluate_func(state, depth) * (1 if player == 3-state.current_player else -1)
    # If the current decision layer is maximizing, find the move with the maximum utility.
    if maximizing:
        max_eval = float('-inf')
        # Explore all possible subsequent moves.
        for move in state.available_moves():
            new_state = state.move(move[0], move[1])
            # Recursively call minimax as the minimizing player since the game alternates turns.
            eval = minimax(new_state, depth - 1, False, player, evaluate_func)
            # Update the maximum evaluation found.
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        # If the current decision layer is minimizing, find the move with the minimum utility.
        min_eval = float('inf')
        # Explore all possible subsequent moves.
        for move in state.available_moves():
            new_state = state.move(move[0], move[1])
            # Recursively call minimax as the maximizing player since the game alternates turns.
            eval = minimax(new_state, depth - 1, True, player, evaluate_func)
            # Update the minimum evaluation found.
            min_eval = min(min_eval, eval)
        return min_eval
    