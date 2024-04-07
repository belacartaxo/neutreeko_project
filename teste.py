import pygame
import sys

# Inicialize o Pygame
pygame.init()

# Defina as dimensões da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Tabuleiro")

# Defina cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Classe para representar as peças
class Piece:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# Crie algumas peças de exemplo
piece1 = Piece(100, 100, 50, 50, WHITE)
piece2 = Piece(200, 200, 50, 50, WHITE)

# Lista de todas as peças
pieces = [piece1, piece2]

# Função para verificar cliques nas peças
def check_click(pos):
    for piece in pieces:
        if piece.rect.collidepoint(pos):
            # Faça alguma coisa quando uma peça for clicada
            print("Peça clicada!")
            break

# Loop principal do jogo
running = True
while running:
    screen.fill(BLACK)

    # Desenhe as peças
    for piece in pieces:
        piece.draw(screen)

    # Verifique eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Verifique se foi um clique do botão esquerdo
                mouse_pos = pygame.mouse.get_pos()
                check_click(mouse_pos)

    pygame.display.flip()

# Encerre o Pygame
pygame.quit()
sys.exit()
