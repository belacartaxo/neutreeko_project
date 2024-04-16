import random
from math import sqrt, log
from copy import deepcopy

import random
# TO DO - fazer o mcts
class Node:
    def __init__(self, board, parent=None):
        self.state = board
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def add_child(self, child_board):
        child = Node(child_board, self)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result

    def is_fully_expanded(self):
        return len(self.children) > 0

    def is_terminal(self):
        if self.state.winner != -1: 
            return True
        return False

class MCTS:
    def __init__(self, root, evaluate_funct = None):
        self.root = Node(root)
        #self.evaluate_game = evaluate_funct

    def get_possible_moves(self, state):
        return state.available_moves()

    def apply_move(self, state, move):
        return state.move(move[0], move[1])

    def evaluate_game(self, state):
        return state.winner == self.current_player


    def select_best_child(self, node):
        # Retorna o filho com o maior número de visitas
        return max(node.children, key=lambda x: x.visits)

    def traverse(self, node):
        while node.is_fully_expanded():
            node = self.select_best_child(node)
        if not node.is_fully_expanded() and not node.is_terminal():
            # Example logic for expanding a node (needs actual implementation details)
            possible_moves = self.get_possible_moves(node.state)  # This method needs to be implemented
            for move in possible_moves:
                new_state = self.apply_move(node.state, move)  # This method also needs to be implemented
                if not any(child.state == new_state for child in node.children):
                    node.add_child(new_state)
        return node

    def rollout(self, node):
        while not node.is_terminal():
            node = self.rollout_policy(node)
        return self.simulate_result(node)

    def rollout_policy(self, node):
        # Implemente a lógica para escolher um filho aleatoriamente
        return random.choice(node.children)

    def simulate_result(self, node):
        current_node = node
        while not current_node.is_terminal():
            possible_moves = current_node.state.available_moves()
            chosen_move = random.choice(possible_moves)
            current_node = Node(current_node.move(chosen_move[0], chosen_move[1]), current_node)  # Simula o movimento escolhido
        return self.evaluate_game(current_node.state)  # Avalia o estado terminal do jogo
    
    def backpropagate(self, node, result):
        while node is not None:
            node.update(result)
            node = node.parent


    def monte_carlo_tree_search(self, iterations = 1000):
        for _ in range(iterations):  # Implemente sua lógica de verificação de recursos
            leaf = self.traverse(self.root)
            simulation_result = self.rollout(leaf)
            self.backpropagate(leaf, simulation_result)
        return self.select_best_child(self.root)
    

def move_mcts(game):
    mcts = MCTS(game.board)
    best_move = mcts.monte_carlo_tree_search()
    game.board = best_move

    

    '''def MCTS(game, iterations=1000):
    root_node = MCTSNode()
    for _ in range(iterations):
        node = root_node
        # Seleção
        while node.untried_moves == [] and node.children != []:
            node = node.UCTSelectChild()

        # Expansão
        if node.untried_moves:
            node = node.expand()

        # Simulação
        result = node.simulate()

        # Retropropagação
        while node is not None:
            node.backpropagate(result)

        return max(root_node.children, key=lambda x: x.visits).move  # Retorna o movimento do filho mais visitado'''

# Utilização


'''
class MCTSNode:
    def __init__(self, game, parent=None, piece_moved = None):
        #raiz vão ser as peças do tabuleiro
        self.game = deepcopy(game)
        self.pieces = game.board.pieces
        self.piece_moved = piece_moved
        self.parent = parent
        self.children = [] #conforme os nos forem analisados vai saindo daqui self.untried_moves e vai para o novo estado
        self.wins = 0
        self.visits = 0
        self.untried_moves = game.board.available_moves() # game.board.available_moves
        self.player_who_moved = game.board.current_player

    def select_child(self):
        """
        Seleciona o filho usando a fórmula UCB1 (Upper Confidence Bound 1).
        """
        log_parent_visits = log(self.visits)
        return max(self.children, key=lambda x: x.wins / x.visits + sqrt(2 * log_parent_visits / x.visits))

    def expand(self):
        """
        Expande um nó filho escolhendo um movimento dos movimentos não tentados e executando-o para criar um novo estado do jogo.
        """
        move = self.untried_moves.pop()
        new_state = self.game_state.make_move(move)  # Supõe que há um método para fazer um movimento
        child_node = MCTSNode(new_state, self, move)
        self.children.append(child_node)
        return child_node

    def simulate(self):
        """
        Simula um jogo aleatório a partir deste nó até um estado terminal.
        """
        state = deepcopy(self.game_state)
        while not state.is_game_over():  # Supõe que há um método para verificar se o jogo acabou
            possible_moves = state.get_legal_moves()
            move = random.choice(possible_moves)
            state = state.make_move(move)
        return state.get_result()  # Supõe que há um método para obter o resultado do jogo

    def backpropagate(self, result):
        """
        Propaga o resultado de uma simulação de volta até a raiz.
        """
        self.visits += 1
        if result == self.player_who_moved:
            self.wins += 1
        if self.parent:
            self.parent.backpropagate(result)


    def UCTSelectChild(self):

        return max(self.children, key=lambda child: child.wins / child.visits + math.sqrt(2 * math.log(self.visits) / child.visits))

    def expand(self):
        move = self.untried_moves.pop()
        new_game = deepcopy(self.game)
        new_game.board.move(move[0], move[1])
        child_node = MCTSNode(new_game, move[1], self)
        self.children.append(child_node)
        return child_node

    def update(self, result):
        self.visits += 1
        if result == self.game.board.current_player:
            self.wins += 1
        elif result != 0: #################### 0 -> Draw
            self.wins -= 1

def MCTS(game, iterations=1000):
    root_node = MCTSNode()
    for _ in range(iterations):
        node = root_node
        # Seleção
        while node.untried_moves == [] and node.children != []:
            node = node.UCTSelectChild()

        # Expansão
        if node.untried_moves:
            node = node.expand()

        # Simulação
        result = node.simulate()

        # Retropropagação
        while node is not None:
            node.backpropagate(result)

        return max(root_node.children, key=lambda x: x.visits).move  # Retorna o movimento do filho mais visitado
    

class MCTSPlayer:
    def __init__(self, iterations):
        self.iterations = iterations
    def choose_move(self, game):
        # Assume que `mcts` é uma função que implementa o algoritmo MCTS e retorna o melhor movimento
        return MCTS(game, self.iterations)
    
player_mcts = MCTSPlayer(iterations=1000)  # Definindo o jogador que usa MCTS com 1000 iterações
game = NeutreekoGame(None, player_mcts)'''