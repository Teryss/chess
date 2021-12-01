import pygame
path = r"C:\Users\AdamWdowiarek\Downloads\chess"
# BASIC VARIABLES
width, height = 400,400
white = (255,255,255)
black = (181,101,29)
running = True
row,col = 8,8
sqr_size = int(width/8)
fps = 45
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess board")
startPossition = "rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR"

def Square_to_position(square_id):
    x = square_id % 8 * sqr_size
    y = int(square_id / 8) * sqr_size
    return x,y
def Position_to_square(position):
    return int(position[0] / 50) + 8 * int(position[1]/50)

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
    if ((pieces_on_board[id1][0].islower and pieces_on_board[id2][0].isupper()) or( pieces_on_board[id1][0].isupper() and pieces_on_board[id2][0].islower())):
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
            if(piece_type.lower() == 'p'):
                if(piece_type.islower()):
                    temp_moves.append(piece_index + 8)
                    if(piece_index <=15):
                        temp_moves.append(piece_index + 16)
                else:
                    temp_moves.append(piece_index - 8)
                    if(piece_index >= 48):
                        temp_moves.append(piece_index - 16)
            moves.append((piece_type, temp_moves))
            temp_moves = []
    return moves

pieces_on_board = ['']*64 #CONTENT IN ORDER: type, path_to_img, position_x, position_y
id = 0
for piece in startPossition:
        if(piece == '/'):
            pass
        else:
            if(piece.isdigit()):
                id += int(piece)
            else:
                pieces_on_board[id] = [piece, pygame.image.load(r"{}\{}\{}.png".format(path, 'White' if piece.islower() else 'Black' ,piece.lower())), Square_to_position(id)]
                id += 1

move_1 = move_2 = 0
moved = True
while running:
    if(moved): DrawBoard(height, width, sqr_size)
    moved = False
    DrawPieces()
    clock = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif(event.type == pygame.MOUSEBUTTONDOWN):
            print(GenerateLegalMoves())
            square_id = Position_to_square(pygame.mouse.get_pos())
            print(square_id)
            if (pieces_on_board[square_id] == ''):
                if(move_1 != 0):
                    pieces_on_board[square_id] = pieces_on_board[move_1]
                    pieces_on_board[move_1] = ''
                    move_1 = 0
                    moved = True
            else:
                if(move_1 != 0 and Compare_pieces_colour(move_1, square_id)):
                    pieces_on_board[square_id] = pieces_on_board[move_1]
                    pieces_on_board[move_1] = ''
                    move_1 = 0
                    moved = True
                elif(move_1 == 0):
                    move_1 = square_id
        pygame.display.update()
        clock.tick(fps)
