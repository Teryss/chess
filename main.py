from tabnanny import check
from black import out
import pygame
import os
import sys
sys.setrecursionlimit(16385)

# BASIC VARIABLES
width, height = 400, 400
white = (255, 255, 255)
black = (181, 101, 29)
sqr_size = int(width/8)
fps = 30
pieces_on_board = ['']*64  # CONTENT IN ORDER: type, path_to_img, position_x, position_y
directions = {
    "knight":((2,1), (2,-1), (1,2), (-1,2), (-2,1),(-2,-1),(1,-2),(-1,-2)),
    "king": ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1,-1)),
    "bishop": ((1, 1), (1, -1), (-1, 1), (-1, -1))
}
did_piece_move = {
    "w_k" : False,
    "b_k" : False,
    "left_rook_white" : False,
    "right_rook_white" : False,
    "left_rook_black" : False,
    "right_rook_black" : False,
}
#BASIC FUNCTIONS
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
#DRAWING FUNCTIONS
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
    for movess in legal_moves:
        if(movess[0] == piece_sqr):
            for move in movess[1]:
                x,y = Square_to_position(move)
                pygame.draw.circle(screen, (255,0,0), (x + 25, y + 25), 10)
#PIECE MOVEMENT FUNCTIONS
def Check_piece_movement_up_down(board, args,cur_sqr):
    legal_moves = list()
    for i in range(args[0], args[1], args[2]):
        if(i != cur_sqr):
            if(board[i] == ''):
                legal_moves.append(i)
            else:
                if(Compare_pieces_colour(cur_sqr, i, board)):
                    legal_moves.append(i)
                return legal_moves
    return legal_moves
def Check_piece_diagonal(board, cur_sqr):
    legal_moves = list()
    row, col = Square_to_row_and_column(cur_sqr)
    for diagnal in directions['bishop']:
        for i in range(1,9):
            t_row = row + i * diagnal[0]
            t_col = col + i * diagnal[1]
            check_square = Row_and_column_to_square(t_row, t_col)
            f_col = Square_to_row_and_column(check_square)[1]
            if(f_col != t_col): break
            if(0 <= check_square <= 63):
                if(board[check_square] == ''):
                    legal_moves.append(check_square)
                else:
                    if(Compare_pieces_colour(cur_sqr, check_square, board)):
                        legal_moves.append(check_square)
                    break
    return legal_moves
def Compare_pieces_colour(id1, id2, comp_board = pieces_on_board):
    if(comp_board[id1] != '' and comp_board[id2] != ''):
        if ((comp_board[id1][0].islower() and comp_board[id2][0].islower()) 
            or (comp_board[id1][0].isupper() and comp_board[id2][0].isupper())):
            return False
        return True
    return False
