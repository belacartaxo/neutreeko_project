import pygame

class Piece:
    def __init__(self, board, piece, player, color, size, space, father):
        # Constructor for the Piece class, initializes the piece's properties.
        self.row = piece[0] # The row position of the piece on the board.
        self.col = piece[1] # The column position of the piece on the board.
        self.color = color  # The color of the piece, used for drawing.
        self.radius = size // 2 - 2 # Calculates the radius of the piece for drawing.
        # Calculates the x-coordinate for drawing the piece, centered in its cell, adjusted by 'space'.
        self.x = self.col * size + size / 2 +space
        # Calculates the y-coordinate for drawing the piece, similarly centered and adjusted.
        self.y = self.row * size + size / 2 + space
        # Calls a method from the 'board' object to determine the piece's possible moves.
        self.piece_moves = board.piece_move(piece, player)
        self.father = (father)  # Stores a reference to the parent object, possibly for back-reference.

    def __str__(self):
        # Defines the string representation of the Piece object, which shows its row and column.
        return f'({self.row}, {self.col})'

    def draw(self, screen):
        # Draws the piece on a Pygame screen as a circle with the defined properties.
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def is_clicked(self, pos):
        # Determines if the piece has been clicked based on mouse position.
        # Calculates the squared distance from the piece's center to the mouse click position.
        distance_squared = (pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2
        # Returns True if the click is within the radius of the piece, indicating a hit.
        return distance_squared <= self.radius ** 2
