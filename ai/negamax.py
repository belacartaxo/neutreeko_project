# TO DO - ajeitar
def execute_negamax_move(evaluate_func, depth):
    def execute_negamax_move_aux(game):
        # This function updates the game state to the best possible move determined by the Negamax algorithm.
        best_move = None
        best_eval = float('-inf')
        # Iterate through all available moves to explore possible future game states.
        for move in game.board.available_moves():
            # Apply a move to generate a new game state.
            new_state = game.board.move(move[0], move[1])
            # Using Negamax recursion to evaluate the new state. 
            # Note the negation, which simplifies handling the minimax logic for two-player games by only considering maximizing.
            new_state_eval = -negamax(new_state, depth - 1, game.board.current_player, evaluate_func)
            # Update the best evaluated move.
            if new_state_eval > best_eval:
                best_move = new_state
                best_eval = new_state_eval
        # Set the game board to the best move found.
        game.board = best_move
    # Return the auxiliary function to be called with the game object.    
    return execute_negamax_move_aux

def negamax(state, depth, player, evaluate_func):
    # Base case: Return the evaluated score if at max depth or if a winning state is reached.
    if depth == 0 or state.winner != -1:
        # Score is adjusted by player perspective, flipping the sign based on whether it's the current player or the opponent.
        return evaluate_func(state, depth) * (1 if player == 3-state.current_player else -1)
    
    max_eval = float('-inf')
    # Explore each possible move from the current game state.
    for move in state.available_moves():
        # Apply the move to create a new game state.
        new_state = state.move(move[0], move[1])
        # Recursively apply Negamax, negating the result to alternate between maximizing and minimizing.
        eval = -negamax(new_state, depth - 1, player, evaluate_func)
        # Update the maximum evaluation found.
        max_eval = max(max_eval, eval)
    # Return the highest evaluation from all explored moves.
    return max_eval