def GenerateLegalMoves(checkboard, all_moves_made):
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
                    if((piece_index <=15 and color == 1 or piece_index >= 48 and color == -1) and checkboard[piece_index + 16 * color] == ''): #2 UP]
                        temp_moves.append(piece_index + 16 * color)
                if 24 >= piece_index >= 31 and color == -1 or 32 >= piece_index >= 39 and color == 1:
                    print('piece index: {} piece to the right {} last move {}'.format(piece_index, checkboard[piece_index+1][0], all_moves_made[-1]))
                    if checkboard[piece_index + 1][0].tolower() == 'p' and Compare_pieces_colour(piece_index + 1, piece_index, checkboard) and all_moves_made[-1] == piece_index + 1:
                        # temp_moves.append(piece_index + 1 + 8 * color)
                        print("IT WORKS")
                        #TODO IMPLEMENT EN PASSANT
                if(checkboard[piece_index + 7 * color] != '' and Compare_pieces_colour(piece_index, piece_index + 7 * color, checkboard)): #TAKING
                    temp_moves.append(piece_index + 7 * color)
                if(checkboard[piece_index + 9 * color] != '' and Compare_pieces_colour(piece_index, piece_index + 9 * color, checkboard)):
                    temp_moves.append(piece_index + 9 * color)
            if(piece_type.lower() == 'r'): #ROOK
                row,col = Square_to_row_and_column(piece_index)
                temp_moves = Check_piece_movement_up_down(checkboard, (piece_index, 64, 8),piece_index) + Check_piece_movement_up_down(checkboard, (piece_index, -1,-8),piece_index) + Check_piece_movement_up_down(checkboard, (piece_index, (row + 1) * 8, 1),piece_index) + Check_piece_movement_up_down(checkboard, (piece_index, (row * 8) - 1, -1),piece_index)
            if(piece_type.lower() == 'b'): #BISHOP
                temp_moves = Check_piece_diagonal(checkboard, piece_index)
            if(piece_type.lower() == 'q'): #QUEEN
                row,col = Square_to_row_and_column(piece_index)
                calc_moves = Check_piece_movement_up_down(checkboard, (piece_index, 64, 8),piece_index) + Check_piece_movement_up_down(checkboard, (piece_index, -1,-8),piece_index) + Check_piece_movement_up_down(checkboard, (piece_index, (row + 1) * 8, 1),piece_index) + Check_piece_movement_up_down(checkboard, (piece_index, (row * 8) - 1, -1),piece_index)
                temp_moves = calc_moves + Check_piece_diagonal(checkboard, piece_index)
            if(piece_type.lower() == 'n'): #KNIGHT
                row,col = Square_to_row_and_column(piece_index)
                for direction in directions['knight']:
                    if(-1 < row + direction[0] < 8 and 8 > col + direction[1] > -1):
                        dest_sqr = Row_and_column_to_square(row + direction[0], col + direction[1])
                        if(0 <= dest_sqr <= 64):
                            if (checkboard[dest_sqr] == ''):
                                temp_moves.append(dest_sqr)
                            elif(Compare_pieces_colour(piece_index, dest_sqr, checkboard)):
                                temp_moves.append(dest_sqr)
            if(piece_type.lower() == 'k'): #KING
                row,col = Square_to_row_and_column(piece_index)
                for direction in directions['king']:
                    dest_sqr = Row_and_column_to_square(row + direction[0], col + direction[1])
                    if(0 <= dest_sqr <= 64):
                        if (checkboard[dest_sqr] == ''):
                            temp_moves.append(dest_sqr)
                        elif(Compare_pieces_colour(piece_index, dest_sqr, checkboard)):
                            temp_moves.append(dest_sqr)
            if(temp_moves != []):
                moves.append([piece_index, temp_moves])
            temp_moves = []
    moves = Add_castle(checkboard, moves)
    return moves

def Delete_illegal_moves(checkboard, moves):
    check = Look_for_checks_in_posstion(moves, checkboard)
    if check != '':
        moves_to_delete = list()
        counter_1, counter_2 = 0,0
        for i in range(len(moves)):
            if (checkboard[moves[i][0]][0].islower() and check == 'w_k_check') or (checkboard[moves[i][0]][0].isupper() and check == 'b_k_check'):
                for move in moves[i][1]:
                    counter_1 += 1
                    alt_pieces = [x for x in checkboard]
                    alt_pieces[move] = alt_pieces[moves[i][0]]
                    alt_pieces[moves[i][0]] = ''
                    alt_moves = GenerateLegalMoves(alt_pieces)
                    if Look_for_checks_in_posstion(alt_moves, alt_pieces):
                        moves_to_delete.append((i,move))
                        counter_2 += 1
        if counter_1 - 1 == counter_2:
            return 0
        else:
            print(counter_1, " ;; ", counter_2)
        for move in moves_to_delete:
            if type(move) is tuple:
                if move[1] in moves[move[0]][1]:
                    moves[move[0]][1].remove(move[1])
    return moves

def Add_castle(checkboard, moves):
    for i in range(len(moves)):
        if checkboard[moves[i][0]][0] == "K":
            global moves_b_k_index
            moves_b_k_index = i
        elif checkboard[moves[i][0]][0] == "k":
            global moves_w_k_index
            moves_w_k_index = i

    if did_piece_move['w_k'] == False:
        if did_piece_move['left_rook_white'] == False and checkboard[1:3] == ['','']:
            moves[moves_w_k_index][1].append(1)
        if did_piece_move['right_rook_white'] == False and checkboard[4:7] == ['','','']:
            moves[moves_w_k_index][1].append(5)
    if did_piece_move["b_k"] == False:
        if did_piece_move['left_rook_black'] == False and checkboard[57:59] == ['','']:
            moves[moves_b_k_index][1].append(57)
        if did_piece_move['right_rook_black'] == False and checkboard[60:63] ==['','','']:
            moves[moves_b_k_index][1].append(61)
    return moves

def Look_for_checks_in_posstion(check_moves, check_pieces):
    all_squares_attacked_by_white = list()
    all_squares_attacked_by_black = list()
    for piece in check_pieces:
        if(piece != ''):
            if(piece[0] == 'k'): 
                w_k = check_pieces.index(piece)
            elif(piece[0]== 'K'):
                b_k = check_pieces.index(piece)                
    for move in check_moves:
        if(check_pieces[move[0]][0].islower()):
            all_squares_attacked_by_white += move[1]
        if(check_pieces[move[0]][0].isupper()):
            all_squares_attacked_by_black += move[1]
    # if w_k in all_squares_attacked_by_black or b_k in all_squares_attacked_by_white:
    #     return True
    # else:
    #     return False
    if w_k in all_squares_attacked_by_black:
        return "w_k_check"
    if b_k in all_squares_attacked_by_white:
        return "b_k_check"
    return ''

