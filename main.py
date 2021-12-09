#### CURRENT STATE IS BUGGED ####
import pygame
path = r"C:\Users\AdamWdowiare_8u\Desktop\chess-main"
# BASIC VARIABLES
width, height = 400, 400
white = (255, 255, 255)
black = (181, 101, 29)
running = True
row, col = 8, 8
sqr_size = int(width/8)
fps = 45
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
def Check_piece_diagnal(cur_sqr):
    legal_moves = list()
    row, col = Square_to_row_and_column(cur_sqr)
    diagnals = ((1, 1), (1, -1), (-1, 1), (-1, -1))
    for diagnal in diagnals:
        for i in range(1,9):
            check_square = Row_and_column_to_square(row + i * diagnal[0], col + i * diagnal[1])
            if(check_square <= 63 and check_square >= 0):
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

def Compare_pieces_colour(id1, id2):
    if ((pieces_on_board[id1][0].islower() and pieces_on_board[id2][0].isupper()) or (pieces_on_board[id1][0].isupper() and pieces_on_board[id2][0].islower())):
        return True
    else:
        return False


def GenerateLegalMoves():
    moves = list()
    temp_moves = list()
    for piece in pieces_on_board:
        if(piece != ''):
            piece_type = piece[0]
            piece_index = pieces_on_board.index(piece)
            color = 1 if piece_type.islower() else - 1
            if(moves_counter % 2 == 0 and color == 1 or moves_counter % 2 == 1 and color == -1):
                if(piece_type.lower() == 'p'):
                    if(moves_counter % 2 == 0 and color == 1 or moves_counter % 2 == 1 and color == -1):
                        if(pieces_on_board[piece_index + 8 * color] == ''): #1 UP
                            temp_moves.append(piece_index + 8 * color)
                        if(piece_index <=15 and color == 1 or piece_index >= 48 and color == -1): #2 UP
                            temp_moves.append(piece_index + 16 * color)
                        if(pieces_on_board[piece_index + 7 * color] != '' and Compare_pieces_colour(piece_index, piece_index + 7 * color)): #TAKING
                            temp_moves.append(piece_index + 7 * color)
                        if(pieces_on_board[piece_index + 9 * color] != '' and Compare_pieces_colour(piece_index, piece_index + 9 * color)):
                            temp_moves.append(piece_index + 9 * color)
                if(piece_type.lower() == 'r'):
                    row,col = Square_to_row_and_column(piece_index)
                    calc_moves = [Check_piece_movement((piece_index, 64, 8),piece_index), Check_piece_movement((piece_index, -1,-8),piece_index), Check_piece_movement((piece_index, (row + 1) * 8, 1),piece_index), Check_piece_movement((piece_index, (row * 8) - 1, -1),piece_index)]
                    for diagnal in calc_moves:
                        for single_move in diagnal:
                            temp_moves.append(single_move)
                if(piece_type.lower() == 'b'):
                    temp_moves = Check_piece_diagnal(piece_index)
                if(piece_type.lower() == 'q'):
                    row,col = Square_to_row_and_column(piece_index)
                    calc_moves = [Check_piece_movement((piece_index, 64, 8),piece_index), Check_piece_movement((piece_index, -1,-8),piece_index), Check_piece_movement((piece_index, (row + 1) * 8, 1),piece_index), Check_piece_movement((piece_index, (row * 8) - 1, -1),piece_index)]
                    for diagnal in calc_moves:
                        for single_move in diagnal:
                            temp_moves.append(single_move)
                    temp_moves = temp_moves + Check_piece_diagnal(piece_index)
                if(piece_type.lower() == 'n'):
                    row,col = Square_to_row_and_column(piece_index)
                    directions = ((2,1), (2,-1), (1,2), (-1,2), (-2,1),(-2,-1),(1,-2),(1,2))
                    for direction in directions:
                        dest_sqr = Row_and_column_to_square(row + direction[0], col + direction[1])
                        if(dest_sqr <= 64 and dest_sqr >= 0):
                            if (pieces_on_board[dest_sqr] == ''):
                                temp_moves.append(dest_sqr)
                            elif(Compare_pieces_colour(piece_index, dest_sqr)):
                                temp_moves.append(dest_sqr)
                if(piece_type.lower() == 'k'):
                    row,col = Square_to_row_and_column(piece_index)
                    directions = ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1))
                    for direction in directions:
                        dest_sqr = Row_and_column_to_square(row + direction[0], col + direction[1])
                        if(0 <= dest_sqr <= 64):
                            if (pieces_on_board[dest_sqr] == ''):
                                temp_moves.append(dest_sqr)
                            elif(Compare_pieces_colour(piece_index, dest_sqr)):
                                temp_moves.append(dest_sqr)
            if(temp_moves != []):
                moves.append((piece_index, temp_moves))
            temp_moves = []
    return moves

def CheckIfMoveIsLegal(curr_sqr, dest_sqr):
    print(moves)
    #check
    # wK_square, bK_square = 0, 0
    # for piece in pieces_on_board:
    #     if(piece[0] == 'k'):
    #         wK_square = Position_to_square((piece[3], piece[4]))
    #     if(piece[0] == 'K'):
    #         bK_square = Position_to_square((piece[3], piece[4]))
    # CONTINUE WITH CHECKS AND MATES: pinned_pieces LIST

    for piece in moves:
        if(piece != ''):
            if (piece[0] == curr_sqr):
                for square in piece[1]:
                    if(int(square) == int(dest_sqr)):
                        return True
    return False

for piece in startPossition:
        if(piece != '/'):
            if(piece.isdigit()):
                id += int(piece)
            else:
                pieces_on_board[id] = [piece, pygame.image.load(r"{}\{}\{}.png".format(path, 'White' if piece.islower() else 'Black' ,piece.lower())), Square_to_position(id)]
                id += 1

move_1 = move_2 = -1
moved = True
moves_counter = 0
while running:
    if(moved): DrawBoard(height, width, sqr_size)
    moved = False
    DrawPieces()
    clock = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif(event.type == pygame.MOUSEBUTTONDOWN):
            moves = GenerateLegalMoves()
            square_id = Position_to_square(pygame.mouse.get_pos())
            if (pieces_on_board[square_id] == ''):
                if(move_1 != -1 and CheckIfMoveIsLegal(move_1, square_id)):
                    pieces_on_board[square_id] = pieces_on_board[move_1]
                    pieces_on_board[move_1] = ''
                    move_1 = -1
                    moved = True
                    moves_counter += 1
                else:
                    move_1 = -1
            else:
                if(move_1 != -1 and move_1 != square_id and CheckIfMoveIsLegal(move_1,square_id)):
                    pieces_on_board[square_id] = pieces_on_board[move_1]
                    pieces_on_board[move_1] = ''
                    move_1 = 0
                    moved = True
                    moves_counter += 1
                elif(move_1 == -1):
                    move_1 = square_id
                elif(move_1 != square_id):
                    move_1 = -1
        pygame.display.update()
        clock.tick(fps)
print("Your game took: " + str(moves_counter) + " moves!")
