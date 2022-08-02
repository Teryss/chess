import board

def unmake_moves(board, moves_made):
    pass

def run(cur_board, move_gen, moves, depth, white_to_move):
    alt_board = board.Board()
    cur_pos = cur_board.Get_pos()
    alt_pos = [x for x in cur_pos]
    alt_board.pieces = alt_pos



    eval1 = eval(alt_board.Get_pos())
    move_to_make = moves[0]
    move_to_make = [move_to_make[0], move_to_make[1][0]]
    alt_board.Make_a_move(move_to_make)
    eval2 = eval(alt_board.Get_pos())

    print(eval1, eval2)

def eval(position):

    piece_weight = {
        'p' : 1,
        'b' : 3.5,
        'n' : 3,
        'q' : 9,
        'r' : 5,
    }

    evaluation = 0
    for piece in position:
        if piece != '':
            if piece[0].lower() != 'k':
                if piece[0].islower():
                    evaluation += piece_weight[piece[0]]
                else:
                    evaluation -= piece_weight[piece[0]]
    return evaluation