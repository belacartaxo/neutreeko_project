import random
import pygame
import sys
import os
from .board import Board
from .piece import Piece
from ai.heuristics import *
from ai.min_max_alpha_beta import *

'''
COMO FAZ PARA COLOCAR OS JOGADORES ATUAIS, ESTÁ UM TEXTO FICANDO POR CIMA DO OUTRO

'''

# --------- Graph ----------#
SIZE =  5
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
RED = (180,0, 0)
GREEN = (78,255,93)
GREEN_1 = (88, 154, 141) 
GREEN_2 = (143, 193, 181)
GREEN_3 = (23,101,81)
CELL_SIZE = 100
BOARD_EDGE = 10
BOARD_SIZE = SIZE * CELL_SIZE
SPACE_SCREEN_BOARD = 100
SCREEN_SIZE = BOARD_SIZE + SPACE_SCREEN_BOARD
WIDTH_BUTTON = 250
HEIGHT_BUTTON = 80
WIDTH_SMALL_BUTTON = 100
HEIGHT_SMALL_BUTTON = 40
WIDTH_PLAYER_BUTTON = 190
HEIGHT_PLAYER_BUTTON = 60
WIDTH_BOX = 300
HEIGHT_BOX = 100
TIME = 0
PIECE_COLORS = (BLACK, WHITE)
FONT_PATH1 = os.path.join("assets", "font", "Bungee_Poppins", "Bungee", "Bungee-Regular.ttf")
FONT_PATH2 = os.path.join("assets", "font", "Bungee_Poppins", "Poppins", "Poppins-Regular.ttf")

#ia parameters
AI = execute_minimax_alpha_beta_move
EASY = evaluate_f1
MEDIUM = evaluate_f2
HARD = evaluate_f3
DEPTH = 3

