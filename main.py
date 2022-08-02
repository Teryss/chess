import pygame
import base_func
import board
import generator
# import eval


def run():
    WIDTH, HEIGHT = 400, 400
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess board")

    START_POSSITION = "rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR"
    FPS = 30
    chess_board = board.Board(START_POSSITION, WIDTH, HEIGHT, SCREEN, side_on_top='B')
    moveGenerationObj = generator.MovesGenerator(chess_board)
    chess_board.importMoveGenerationObj(moveGenerationObj)
    moves_counter = 0
    running = True
    all_moves_made = list()
    are_moves_generated = False

    while running:
        chess_board.Draw_Board()
        chess_board.Draw_Legal_Moves()
        chess_board.Draw_Pieces()
        if are_moves_generated is False:
            chess_board.Pawn_promotion()
            moves = moveGenerationObj.Generate_legal_moves(all_moves_made, get_cur_pos = True, which_player_to_move = 1 if moves_counter % 2 == 0 else -1)
            are_moves_generated = True
            if type(moves) is not list:
                print(moves)
                running = False

        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                sqr = base_func.Position_to_square(pygame.mouse.get_pos())
                did_any_piece_move = chess_board.moveHandler(sqr)
                if did_any_piece_move is not None:
                    moves_counter += 1
                    all_moves_made.append(did_any_piece_move)
                    are_moves_generated = False
                    
            pygame.display.update()
            clock.tick(FPS)
    print("Moves made in total: ", moves_counter)

if __name__ == '__main__':
    run()
