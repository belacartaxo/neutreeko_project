from copy import deepcopy
import math
import random

class MCTSNode:
    def __init__(self, game, node, parent=None):
        self.game = deepcopy(game)
        self.node = node
        self.parent = parent
        self.children = [] #conforme os nos forem analisados vai saindo daqui self.untried_moves e vai para o novo estado
        self.wins = 0
        self.visits = 0
        self.untried_moves = game.board.available_moves() # game.board.available_moves

    def UCTSelectChild(self):
        '''
        Utiliza a fórmula UCT (Upper Confidence Bound 1 applied to trees) para selecionar um dos filhos para exploração. Escolhe o filho com o valor UCT mais alto, que equilibra a exploração de novos movimentos com a explotação de movimentos conhecidos por serem bons. A fórmula leva em consideração tanto as vitórias relativas do filho quanto a raiz quadrada do logaritmo das visitas do pai dividido pelo número de visitas ao filho, promovendo um equilíbrio entre exploração e explotação.
        '''
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
        elif result != 'Draw':
            self.wins -= 1

def MCTS(root, iterations=1000):
    for _ in range(iterations):
        node = root
        game = deepcopy(root.game)

        # Seleção
        while node.untried_moves == [] and node.children != []:
            node = node.UCTSelectChild()
            game.board.move(node.father, node.node)

        # Expansão
        if node.untried_moves != []:
            node = node.expand()

        # Simulação
        while game.board.update_winner() == -1:
            move = random.choice(game.board.get_valid_moves())
            game.move(move[0], move[1])

        # Retropropagação
        while node is not None:
            node.update(game.update_winner())
            node = node.parent