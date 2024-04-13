def execute_negamax_move(evaluate_func, depth):
    def execute_negamax_move_aux(game):
        # updates the game state to the best possible move (uses negamax to determine it)
        best_move = None
        best_eval = float('-inf')
        for move in game.board.available_moves():
            new_state = game.board.move(move[0], move[1])
            # using negamax recursion
            new_state_eval = -negamax(new_state, depth - 1, game.board.current_player, evaluate_func)

            if new_state_eval > best_eval:
                best_move = new_state
                best_eval = new_state_eval
        game.board = best_move
        
    return execute_negamax_move_aux

def negamax(state, depth, player, evaluate_func):
    if depth == 0 or state.winner != -1:
        return evaluate_func(state) * (1 if player == 1 else -1)
    
    max_eval = float('-inf')
    for move in state.available_moves():
        new_state = state.move(move[0], move[1])
        eval = -negamax(new_state, depth - 1, player, evaluate_func)
        max_eval = max(max_eval, eval)
    return max_eval
