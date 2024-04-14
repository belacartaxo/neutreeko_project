def execute_minimax_move(evaluate_func, depth):
    def execute_minimax_move_aux(game):
        # updates the game state to the best possible move (uses minimax to determine it)
        best_move = None
        best_eval = float('-inf')
        for move in game.board.available_moves():
            new_state = game.board.move(move[0], move[1])
            # maximizing = False because we are checking for the best moves for the opponent after this move
            new_state_eval = minimax(new_state, depth - 1, False, game.board.current_player, evaluate_func)

            if new_state_eval > best_eval:
                best_move = new_state
                best_eval = new_state_eval
        game.board = best_move
    
    return execute_minimax_move_aux

def minimax(state, depth, maximizing, player, evaluate_func):
    if depth == 0 or state.winner != -1:
        return evaluate_func(state)  * (1 if player == state.current_player else -1)
    
    if maximizing:
        max_eval = float('-inf')
        for move in state.available_moves():
            new_state = state.move(move[0], move[1])
            eval = minimax(new_state, depth - 1, False, player, evaluate_func)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in state.available_moves():
            new_state = state.move(move[0], move[1])
            eval = minimax(new_state, depth - 1, True, player, evaluate_func)
            min_eval = min(min_eval, eval)
        return min_eval
    