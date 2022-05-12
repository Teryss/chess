#### PIECE MOVEMENT WORKS, PROBLEM WITH CHECKS ####
import pygame
import os
path = os.path.dirname(os.path.abspath(__file__))
# BASIC VARIABLES
width, height = 400, 400
white = (255, 255, 255)
black = (181, 101, 29)
running = True
row, col = 8, 8
sqr_size = int(width/8)
fps = 30
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess board")
startPossition = "rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR"
pieces_on_board = ['']*64  # CONTENT IN ORDER: type, path_to_img, position_x, position_y
id = 0
pinned_pieces = list()

def Square_to_position(square_id):
    x = square_id % 8 * sqr_size
    y = int(square_id / 8) * sqr_size
    return x, y
def Position_to_square(position):
    return int(position[0] / 50) + 8 * int(position[1]/50)
def Square_to_row_and_column(square_id):
    return int(square_id / 8), int(square_id % 8)
def Row_and_column_to_square(row, column):
    return row * 8 + column
def Check_piece_movement(args,cur_sqr):
    legal_moves = list()
    for i in range(args[0], args[1], args[2]):
        if(i != cur_sqr):
            if(pieces_on_board[i] == ''):
                legal_moves.append(i)
            else:
                if(Compare_pieces_colour(cur_sqr, i)):
                    legal_moves.append(i)
                return legal_moves
    return legal_moves
def Check_piece_diagonal(cur_sqr):
    legal_moves = list()
    row, col = Square_to_row_and_column(cur_sqr)
    diagnals = ((1, 1), (1, -1), (-1, 1), (-1, -1))
    for diagnal in diagnals:
        for i in range(1,9):
            t_row = row + i * diagnal[0]
            t_col = col + i * diagnal[1]
            check_square = Row_and_column_to_square(t_row, t_col)
            f_col = Square_to_row_and_column(check_square)[1]
            if(f_col != t_col): break
            if(0 <= check_square <= 63):
                if(pieces_on_board[check_square] == ''):
                    legal_moves.append(check_square)
                else:
                    if(Compare_pieces_colour(cur_sqr, check_square)):
                        legal_moves.append(check_square)
                    break
    return legal_moves
def DrawBoard(height, width, sqr_size):
    screen.fill(black)
    for y in range(0, height, sqr_size):
        for x in range(0, width, sqr_size*2):
            if(y % int(width/4) != 0):
                pygame.draw.rect(screen, white, (x+sqr_size,y,sqr_size,sqr_size))
            else:
                pygame.draw.rect(screen, white, (x,y,sqr_size,sqr_size))
def DrawPieces():
    for piece in pieces_on_board:
        if(piece != ''):
            screen.blit(pygame.transform.scale( piece[1], (sqr_size,sqr_size)), Square_to_position(pieces_on_board.index(piece)))
def DrawLegalMoves(screen, legal_moves, piece_sqr):
    for moves in legal_moves:
        if(moves[0] == piece_sqr):
            for move in moves[1]:
                x,y = Square_to_position(move)
                pygame.draw.circle(screen, (255,0,0), (x + 25, y + 25), 10)
def Compare_pieces_colour(id1, id2):
    if(pieces_on_board[id1] != '' and pieces_on_board[id2] != ''):
        if ((pieces_on_board[id1][0].islower() and pieces_on_board[id2][0].isupper()) 
            or (pieces_on_board[id1][0].isupper() and pieces_on_board[id2][0].islower())):
            return True
        else: return False
    return True
def GenerateLegalMoves(checkboard):
    moves = list()
    temp_moves = list()
    for piece in checkboard:
        if(piece != ''):
            piece_type = piece[0]
            piece_index = checkboard.index(piece)
            color = 1 if piece_type.islower() else - 1
            if(piece_type.lower() == 'p'): #PAWN
                if(checkboard[piece_index + 8 * color] == ''): #1 UP
                    temp_moves.append(piece_index + 8 * color)
                    if(piece_index <=15 and color == 1 or piece_index >= 48 and 
                        color == -1 and checkboard[piece_index + 16 * color] == ''): #2 UP
                        temp_moves.append(piece_index + 16 * color)
                if(checkboard[piece_index + 7 * color] != '' and Compare_pieces_colour(piece_index, piece_index + 7 * color)): #TAKING
                    temp_moves.append(piece_index + 7 * color)
                if(checkboard[piece_index + 9 * color] != '' and Compare_pieces_colour(piece_index, piece_index + 9 * color)):
                    temp_moves.append(piece_index + 9 * color)
                if(color == 1 and 48 >= piece_index >= 55):
                    pass
            if(piece_type.lower() == 'r'): #ROOK
                row,col = Square_to_row_and_column(piece_index)
                calc_moves = [Check_piece_movement((piece_index, 64, 8),piece_index), 
                              Check_piece_movement((piece_index, -1,-8),piece_index), 
                              Check_piece_movement((piece_index, (row + 1) * 8, 1),piece_index), 
                              Check_piece_movement((piece_index, (row * 8) - 1, -1),piece_index)]
                for diagnal in calc_moves:
                    for single_move in diagnal:
                        temp_moves.append(single_move)
            if(piece_type.lower() == 'b'): #BISHOP
                temp_moves = Check_piece_diagonal(piece_index)
            if(piece_type.lower() == 'q'): #QUEEN
                row,col = Square_to_row_and_column(piece_index)
                calc_moves = [Check_piece_movement((piece_index, 64, 8),piece_index), 
                              Check_piece_movement((piece_index, -1,-8),piece_index), 
                              Check_piece_movement((piece_index, (row + 1) * 8, 1),piece_index), 
                              Check_piece_movement((piece_index, (row * 8) - 1, -1),piece_index)]
                for diagnal in calc_moves:
                    for single_move in diagnal:
                        temp_moves.append(single_move)
                temp_moves = temp_moves + Check_piece_diagonal(piece_index)
            if(piece_type.lower() == 'n'): #KNIGHT
                row,col = Square_to_row_and_column(piece_index)
                directions = ((2,1), (2,-1), (1,2), (-1,2), (-2,1),(-2,-1),(1,-2),(-1,-2))
                for direction in directions:
                    if(row + direction[0] < 8 and col + direction[1] < 8):
                        dest_sqr = Row_and_column_to_square(row + direction[0], col + direction[1])
                        if(0 <= dest_sqr <= 64):
                            if (checkboard[dest_sqr] == ''):
                                temp_moves.append(dest_sqr)
                            elif(Compare_pieces_colour(piece_index, dest_sqr)):
                                temp_moves.append(dest_sqr)
            if(piece_type.lower() == 'k'): #KING
                row,col = Square_to_row_and_column(piece_index)
                directions = ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1))
                for direction in directions:
                    dest_sqr = Row_and_column_to_square(row + direction[0], col + direction[1])
                    if(0 <= dest_sqr <= 64):
                        if (checkboard[dest_sqr] == ''):
                            temp_moves.append(dest_sqr)
                        elif(Compare_pieces_colour(piece_index, dest_sqr)):
                            temp_moves.append(dest_sqr)
            if(temp_moves != []):
                moves.append((piece_index, temp_moves))
            temp_moves = []
    return moves
