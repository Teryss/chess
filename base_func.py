def Square_to_position(square_id, sqr_size):
    x = square_id % 8 * sqr_size
    y = int(square_id / 8) * sqr_size
    return x, y
    
def Position_to_square(position):
    return int(position[0] / 50) + 8 * int(position[1]/50)

def Square_to_row_and_column(square_id):
    return int(square_id / 8), int(square_id % 8)

def Row_and_column_to_square(row, column):
    return row * 8 + column

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

def Check_piece_diagonal(board, cur_sqr, directions):
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

def Compare_pieces_colour(id1, id2, comp_board):
    if(comp_board[id1] != '' and comp_board[id2] != ''):
        if ((comp_board[id1][0].islower() and comp_board[id2][0].islower()) 
            or (comp_board[id1][0].isupper() and comp_board[id2][0].isupper())):
            return False
        return True
    return False