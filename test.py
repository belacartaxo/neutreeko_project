from neutreeko.board import Board
from ai.heuristics import *
from ai.min_max_alpha_beta import *
import time
 
class Test:
    def __init__(self, ai1, ai2):
            # Initial positions for pieces on the board
            self.initial_position = [(4, 1),(1, 2), (4, 3)], [(0,1), (3, 2), (0,3)]
            self.board = Board(self.initial_position) 
            self.ai = [ai1, ai2]
            self.winner = -1
            self.moves = 0

    def inicialize_test(self):
        self.initial_position = [(4, 1),(1, 2), (4, 3)], [(0,1), (3, 2), (0,3)]
        self.board = Board(self.initial_position)
        self.winner = -1
        self.moves = 0
    
    def run_test(self):
        self.inicialize_test()
        while True:
            if self.board.current_player == 1:
                self.ai[0](self)
            else:
                self.ai[1](self) 
            self.moves += 1
            if self.board.winner != -1:
                print(f"End of game! Player {self.board.winner} wins -> {self.moves} moves")
                self.winner = self.board.winner
                return 
            
    def run_n_matches(self, n, max_time = 3600):
        # utility function to automate n matches execution
        # should return the total distribution of players wins and draws
        # your code here
        #--------------------------------------------------#
        start_time = time.time()

        results = [0, 0, 0] # [draws, player 1 victories, player 2 victories]

        while n > 0 and time.time() - start_time < max_time:
            n -= 1
            self.run_test()
            results[self.board.winner] += 1

        print("\n=== Elapsed time: %s seconds ===" % (int(time.time() - start_time)))
        print(f"  Player 1: {results[1]} victories")
        print(f"  Player 2: {results[2]} victories")
        print(f"  Draws: {results[0]} ")
        print("===============================")

depth = 3
heuristics = [evaluate_f1, evaluate_f2, evaluate_f3]


#Heuristic x Heuristic
for i, h1 in enumerate(heuristics):
    for j, h2 in enumerate(heuristics):
        print(f"Heuristic {i+1} x Heuristic {j+1} - depth {depth}")
        test = Test(execute_minimax_alpha_beta_move(h1, depth), execute_minimax_alpha_beta_move(h2, depth))
        test.run_n_matches(5)
        print("\n\n")

#Random x heuristic
for h in range(len(heuristics)):
    print(f"Random x Heuristic {h+1} - depth {depth}")
    test = Test(execute_random_move, execute_minimax_alpha_beta_move(heuristics[h], depth))
    test.run_n_matches(5)
    print("\n\n")