class NeutreekoGame:
    def __init__(self):
        self.initial_position = [(4, 1),(1, 2), (4, 3)], [(0,1), (3, 2), (0,3)]
        self.board = Board(self.initial_position)
        self.player =[False, False]
        self.home_screen = True
        self.rules_screen = False
        self.info_screen = False
        self.board_screen = False
        self.choose_player_screen = False
        self.screen_update = False
        self.mouse_over_button = False
        self.game_pieces = [[], []]
        self.players_moved = False
        self.available_pieces = []

    def create_board_surface(self, screen):
        pygame.draw.rect(screen, BLACK, (SPACE_SCREEN_BOARD/2-BOARD_EDGE,SPACE_SCREEN_BOARD/2-BOARD_EDGE, BOARD_SIZE+BOARD_EDGE*2, BOARD_SIZE+BOARD_EDGE*2))
        for row in range(SIZE):
            for col in range(SIZE):
                color =  GREEN_1 if (row + col) % 2 == 0 else GREEN_2
                pygame.draw.rect(screen, color, (SPACE_SCREEN_BOARD/2+col * CELL_SIZE, SPACE_SCREEN_BOARD/2+row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def create_piece_surface(self, pieces, screen, clicked_piece):
        for i in range(len(pieces)):
            if len(self.game_pieces[i]) == 0:
                self.game_pieces[i] = [self.create_piece(p, i+1, PIECE_COLORS[i], screen) for p in pieces[i]]
            else:
                self.draw_piece(self.game_pieces[i], screen)
                      
        if clicked_piece:
            self.available_pieces = [self.create_piece(p, self.board.current_player, GREEN, screen, clicked_piece) for p in clicked_piece.piece_moves]
            return
        
        if len(self.available_pieces) > 0:
            self.draw_piece(self.available_pieces, screen)

    def draw_piece(self, pieces, screen):
        for p in pieces:
            p.draw(screen)
    
    def create_piece(self, piece, player, color, screen, father = None):
        piece = Piece(self.board, piece, player, color, CELL_SIZE, SPACE_SCREEN_BOARD/2, father)
        piece.draw(screen)
        return piece
            
    def update_board_screen(self, screen, clicked_piece = None):
        self.update_home_screen(screen)
        self.create_board_surface(screen)
        self.create_piece_surface(self.board.pieces, screen, clicked_piece)
        pygame.display.flip()

    def update_home_screen(self, screen):
        pygame.draw.rect(screen, GREEN_1, (0, 0, SCREEN_SIZE, SCREEN_SIZE))
    
    def update_rules_screen(self, screen, font1, font2, font3, color, back_button):
        pygame.draw.rect(screen, GREEN_1, (0, 0, SCREEN_SIZE, SCREEN_SIZE))
        pygame.draw.rect(screen, GREEN_3, (50, 110, 500, 380), border_radius=20)
        pygame.display.flip()
        self.create_text(screen, "Rules", font1, WHITE, 30)
        self.create_text(screen, "Black pieces always start.", font2, WHITE, 140)
        self.create_text(screen, "Move vertically, horizontally, or diagonally", font2, WHITE, 200)
        self.create_text(screen, "to the last open spot on the board.", font2, WHITE, 225)
        self.create_text(screen, "A draw occurs if the same board", font2, WHITE, 300)
        self.create_text(screen, "configuration repeats 3 times.", font2, WHITE, 325)
        self.create_text(screen, "Win by aligning your 3 pieces in a row,", font2, WHITE, 400)
        self.create_text(screen, "either vertically, horizontally, or diagonally.", font2, WHITE, 425)
        self.draw_button(screen, 'Back', font3, GREEN_3, back_button,(back_button.x+WIDTH_SMALL_BUTTON/2, back_button.y-HEIGHT_BUTTON/4))
        self.rules_screen = True

    def update_obs_screen(self, screen, font1, font2, font3, color, back_button):
        pygame.draw.rect(screen, GREEN_1, (0, 0, SCREEN_SIZE, SCREEN_SIZE))
        pygame.draw.rect(screen, GREEN_3, (50, 110, 500, 380), border_radius=20)
        pygame.display.flip()
        self.create_text(screen, "Information", font1, WHITE, 30)
        self.create_text(screen, "Developed by the following FCUP students:", font2, WHITE, 140)
        self.create_text(screen, "Isabela Britto Cartaxo", font2, WHITE, 175)
        self.create_text(screen, "Rafael Arruda Costa", font2, WHITE, 200)
        self.create_text(screen, "Sérgio Barbosa Marques", font2, WHITE, 225)
        self.create_text(screen, "This work is an implementation of", font2, WHITE, 285)
        self.create_text(screen, "Jan Kristian Haugland's game:", font2, WHITE, 310)
        self.create_text(screen, "Neutreeko", font2, WHITE, 335)
        self.create_text(screen, "Code and strategies were based on:", font2, WHITE, 380)
        self.create_text(screen, "Professor Luis Paulo Reis’s classes", font2, WHITE, 405)
        self.create_text(screen, "OpenAI's chatGPT prompts", font2, WHITE, 430)
        self.draw_button(screen, 'Back', font3, GREEN_3, back_button,(back_button.x+WIDTH_SMALL_BUTTON/2, back_button.y-HEIGHT_BUTTON/4))
        self.info_screen = True

    def check_click(self, screen, pos):
        for piece in self.game_pieces[self.board.current_player-1]:
            if piece.is_clicked(pos):
                self.update_board_screen(screen, piece) 
                return
    
        for piece in self.available_pieces:
            if piece.is_clicked(pos):
                self.board = self.board.move((piece.father.row, piece.father.col), (piece.row, piece.col))
                self.available_pieces = []
                self.game_pieces = [[],[]]
                self.players_moved = True
                return

        
    def run_game(self):
        self.board = Board(self.initial_position)
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Neutreeko")

        font_1 = pygame.font.Font(FONT_PATH1, 30)
        font_2 = pygame.font.Font(FONT_PATH1, 60)
        font_3 = pygame.font.Font(FONT_PATH2, 18)
        font_4 = pygame.font.Font(FONT_PATH1, 18)
        font_5 = pygame.font.Font(FONT_PATH1, 23)

        start_button_rect = pygame.Rect((SCREEN_SIZE - WIDTH_BUTTON)/2, 200, WIDTH_BUTTON, HEIGHT_BUTTON)
        rules_button_rect = pygame.Rect((SCREEN_SIZE - WIDTH_BUTTON)/2, 300, WIDTH_BUTTON, HEIGHT_BUTTON)
        obs_button_rect = pygame.Rect((SCREEN_SIZE - WIDTH_BUTTON)/2, 400, WIDTH_BUTTON, HEIGHT_BUTTON)
        back_button_rect = pygame.Rect((SCREEN_SIZE - WIDTH_SMALL_BUTTON)/2, SCREEN_SIZE-80, WIDTH_SMALL_BUTTON, HEIGHT_SMALL_BUTTON)
        home_buttons = [start_button_rect, rules_button_rect, obs_button_rect]
        home_buttons_text = ["Start Game", "Rules", "Information"]
        # player 1 buttons
        human_player_button1 = pygame.Rect((SCREEN_SIZE - WIDTH_PLAYER_BUTTON)/4 - 20, 150, WIDTH_PLAYER_BUTTON, HEIGHT_PLAYER_BUTTON)
        easy_button1 = pygame.Rect((SCREEN_SIZE - WIDTH_PLAYER_BUTTON)/4 - 20, 250, WIDTH_PLAYER_BUTTON, HEIGHT_PLAYER_BUTTON)
        medium_button1 = pygame.Rect((SCREEN_SIZE - WIDTH_PLAYER_BUTTON)/4 - 20, 350, WIDTH_PLAYER_BUTTON, HEIGHT_PLAYER_BUTTON)
        hard_button1 = pygame.Rect((SCREEN_SIZE - WIDTH_PLAYER_BUTTON)/4 - 20, 450, WIDTH_PLAYER_BUTTON, HEIGHT_PLAYER_BUTTON)
        # player 2 buttons
        human_player_button2 = pygame.Rect(3*(SCREEN_SIZE - WIDTH_PLAYER_BUTTON)/4 + 20, 150, WIDTH_PLAYER_BUTTON, HEIGHT_PLAYER_BUTTON)
        easy_button2 = pygame.Rect(3*(SCREEN_SIZE - WIDTH_PLAYER_BUTTON)/4 + 20, 250, WIDTH_PLAYER_BUTTON, HEIGHT_PLAYER_BUTTON)
        medium_button2 = pygame.Rect(3*(SCREEN_SIZE - WIDTH_PLAYER_BUTTON)/4 + 20, 350, WIDTH_PLAYER_BUTTON, HEIGHT_PLAYER_BUTTON)
        hard_button2 = pygame.Rect(3*(SCREEN_SIZE - WIDTH_PLAYER_BUTTON)/4 + 20, 450, WIDTH_PLAYER_BUTTON, HEIGHT_PLAYER_BUTTON)

        players_buttons = [human_player_button1, easy_button1, medium_button1, hard_button1, human_player_button2, easy_button2, medium_button2, hard_button2]
        players_buttons_text = ["Human", "AI - Easy", "AI - Medium", "AI - Hard", "Human", "AI - Easy", "AI - Medium", "AI - Hard"]
        ai = [None, EASY, MEDIUM, HARD, None, EASY, MEDIUM, HARD]
        continue_button_rect = pygame.Rect((SCREEN_SIZE - WIDTH_SMALL_BUTTON)/2, SCREEN_SIZE-70, WIDTH_SMALL_BUTTON, HEIGHT_SMALL_BUTTON)


        while True: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:   
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #clique no botâo de iniciar
                    if self.home_screen and start_button_rect.collidepoint(event.pos):
                        self.home_screen = False
                        self.choose_player_screen = True
                        self.screen_update = False

                        '''self.home_screen = False
                        self.board_screen = True
                        self.update_board_screen(screen)
                        self.create_text(screen, f"Current player: {self.board.current_player}", font_4, WHITE, 20)'''

                    #clique nas peças para pegas as jogadas
                    elif self.board_screen and self.player[self.board.current_player-1] is None:
                        mouse_pos = pygame.mouse.get_pos()
                        self.check_click(screen, mouse_pos)

                    #clique no botão rules
                    elif self.home_screen and rules_button_rect.collidepoint(event.pos):
                        self.home_screen = False
                        self.rules_screen = True
                        self.update_rules_screen(screen, font_2, font_3, font_4, GREEN_3, back_button_rect)
                        self.screen_update = False

                    elif self.home_screen and obs_button_rect.collidepoint(event.pos):
                        self.home_screen = False
                        self.info_screen = True
                        self.update_obs_screen(screen, font_2, font_3, font_4, GREEN_3, back_button_rect)
                        self.screen_update = False

                    elif self.rules_screen or self.info_screen and back_button_rect.collidepoint(event.pos):
                        self.home_screen = True
                        self.info_screen = False
                        self.rules_screen = False
                    elif self.choose_player_screen:
                        for i in range(len(players_buttons)):
                            if players_buttons[i].collidepoint(event.pos):
                                if i < 4:
                                    for n in range(4):
                                        self.draw_button(screen, players_buttons_text[n], font_5, GREEN_3, players_buttons[n],(players_buttons[n].x + WIDTH_PLAYER_BUTTON/2, players_buttons[n].y-10))
                                    print("111")

                                    self.player[0] = AI(ai[i], DEPTH) if ai[i] != None else None

                                    self.draw_button(screen, players_buttons_text[i], font_5, GREEN_2, players_buttons[i],(players_buttons[i].x + WIDTH_PLAYER_BUTTON/2, players_buttons[i].y-10))
                                else:
                                    print("222")
                                    for n in range(4, len(players_buttons)):
                                        self.draw_button(screen, players_buttons_text[n], font_5, GREEN_3, players_buttons[n],(players_buttons[n].x + WIDTH_PLAYER_BUTTON/2, players_buttons[n].y-10))
                                    self.draw_button(screen, players_buttons_text[i], font_5, GREEN_2, players_buttons[i],(players_buttons[i].x + WIDTH_PLAYER_BUTTON/2, players_buttons[i].y-10))
                                    self.player[1] = AI(ai[i], DEPTH) if ai[i] != None else None
                        if continue_button_rect.collidepoint(event.pos):
                            if self.player[0] != False and self.player[1] != False:
                                self.choose_player_screen = False
                                self.board_screen = True
                                self.update_board_screen(screen)
                                self.create_text(screen, f"Current player: {self.board.current_player}", font_4, WHITE, 20)
                            else:
                                self.create_text(screen, "Choose both players", font_4, RED, 120)



                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.home_screen:
                        for i in range(len(home_buttons)):
                            # Verifica se o mouse está dentro das dimensões do botão
                            if home_buttons[i].left <= mouse_pos[0] <= home_buttons[i].right and home_buttons[i].top <= mouse_pos[1] <= home_buttons[i].bottom:
                                self.draw_button(screen, home_buttons_text[i], font_1, GREEN_2, home_buttons[i],(SCREEN_SIZE/2, home_buttons[i].y))
                            else:
                                self.draw_button(screen, home_buttons_text[i], font_1, GREEN_3, home_buttons[i],(SCREEN_SIZE/2, home_buttons[i].y))

                    if self.rules_screen or self.info_screen:
                        if back_button_rect.left <= mouse_pos[0] <= back_button_rect.right and back_button_rect.top <= mouse_pos[1] <= back_button_rect.bottom:
                            self.draw_button(screen, "Back", font_4, GREEN_2, back_button_rect,(back_button_rect.x+WIDTH_SMALL_BUTTON/2, back_button_rect.y-HEIGHT_BUTTON/4))
                        else:
                            self.draw_button(screen, "Back", font_4, GREEN_3, back_button_rect,(back_button_rect.x+WIDTH_SMALL_BUTTON/2, back_button_rect.y-HEIGHT_BUTTON/4))

                    if self.choose_player_screen:
                        if continue_button_rect.left <= mouse_pos[0] <= back_button_rect.right and back_button_rect.top <= mouse_pos[1] <= back_button_rect.bottom:
                            self.draw_button(screen, 'Continue', font_3, GREEN_2, continue_button_rect,(continue_button_rect.x+WIDTH_SMALL_BUTTON/2, continue_button_rect.y-HEIGHT_BUTTON/4))
                        else:
                            self.draw_button(screen, 'Continue', font_3, GREEN_3, continue_button_rect,(continue_button_rect.x+WIDTH_SMALL_BUTTON/2, continue_button_rect.y-HEIGHT_BUTTON/4))

                              
            #jogo acontecendo
            if self.board_screen:
                if self.player[self.board.current_player-1] and not(self.players_moved):

                    if self.board.current_player == 1:
                        self.player[0](self)
                    else:
                        self.player[1](self)  

                    self.game_pieces = [[],[]] 
                    pygame.time.wait(TIME)
                    self.players_moved = True
                    
                    #pygame.draw.rect(screen, GREEN_1, (0, 0, SCREEN_SIZE, SCREEN_SIZE))
                
                if self.players_moved: 
                    self.update_board_screen(screen)
                    if self.board.winner != -1:
                        text = f"Player {self.board.winner} wins!" if self.board.winner != 0 else "Draw!"
                        self.create_text(screen, text, font_1, WHITE, (SCREEN_SIZE - HEIGHT_BOX )/2, (SCREEN_SIZE - WIDTH_BOX)/2, True)
                        pygame.time.wait(2000)
                        self.update_board_screen(screen)
                        pygame.quit()
                        return  
                    rect = pygame.Rect(180, 10, 250, 30)
                    screen.fill((GREEN_1), rect)
                    pygame.display.flip()
                    self.create_text(screen, f"Current player: {self.board.current_player}", font_4, WHITE, 20)
                    self.players_moved = False

            if self.choose_player_screen and not self.screen_update:
                self.update_home_screen(screen)
                self.create_text(screen, "Player 1", font_1, WHITE, 80, SCREEN_SIZE/4-WIDTH_PLAYER_BUTTON/4)
                self.create_text(screen, "Player 2", font_1, WHITE, 80, 3*SCREEN_SIZE/4-WIDTH_PLAYER_BUTTON/2-10)
                for i in range(len(players_buttons)):
                    self.draw_button(screen, players_buttons_text[i], font_5, GREEN_3, players_buttons[i],(players_buttons[i].x + WIDTH_PLAYER_BUTTON/2, players_buttons[i].y-10))
                self.screen_update = True
                self.draw_button(screen, 'Continue', font_3, GREEN_3, continue_button_rect,(continue_button_rect.x+WIDTH_SMALL_BUTTON/2, continue_button_rect.y-HEIGHT_BUTTON/4))
            
            if self.home_screen and not self.screen_update:
                self.update_home_screen(screen)
                self.create_text(screen, "NEUTREEKO", font_2, WHITE, 100)
                for i in range(len(home_buttons)):
                    self.draw_button(screen, home_buttons_text[i], font_1, GREEN_3, home_buttons[i],(SCREEN_SIZE/2, home_buttons[i].y))
                self.screen_update = True

    def create_text(self, screen, text, font, color_text, position_y, position_x = None, box=False):
        #text_rect = text_surface.get_rect()
        text_surface = font.render(text, True, color_text)
        text_width, text_height = text_surface.get_size()
        if box:
            text_rect = pygame.Rect(position_x, position_y, WIDTH_BOX, HEIGHT_BOX)
            pygame.draw.rect(screen, BLACK, text_rect)
            screen.blit(text_surface, ((SCREEN_SIZE - text_width)/2, (SCREEN_SIZE - text_height )/2))
        else:
            if not position_x: position_x = (SCREEN_SIZE - text_width)/2
            screen.blit(text_surface, (position_x, position_y))
        pygame.display.flip()

    def draw_button(self, screen, text, font, color, button_rect, position):   
        pygame.draw.rect(screen, color, button_rect, 0, 10)
        button_surface = font.render(text, True, WHITE)
        text_width, text_height = button_surface.get_size()
        screen.blit(button_surface, (position[0]-text_width/2, position[1]+ (HEIGHT_BUTTON - text_height)/2))
        pygame.display.flip()

def execute_random_move(game):
    new_pieces = random.choice(game.board.available_moves())
    game.board = game.board.move(new_pieces[0], new_pieces[1])

