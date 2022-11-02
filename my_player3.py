from alpha_beta_player import AlphaBetaPlayer
from board_reader import BoardReader
from board_writer import BoardWriter

from go import GO


if __name__ == "__main__":
    N = 5
    board_reader = BoardReader()
    piece_type, previous_board, current_board = board_reader.read_board()
    move_number = board_reader.get_move_number(current_board, previous_board)

    go = GO(N)
    go.n_move = move_number
    go._set_board(piece_type, previous_board, current_board)

    my_player = AlphaBetaPlayer()
    move = my_player.move(go, piece_type)

    try:
        board_writer = BoardWriter()
        board_writer.write_move(move, True)
    except Exception as e:
        print(move)