def CheckIfMoveIsInGeneratedMoves(curr_sqr, dest_sqr):
    for piece in moves:
        if curr_sqr == piece[0] and int(dest_sqr) in piece[1]:
            if curr_sqr == 63 or dest_sqr == 63: did_piece_move['right_rook_black'] = True
            elif curr_sqr == 56 or dest_sqr == 56: did_piece_move['left_rook_black'] = True
            elif curr_sqr == 0 or dest_sqr == 0: did_piece_move['left_rook_white'] = True
            elif curr_sqr == 7 or dest_sqr == 7: did_piece_move['right_rook_white'] = True
            elif curr_sqr == 3:
                if dest_sqr == 1:
                    pieces_on_board[2] = pieces_on_board[0]
                    pieces_on_board[0] = ''
                elif dest_sqr == 5:
                    pieces_on_board[4] = pieces_on_board[7]
                    pieces_on_board[7] = ''
                did_piece_move['w_k'] = True
            elif curr_sqr == 59: 
                if dest_sqr == 57:
                    pieces_on_board[58] = pieces_on_board[56]
                    pieces_on_board[56] = ''
                elif dest_sqr == 61:
                    pieces_on_board[60] = pieces_on_board[63]
                    pieces_on_board[63] = '' 
                did_piece_move['b_k'] = True
            return True
    return False
id = 0
startPossition = "rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR"
path = os.path.dirname(os.path.abspath(__file__))
for piece in startPossition:
        if(piece != '/'):
            if(piece.isdigit()):
                id += int(piece)
            else:
                pieces_on_board[id] = [piece, pygame.image.load(r"{}\{}\{}.png".format(path, 
                                        'White' if piece.islower() else 'Black' ,piece.lower())), 
                                        Square_to_position(id)]
                id += 1
#ACTUAL LOOP
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess board")
sqr1,sqr2 = -10,-10
moved = True
moves_counter = 0
clicked = False
global running
running = True
all_moves_made = list()
are_moves_generated = False
while running:
    DrawBoard(height, width, sqr_size)
    DrawPieces()
    if are_moves_generated == False:
        moves = Delete_illegal_moves(pieces_on_board, GenerateLegalMoves(pieces_on_board, all_moves_made))
        if moves == 0:
            running = False
        are_moves_generated == True
    if(clicked): 
        DrawLegalMoves(screen, moves, sqr1)
    clock = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif(event.type == pygame.MOUSEBUTTONDOWN):
            sqr1 = Position_to_square(pygame.mouse.get_pos())
            print(sqr1)
            if(sqr2 != -10): #SECOND CLICK
                if(sqr1 != sqr2):
                    if(pieces_on_board[sqr1] == ''): #MOVE PIECE TO ANOTHER SQUARE
                        if(CheckIfMoveIsInGeneratedMoves(sqr2, sqr1)):
                            pieces_on_board[sqr1] = pieces_on_board[sqr2]
                            pieces_on_board[sqr2] = ''
                            moves_counter += 1
                            all_moves_made.append(sqr1)
                            print("DONE")
                            are_moves_generated = False
                        else:
                            print("Illegal move 1")
                    elif((pieces_on_board[sqr1][0].islower() and pieces_on_board[sqr2][0].isupper() or 
                            pieces_on_board[sqr2][0].islower() and pieces_on_board[sqr1][0].isupper())): #CAPTURE ANOTHER PIECE
                        if(CheckIfMoveIsInGeneratedMoves(sqr2, sqr1)):
                            pieces_on_board[sqr1] = pieces_on_board[sqr2]
                            pieces_on_board[sqr2] = ''
                            moves_counter += 1
                            all_moves_made.append(sqr1)
                            are_moves_generated = False
                            print("DONE 2")
                        else:
                            print("Illegal move 2")
                sqr1, sqr2 = -10,-10
                clicked = False
            elif(pieces_on_board[sqr1] != '' and ( pieces_on_board[sqr1][0].islower() and moves_counter % 2 == 0 or 
                                                    pieces_on_board[sqr1][0].isupper() and moves_counter % 2 == 1 )): #FIRST CLICK
                clicked = True
                sqr2 = sqr1
        pygame.display.update()
        clock.tick(fps)
print("Your game took: " + str(int(moves_counter/2)) + " moves!")
