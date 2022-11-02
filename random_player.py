import random

from board_reader import BoardReader
from board_writer import BoardWriter
from host import GO


class RandomPlayer(object):
    def __init__(self):
        self.type = 'random'

    def move(self, go, piece_type):
        '''
        Get one input.

        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''
        possible_placements = list(go._get_legal_moves(piece_type))
        if not possible_placements:
            return "PASS"
        else:
            return random.choice(possible_placements)


if __name__ == "__main__":
    N = 5
    board_reader = BoardReader()
    piece_type, previous_board, board = board_reader.read_board()

    go = GO(N)
    go._set_board(piece_type, previous_board, board)
    player = RandomPlayer()
    action = player.get_input(go, piece_type)

    board_writer = BoardWriter()
    board_writer.write_move(action)
