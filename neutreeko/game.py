import random
import pygame
import sys
from .board import Board
from .piece import Piece

# --------- Graph ----------#
SIZE =  5
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
GREEN = (78,255,93)
BLUE_1 = (88, 154, 141) 
BLUE_2 = (143, 193, 181)
CELL_SIZE = 100
BOARD_SIZE = SIZE * CELL_SIZE
WIDTH_BUTTON = 300
HEIGHT_BUTTON = 100
TIME = 300
PIECE_COLORS = (BLACK, WHITE)
# --------- Graph ----------#

class NeutreekoGame:
    def __init__(self, ai1 = None, ai2 = None):
        # Initial positions for player 1 and player 2
        self.initial_position = [(4, 1),(1, 2), (4, 3)], [(0,1), (3, 2), (0,3)]
        # Create a new board with the initial positions
        self.board = Board(self.initial_position)
        # Player 1 and Player 2 functions to control their moves
        self.player =[ ai1, ai2]
        # Flags to control the game flow
        self.button_clicked = False
        self.screen_update = False
        self.mouse_over_button = False
        self.game_pieces = [[], []]
        self.players_moved = False
        self.available_pieces = []
        
    def create_board_surface(self, screen):
        # Create the game board surface
        for row in range(SIZE):
            for col in range(SIZE):
                color =  BLUE_1 if (row + col) % 2 == 0 else BLUE_2 # Determine the color of the current cell
                pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))  #Draw a rectangle representing the current cell on the screen

    def create_piece_surface(self, pieces, screen):
        for i in range(len(pieces)):
            self.game_pieces[i].clear()
            for p in pieces[i]: # Pieces player 1
                self.game_pieces[i].append(self.create_piece(p, PIECE_COLORS[i], screen))
        
        if len(self.available_pieces) > 0:
            for p in self.available_pieces:
                self.create_piece(p, GREEN, screen)
    
    def create_piece(self, piece, color, screen):
        piece = Piece(self.board, piece, color, CELL_SIZE)
        piece.draw(screen)
        return piece
            
    def update_screen(self, screen):
        # Update the game screen with the board and pieces
        self.create_board_surface(screen)
        self.create_piece_surface(self.board.pieces, screen)
        pygame.display.flip()
    
    def check_click(self, screen, pos):
        for piece in self.game_pieces[self.board.current_player-1]:
            if piece.is_clicked(pos):
                self.available_pieces = piece.piece_moves
                self.update_screen(screen) #
                break
               

        
    def run_game(self):
        # Initialize the game board
        self.board = Board(self.initial_position)

        # GRAPH
        pygame.init()# Initialize Pygame
        screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))# Set up the game screen 
        pygame.display.set_caption("Neutreeko")# Set the title of the game window
        font = pygame.font.SysFont("Arial", 50) # Create a font object for rendering text in the game
        button_rect = pygame.Rect(100, 200, WIDTH_BUTTON, HEIGHT_BUTTON)# Create a rectangle representing the button

        # Enter a loop to continuously handle Pygame events
        while True: 
            for event in pygame.event.get(): # Iterate through all Pygame events
                if event.type == pygame.QUIT:   # Check if the user clicked the close button
                    pygame.quit() # Quit Pygame
                    sys.exit() # Exit the Python program
                elif event.type == pygame.MOUSEBUTTONDOWN:# Check if the user clicked the mouse button
                    if not self.button_clicked and button_rect.collidepoint(event.pos):  # Check if the game button hasn't been clicked yet and if the mouse click occurGREEN within the button rectangle
                        self.button_clicked = True # Set the button_clicked flag to True
                        self.update_screen(screen)# Update the screen to reflect the button click
                    elif self.button_clicked and self.player[self.board.current_player-1] is None:  # Check if current player is human
                    # Process human player's click
                        mouse_pos = pygame.mouse.get_pos()
                        self.check_click(screen, mouse_pos)

            if self.button_clicked:
                # Execute player moves
                if self.player[self.board.current_player-1]: # se o jogador for uma ia
                    if self.board.current_player == 1:
                        self.player[0](self)
                    else:
                        self.player[1](self)   
                    pygame.time.wait(TIME) # wait a few seconds so we can view the moves
                    self.players_moved = True
                self.update_screen(screen) # updates the screen after each movement
                
                # Check the winner
                if self.players_moved: 
                    if self.board.winner != -1:
                        text = f"Player {self.board.winner} wins!" if self.board.winner != 0 else "Draw!" # Determine the message to be displayed based on the winner
                        text_surface = font.render(text, True, BLACK)  # Render the text onto a surface
                        text_rect = self.create_text(screen, font, text)   # Create a rectangle to position the text in the center of the screen
                        screen.blit(text_surface, text_rect) # Blit the rendeGREEN text surface onto the screen
                        pygame.display.flip()   # Update the display 
                        pygame.time.wait(2000) # Pause the game so we can see the result
                        pygame.quit() # Quit Pygame
                        return  # Exit the function, ending the game
                    # Switch player turn
                    self.players_moved = False
                    self.board.current_player = 3 - self.board.current_player
            
            # If the screen has not been updated yet
            if not self.screen_update:
                self.update_screen(screen) # Update the screen with the game board and pieces
                self.draw_button(screen, font, button_rect)  # Draw the start game button on the screen
                self.screen_update = True # Set the screen_update flag to True to indicate that the screen has been updated

        
    def create_text(self, screen, font, text):
        # Create a text surface
        result_box = pygame.Rect(100, 200, 300, 100) # Define a rectangle
        pygame.draw.rect(screen, WHITE, result_box) # Draw a rectangle on the screen using the defined rectangle
        text = font.render(text, True, WHITE) # Render the text onto a surface
        return text.get_rect(center=result_box.center) # Return a rectangle that centers the rendeGREEN text within the previously defined rectangle
    
    def draw_button(self, screen, font, button_rect):   
            # Draw the start game button         
            pygame.draw.rect(screen, BLACK, button_rect) # Draw a rectangle representing the button on the scree
            button_text = font.render("Start  Game", True, WHITE) # Render the text "Start Game" onto a surface
            screen.blit(button_text, (140, 220)) # Blit the rendeGREEN text surface onto the screen
            pygame.display.flip()# Update the display

def execute_random_move(game):
    # Select a random move among the available moves in the game
    new_pieces = random.choice(game.board.available_moves())
    # Execute the selected move on the game board
    game.board.move(new_pieces[0], new_pieces[1])
