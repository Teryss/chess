import os
import pygame
from base_func import Square_to_position, Compare_pieces_colour, Position_to_square


class Board():
    def __init__(self, start_position, width, height, screen, side_on_top = 'W'):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.screen = screen
        self.height = height
        self.width = width
        self.sqr_size = width // 8
        self.movesGenerator = None
        self.sq1 = None
        self.movesCounter = 0

        self.colors = {
            'white': (255, 255, 255),
            'black': (181, 101, 29),
            'red': (255, 0, 0),
            'blue': (105, 236, 144),
            'green': (0, 202, 20),
            'yellow': (255, 233, 0),
        }
        self.imgs = {
            'r': pygame.image.load(r"{}\{}\{}.png".format(self.path, 'White', 'r')),
            'R': pygame.image.load(r"{}\{}\{}.png".format(self.path, 'Black', 'R')),
            'b': pygame.image.load(r"{}\{}\{}.png".format(self.path, 'White', 'b')),
            'B': pygame.image.load(r"{}\{}\{}.png".format(self.path, 'Black', 'B')),
            'n': pygame.image.load(r"{}\{}\{}.png".format(self.path, 'White', 'n')),
            'N': pygame.image.load(r"{}\{}\{}.png".format(self.path, 'Black', 'N')),
            'q': pygame.image.load(r"{}\{}\{}.png".format(self.path, 'White', 'q')),
            'Q': pygame.image.load(r"{}\{}\{}.png".format(self.path, 'Black', 'Q')),
            'p': pygame.image.load(r"{}\{}\{}.png".format(self.path, 'White', 'p')),
            'P': pygame.image.load(r"{}\{}\{}.png".format(self.path, 'Black', 'P')),
            'k': pygame.image.load(r"{}\{}\{}.png".format(self.path, 'White', 'k')),
            'K': pygame.image.load(r"{}\{}\{}.png".format(self.path, 'Black', 'K')),
        }
        self.pieces = [''] * 64
        # CONTENT IN ORDER: piece_type, path_to_img, position_x, position_y
        self.checked_square = -10
        self.drawPromotion = False
        self.selectedPiece = -10

        # INIT THE STARTING POSITION
        self.startPos = start_position
        id = 0
        for piece in self.startPos:
                if piece != '/':
                    if piece.isdigit():
                        id += int(piece)
                    else:
                        self.pieces[id] = [
                                    piece,
                                    self.imgs[piece],
                                    Square_to_position(id, self.sqr_size)]
                        id += 1

    def Draw_Board(self):
        self.screen.fill(self.colors['black'])
        for y in range(0, self.height, self.sqr_size):
            for x in range(0, self.width, self.sqr_size*2):
                if y % int(self.width/4) != 0:
                    pygame.draw.rect(self.screen, self.colors['white'], (x + self.sqr_size, y, self.sqr_size, self.sqr_size))
                else:
                    pygame.draw.rect(self.screen, self.colors['white'], (x, y, self.sqr_size, self.sqr_size))

        # HIGHLIGHT CHECK SQUARE
        if self.checked_square != -10:
            x, y = Square_to_position(self.checked_square, self.sqr_size)
            pygame.draw.rect(self.screen, self.colors['red'], (x, y, self.sqr_size, self.sqr_size))

        # HIGHLIGHT SELECTED PIECE
        if self.selectedPiece != -10:
            x, y = Square_to_position(self.selectedPiece, self.sqr_size)
            pygame.draw.rect(self.screen, self.colors['blue'], (x, y, self.sqr_size, self.sqr_size))

    def Draw_Pieces(self):
        for piece in self.pieces:
            if(piece != ''):
                self.screen.blit(
                    pygame.transform.scale(piece[1], (self.sqr_size,self.sqr_size)),
                    Square_to_position(self.pieces.index(piece), self.sqr_size)
                    )

    def Draw_Legal_Moves(self):
        if self.sq1 is not None:
            moves = self.movesGenerator.getMoves()
            for piece_moves in moves:
                if(piece_moves[0] == self.sq1):
                    for move in piece_moves[1]:
                        if self.pieces[move] != '':
                            x,y =Square_to_position(move, self.sqr_size)
                            pygame.draw.rect(self.screen, self.colors['yellow'], (x,y , self.sqr_size, self.sqr_size))
                        else:
                            x,y = Square_to_position(move, self.sqr_size)
                            pygame.draw.circle(self.screen, self.colors['yellow'], (x + 25, y + 25), 10)

    def Pawn_promotion(self):
        squares_to_check = [x for x in range(0,8)] + [x for x in range(56,64)] 
        
        for i in squares_to_check:
            if self.pieces[i] != '':
                if self.pieces[i][0] == 'p' or self.pieces[i][0] == 'P':
                    black = False if self.pieces[i][0] == 'p' else True
                    pawn_type = self.pieces[i][0]
                    pygame.draw.rect(self.screen, (150,50,50), (self.sqr_size * 2, self.sqr_size * 4, self.sqr_size * 4, self.sqr_size * 1))
                    self.screen.blit(pygame.transform.scale(self.imgs['Q' if black else 'q'], (self.sqr_size,self.sqr_size)), (self.sqr_size * 2, self.sqr_size * 4))
                    self.screen.blit(pygame.transform.scale(self.imgs['B' if black else 'b'], (self.sqr_size,self.sqr_size)), (self.sqr_size * 3, self.sqr_size * 4))
                    self.screen.blit(pygame.transform.scale(self.imgs['N' if black else 'n'], (self.sqr_size,self.sqr_size)), (self.sqr_size * 4, self.sqr_size * 4))
                    self.screen.blit(pygame.transform.scale(self.imgs['R' if black else 'r'], (self.sqr_size,self.sqr_size)), (self.sqr_size * 5, self.sqr_size * 4))
                    pygame.display.update()
                    sqr = 0
                    while sqr == 0:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                sqr = Position_to_square(pygame.mouse.get_pos())
                                if sqr == 34:
                                    piece_type = 'Q' if black else 'q'
                                elif sqr == 35:
                                    piece_type = 'B' if black else 'b'
                                elif sqr == 36:
                                    piece_type = 'N' if black else 'n'
                                elif sqr == 37:
                                    piece_type = 'R' if black else 'r'
                                else:
                                    sqr = 0
                                    break
                                if pawn_type.isupper():
                                    piece_type = piece_type.upper()

                                self.pieces[i] = [
                                    piece_type,
                                    self.imgs[piece_type],
                                    self.pieces[i][2]
                                ]
    def moveHandler(self, sqr):
        if self.sq1 is None:
            if self.pieces[sqr] != '':
                piece_type = self.pieces[sqr][0]
                if piece_type.islower() and self.movesCounter % 2 == 0 or piece_type.isupper() and self.movesCounter % 2 == 1:
                    self.sq1 = sqr
                    self.Set_clicked_piece(sqr)
        else:
            if sqr == self.sq1:
                self.Reset_clicked_piece()
                self.sq1 = None
            elif self.pieces[sqr] == '' or self.Are_pieces_diff_color((sqr, self.sq1)):
                if self.movesGenerator is not None:
                    if self.movesGenerator.CheckIfMoveIsInGeneratedMoves(self.sq1, sqr):
                        sq1 = self.sq1
                        self.Make_a_move((self.sq1, sqr))
                        return sq1, sqr
                else:
                    print("Pointer of move generation obj not imported to board obj")
            else:
                if self.pieces[sqr] != '':
                    piece_type = self.pieces[sqr][0]
                    if piece_type.islower() and self.movesCounter % 2 == 0 or piece_type.isupper() and self.movesCounter % 2 == 1:
                        self.sq1 = sqr
                        self.Set_clicked_piece(sqr)
                else:
                    self.sq1 = None
        return None

    def importMoveGenerationObj(self, obj):
        self.movesGenerator = obj

    def Make_a_move(self, sqrs):
        self.pieces[sqrs[1]] = self.pieces[sqrs[0]]
        self.pieces[sqrs[0]] = ''
        self.movesCounter += 1
        self.sq1 = None
        self.Reset_clicked_piece()
    
    def Check_square(self, square):
        if self.pieces[square] == '':
            return 'Empty'
        elif self.pieces[square][0].isupper():
            return 'Black'
        return 'White'

    def Are_pieces_diff_color(self, sqrs):
        return Compare_pieces_colour(sqrs[0], sqrs[1], self.pieces)

    def Get_pos(self):
        return self.pieces
    
    def Change_checked_king_square(self,sqr):
        self.checked_square = sqr

    def Set_clicked_piece(self, id):
        self.selectedPiece = id

    def Reset_clicked_piece(self):
        self.selectedPiece = -10