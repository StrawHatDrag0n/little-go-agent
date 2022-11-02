from board_reader import BoardReader
from board_writer import BoardWriter
from greedy_player import GreedyPlayer
from q_player import QLearner

if __name__ == '__main__':
    board_reader = BoardReader()
    piece_type, previous_board, current_board = board_reader.read_board()
    my_player = GreedyPlayer(piece_type, current_board, previous_board)
    move = my_player.move()
    board_writer = BoardWriter()
    if move == 'PASS':
        board_writer.write_move(move)
    else:
        board_writer.write_move(f'{move[0]},{move[1]}')
