import base_func

class MovesGenerator():
    def __init__(self, board):
        self.board = board
        self.Get_current_pos()
        self.directions = {
            "knight": ((2,1), (2,-1), (1,2), (-1,2), (-2,1), (-2,-1), (1,-2), (-1,-2)),
            "king":  ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1,-1)),
            "bishop": ((1, 1), (1, -1), (-1, 1), (-1, -1))
        }
        self.moves = []
        self.did_piece_move = {
            "w_k" : False,
            "b_k" : False,
            "left_rook_white" : False,
            "right_rook_white" : False,
            "left_rook_black" : False,
            "right_rook_black" : False,
        }
        self.en_passant = False
        self.sqrs_attacked_by = {
            'B': [],
            'W': []
        }

    def Get_current_pos(self):
        self.piece_pos = self.board.Get_pos()

    def Generate_legal_moves(self, all_moves_made, get_cur_pos, which_player_to_move):
        if get_cur_pos:
            self.Get_current_pos()
        
        all_moves, self.en_passant = self.Gen_all_moves(made_moves = all_moves_made, return_enpassant=True)
        moves_with_castling = self.Add_castle(all_moves)
        only_legal_moves = self.Delete_illegal_moves(moves_with_castling, which_player_to_move)
        self.moves = only_legal_moves
        return self.moves

    def Gen_all_moves(self, alt_board = 0, made_moves = 0, return_enpassant = False):
        moves = list()
        temp_moves = list()
        if alt_board == 0:
            checkboard = self.piece_pos
        else:
            checkboard = alt_board
        is_en_passsant_possible = False
        found_en_passant = False
        #Should look for en passant?
        if made_moves != 0:
            if len(made_moves) > 0:
                try:
                    is_en_passsant_possible = True if checkboard[made_moves[-1][1]][0].lower() == 'p' and abs(made_moves[-1][0] - made_moves[-1][1]) == 16 else False
                except:
                    # print("looking for en passant broke")
                    is_en_passsant_possible = False

        for piece in checkboard:
            if piece != '':
                piece_type = piece[0]
                piece_index = checkboard.index(piece)
                color = 1 if piece_type.islower() else -1
                #PAWN
                if piece_type.lower() == 'p': 
                    if -1 < piece_index + 8 * color < 64 and checkboard[piece_index + 8 * color] == '': #1 UP
                        temp_moves.append(piece_index + 8 * color)
                        if (piece_index <=15 and color == 1 or piece_index >= 48 and color == -1) and checkboard[piece_index + 16 * color] == '': #2 UP]
                            temp_moves.append(piece_index + 16 * color)
                    if is_en_passsant_possible:
                        if piece_index + 1 == made_moves[-1][1]:
                            if base_func.Compare_pieces_colour(piece_index, made_moves[-1][1], checkboard):
                                if color == 1 :
                                    temp_moves.append(piece_index + 9 * color)
                                else:
                                    temp_moves.append(piece_index + 7 * color)
                                found_en_passant = True
                        elif piece_index - 1 == made_moves[-1][1]:
                            if base_func.Compare_pieces_colour(piece_index, made_moves[-1][1], checkboard):
                                if color == 1 :
                                    temp_moves.append(piece_index + 7 * color)
                                else:
                                    temp_moves.append(piece_index + 9 * color)
                                found_en_passant = True
                    #TAKING
                    if -1 < piece_index + 7 * color < 64 and checkboard[piece_index + 7 * color] != '' and base_func.Compare_pieces_colour(piece_index, piece_index + 7 * color, checkboard):
                        if abs(base_func.Square_to_row_and_column(piece_index)[1] - base_func.Square_to_row_and_column(piece_index + 7 * color)[1]) <= 1:
                            temp_moves.append(piece_index + 7 * color)
                    if -1 < piece_index + 7 * color < 64 and checkboard[piece_index + 9 * color] != '' and base_func.Compare_pieces_colour(piece_index, piece_index + 9 * color, checkboard):
                        if abs(base_func.Square_to_row_and_column(piece_index)[1] - base_func.Square_to_row_and_column(piece_index + 9 * color)[1]) <= 1:
                            temp_moves.append(piece_index + 9 * color)
                if piece_type.lower() == 'r':
                    temp_moves += self.RookMovement(piece_index, checkboard)
                if piece_type.lower() == 'b':
                    temp_moves = base_func.Check_piece_diagonal(checkboard, piece_index, self.directions)
                if piece_type.lower() == 'q':
                    temp_moves += self.RookMovement(piece_index, checkboard)
                    temp_moves += base_func.Check_piece_diagonal(checkboard, piece_index,self.directions)
                if piece_type.lower() == 'n':
                    temp_moves += self.KingNMovemnt(piece_index, checkboard, 'knight')
                if piece_type.lower() == 'k':
                    temp_moves += self.KingNMovemnt(piece_index, checkboard, 'king')
                if temp_moves != []:
                    moves.append([piece_index, temp_moves])
                temp_moves = []
        if return_enpassant:
            return moves, found_en_passant
        return moves

    def RookMovement(self, index, board):
        row,col = base_func.Square_to_row_and_column(index)
        moves = base_func.Check_piece_movement_up_down(board, (index, 64, 8),index)
        moves += base_func.Check_piece_movement_up_down(board, (index, -1,-8),index) 
        moves += base_func.Check_piece_movement_up_down(board, (index, (row + 1) * 8, 1),index) 
        moves += base_func.Check_piece_movement_up_down(board, (index, (row * 8) - 1, -1),index)
        return moves

    def KingNMovemnt(self, index, board, type):
        moves = list()
        row,col = base_func.Square_to_row_and_column(index)
        for direction in self.directions[type]:
            if -1 < row + direction[0] < 8 and 8 > col + direction[1] > -1:
                dest_sqr = base_func.Row_and_column_to_square(row + direction[0], col + direction[1])
                if 0 <= dest_sqr <= 63:
                    if board[dest_sqr] == '':
                        moves.append(dest_sqr)
                    elif base_func.Compare_pieces_colour(index, dest_sqr, board):
                        moves.append(dest_sqr)
        return moves
        
    def Add_castle(self, moves):
        self.sqrs_attacked_by['W'], self.sqrs_attacked_by['B'] = self.GetAllSqrsOccupied(self.piece_pos, moves) 
        for i in range(len(moves)):
            if self.piece_pos[moves[i][0]][0] == "K":
                moves_b_k_index = i
            elif self.piece_pos[moves[i][0]][0] == "k":
                moves_w_k_index = i

        if self.did_piece_move['w_k'] == False:
            if self.did_piece_move['left_rook_white'] == False and self.piece_pos[1:3] == ['',''] and 3 not in self.sqrs_attacked_by['B']:
                moves[moves_w_k_index][1].append(1)
            if self.did_piece_move['right_rook_white'] == False and self.piece_pos[4:7] == ['','',''] and 4 not in self.sqrs_attacked_by['B']:
                moves[moves_w_k_index][1].append(5)

        if self.did_piece_move["b_k"] == False:
            if self.did_piece_move['left_rook_black'] == False and self.piece_pos[57:59] == ['',''] and 57 not in self.sqrs_attacked_by['W']:
                moves[moves_b_k_index][1].append(57)
            if self.did_piece_move['right_rook_black'] == False and self.piece_pos[60:63] ==['','',''] and 60 not in self.sqrs_attacked_by['W']:
                moves[moves_b_k_index][1].append(61)
        return moves

    def Delete_illegal_moves(self, moves, player_turn):
        checkboard = self.piece_pos
        check = self.Look_for_checks_in_posstion(moves, checkboard)
        moves_to_delete = list()
        for i in range(len(moves)):
            for move in moves[i][1]:
                alt_pieces = [x for x in checkboard] 
                alt_pieces[move] = alt_pieces[moves[i][0]]
                alt_pieces[moves[i][0]] = ''
                alt_moves = self.Gen_all_moves(alt_pieces)
                who_got_checked = self.Look_for_checks_in_posstion(alt_moves, alt_pieces)

                if player_turn == 1 and 'W' in who_got_checked or player_turn == -1 and 'B' in who_got_checked:
                    moves_to_delete.append((i,move))

        for move in moves_to_delete:
            if type(move) is tuple:
                if move[1] in moves[move[0]][1]:
                    moves[move[0]][1].remove(move[1])

        if check != '':
            if 'W' in check and player_turn == 1 and len(self.sqrs_attacked_by['W']) == 0:
                return "Black wins by checkmate"
            elif 'B' in check and player_turn == -1 and len(self.sqrs_attacked_by['B']) == 0:
                return "White wins by checkmate"
            k_pos = self.Locate_kings_on_board()
            self.board.Change_checked_king_square(k_pos[1] if check == 'B' else k_pos[0])
        else:
            if len(self.sqrs_attacked_by['B']) == 0 and player_turn == -1 or len(self.sqrs_attacked_by['W']) == 0 and player_turn == 1:
                return "Draw by stalemate"
            self.board.Change_checked_king_square(-10)

        return moves
        
    def Look_for_checks_in_posstion(self, check_moves, check_pieces):
        w_k,b_k = -10,-10
        for piece in check_pieces:
            if(piece != ''):
                if(piece[0] == 'k'): 
                    w_k = check_pieces.index(piece)
                elif(piece[0]== 'K'):
                    b_k = check_pieces.index(piece)

        w_moves, b_moves = self.GetAllSqrsOccupied(check_pieces, check_moves)
        output = ''
        if w_k == -10 or w_k in b_moves:
            output += 'W'
        if b_k == -10 or b_k in w_moves:
            output += 'B'
        return output

    def CheckIfMoveIsInGeneratedMoves(self,curr_sqr, dest_sqr):
        # print('Is en passant possible? ', self.en_passant)
        for piece in self.moves:
            if curr_sqr == piece[0] and int(dest_sqr) in piece[1]:
                #CASTLING
                if curr_sqr == 63 or dest_sqr == 63: self.did_piece_move['right_rook_black'] = True
                elif curr_sqr == 56 or dest_sqr == 56: self.did_piece_move['left_rook_black'] = True
                elif curr_sqr == 0 or dest_sqr == 0: self.did_piece_move['left_rook_white'] = True
                elif curr_sqr == 7 or dest_sqr == 7: self.did_piece_move['right_rook_white'] = True
                elif curr_sqr == 3:
                    if dest_sqr == 1:
                        self.piece_pos[2] = self.piece_pos[0]
                        self.piece_pos[0] = ''
                    elif dest_sqr == 5:
                        self.piece_pos[4] = self.piece_pos[7]
                        self.piece_pos[7] = ''
                    self.did_piece_move['w_k'] = True
                elif curr_sqr == 59: 
                    if dest_sqr == 57:
                        self.piece_pos[58] = self.piece_pos[56]
                        self.piece_pos[56] = ''
                    elif dest_sqr == 61:
                        self.piece_pos[60] = self.piece_pos[63]
                        self.piece_pos[63] = '' 
                    self.did_piece_move['b_k'] = True
                #EN PASSANT
                if self.en_passant:
                    if self.piece_pos[curr_sqr][0].lower() == 'p' and self.piece_pos[dest_sqr] == '':
                        pawn_color = 1 if self.piece_pos[curr_sqr][0].islower() else -1
                        if self.piece_pos[dest_sqr - 8 * pawn_color] != '' and self.piece_pos[dest_sqr - 8 * pawn_color][0].lower() == 'p':
                            if self.piece_pos[curr_sqr] != self.piece_pos[dest_sqr - 8 * pawn_color]:
                                self.piece_pos[dest_sqr - 8 * pawn_color] = ''
                return True
        return False

    def Locate_kings_on_board(self, position = None):
        pieces = position if position is not None else self.piece_pos
        kings_pos = [-10,-10]

        for piece in pieces:
            if piece != '':
                if piece[0] == 'k':
                    kings_pos[0] = self.piece_pos.index(piece)
                if piece[0] == 'K':
                    kings_pos[1] = self.piece_pos.index(piece)
        return kings_pos 

    def GetAllSqrsOccupied(self, pieces, moves):
        w, b = [], []
        for move in moves:
            if(pieces[move[0]][0].islower()):
                w += move[1]
            if(pieces[move[0]][0].isupper()):
                b += move[1]
        return w, b

    def getMoves(self):
        return self.moves