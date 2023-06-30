import random

from board_reader import BoardReader
from board_writer import BoardWriter
from go import GO
from greedy_player import GreedyPlayer

N = 5


class AggressivePlayer(GreedyPlayer):

    def move(self, go, piece_type):
        greedy_moves, max_group_size = self.get_greedy_moves(go, piece_type)
        move = random.choice(greedy_moves)



if __name__ == '__main__':
    board_reader = BoardReader()
    piece_type, previous_board, current_board = board_reader.read_board()

    go = GO(N)
    go.set_board(piece_type, previous_board, current_board)

    my_player = AggressivePlayer()
    move = my_player.move(go, piece_type)

    board_writer = BoardWriter()
    board_writer.write_move(move)