def CheckIfMoveIsLegal(curr_sqr, dest_sqr, pieces):
    if(Look_for_checks_in_posstion(moves, pieces)):
        alt_pieces = [x for x in pieces]
        alt_pieces[dest_sqr] = alt_pieces[curr_sqr]
        alt_pieces[curr_sqr] = ''
        alt_moves = GenerateLegalMoves(alt_pieces)
    #DEBUGGING
        # print(alt_moves)
        # for move in alt_moves:
        #     if(move[0] == 59):
        #         print(move)
    #DEBUGGING
        if(Look_for_checks_in_posstion(alt_moves, alt_pieces)):
            print("alt moves detected check")
            return False
        return True
        # NOT WORKING YET :(
    else:
        for piece in moves:
            if(piece != ''):
                if (piece[0] == curr_sqr):
                    for square in piece[1]:
                        if(int(square) == int(dest_sqr)):
                            return True
        return False

# FUNCTIONS FOR CHECKS
def Look_for_checks_in_posstion(moves, pieces = pieces_on_board):
    b_k, w_k = Locate_kings_on_board(pieces)
    for piece in moves:
        if(piece != ''):
            for square in piece[1]:
                if(square == w_k and Compare_pieces_colour(w_k, piece[0]) or square == b_k and Compare_pieces_colour(b_k, piece[0])):
                    print("Piece square " , piece[0], "Move square " , square, "Whole : ", piece)
                    return True
    return False

def Locate_kings_on_board(pieces = pieces_on_board):
    for piece in pieces:
        if(piece != ''):
            if(piece[0] == 'k'):
                w_k = pieces_on_board.index(piece)
                print("w_k ", w_k)
            elif(piece[0] == 'K'):
                b_k = pieces_on_board.index(piece)
                print("b_k ", b_k)
    return b_k, w_k

for piece in startPossition:
        if(piece != '/'):
            if(piece.isdigit()):
                id += int(piece)
            else:
                pieces_on_board[id] = [piece, pygame.image.load(r"{}\{}\{}.png".format(path, 
                                        'White' if piece.islower() else 'Black' ,piece.lower())), 
                                        Square_to_position(id)]
                id += 1

sqr1,sqr2 = -10,-10
moved = True
moves_counter = 0
clicked = False
while running:
    DrawBoard(height, width, sqr_size)
    moved = False
    DrawPieces()
    if(clicked): DrawLegalMoves(screen, moves, sqr1)
    clock = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif(event.type == pygame.MOUSEBUTTONDOWN):
            sqr1 = Position_to_square(pygame.mouse.get_pos())
            print(sqr1)
            moves = GenerateLegalMoves(pieces_on_board)
            if(sqr2 != -10): #SECOND CLICK
                if(sqr1 != sqr2):
                    if(pieces_on_board[sqr1] == ''):
                        if(CheckIfMoveIsLegal(sqr2, sqr1, pieces_on_board)):
                            pieces_on_board[sqr1] = pieces_on_board[sqr2]
                            pieces_on_board[sqr2] = ''
                            moves_counter += 1
                            print("DONE")
                        else:
                            print("Illegal move")
                    elif((pieces_on_board[sqr1][0].islower() and pieces_on_board[sqr2][0].isupper() or 
                            pieces_on_board[sqr2][0].islower() and pieces_on_board[sqr1][0].isupper())):
                        if(CheckIfMoveIsLegal(sqr2, sqr1, pieces_on_board)):
                            pieces_on_board[sqr1] = pieces_on_board[sqr2]
                            pieces_on_board[sqr2] = ''
                            moves_counter += 1
                        else:
                            print("Illegal move")
                    else:
                        print("Move is illegal")
                sqr1, sqr2 = -10,-10
                clicked = False
            elif(pieces_on_board[sqr1] != '' and ( pieces_on_board[sqr1][0].islower() and moves_counter % 2 == 0 or 
                                                    pieces_on_board[sqr1][0].isupper() and moves_counter % 2 == 1 )): #FIRST CLICK
                clicked = True
                sqr2 = sqr1
        pygame.display.update()
        clock.tick(fps)
print("Your game took: " + str(int(moves_counter/2)) + " moves!")
