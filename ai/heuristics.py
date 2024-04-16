# Importing deepcopy function to create deep copies of objects.
from copy import deepcopy
import random

# Heuristic functions
def evaluate_f1(board, depth): # EASY
    # Returns the value based on whether the current player is winning.
    # Multiplies the result by the current depth.
    # This emphasizes more immediate threats or victories because as the depth increases, the algorithm subtracts depth by 1.
    return board.check_victory(3-board.current_player) * depth

def evaluate_f2(board, depth): # MEDIUM
    # Uses evaluate_f1 and adjusts it by considering imminent victories.
    # Adds the difference between the imminent victories of the current player and the opponent.
    # Multiplies evaluate_f1 by 100 to prioritize actual victories over imminent ones.
    return evaluate_f1(board, depth) * 100 + board.check_imminent_victory(3-board.current_player) - board.check_imminent_victory(board.current_player)

# TO DO -verificar função de avaliação 3 
def evaluate_f3(board, depth): #HARD
    # First, checks for a straightforward victory using evaluate_f1.
    # If a victory or draw is detected, returns a high value or zero respectively.
    if evaluate_f1(board, depth): return 1000 * evaluate_f1(board,depth)
    if board.winner == 0: return 0
    # Check and handle imminent victories for the opponent.
    opponent_imminent_victory = board.check_imminent_victory(board.current_player)
    # Calculate the score by considering blocking moves and adjusting weights for imminent victories.
    if opponent_imminent_victory:
        return check_for_blocking_moves(board) + board.check_imminent_victory(3-board.current_player) - board.check_imminent_victory(board.current_player)
    # If the current player is about to win, give a score based on imminent victory.
    player_imminent_victory = board.check_imminent_victory(3-board.current_player)
    return player_imminent_victory * 10

def check_for_blocking_moves(board):
    # Create a new copy of the board to simulate future moves.
    new_board = deepcopy(board)
    # Set the player to the current player.
    new_board.current_player = board.current_player
    # Iterate through all possible moves.
    for move in board.available_moves(board.current_player):
        # Perform each move on the board copy.
        moved_board = new_board.move(move[0], move[1])
        # Check if performing the move leads to a win.
        if moved_board.winner != -1:
            return -400 # Penalize if the move leads to an opponent's win.
    return 400 # Reward if blocking moves are effective.

#random
def execute_random_move(game):
    new_pieces = random.choice(game.board.available_moves())
    game.board = game.board.move(new_pieces[0], new_pieces[1])