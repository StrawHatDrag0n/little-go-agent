import random
from board_reader import BoardReader
from board_writer import BoardWriter
from exceptions import DeadPieceNotPresentException
from go import GO
from player import Player

N = 5


class GreedyPlayer(Player):
    def __init__(self):
        self.type = 'greedy'
        super(GreedyPlayer, self).__init__()

    def get_greedy_moves(self, go, piece_type):
        groups = go.get_enemy_groups(piece_type)
        if not groups:
            return list(go._get_legal_moves(piece_type).keys()), 0
        # This is the group of enemies with max size
        max_group = max(groups, key=lambda group: len(group))
        greedy_moves = list()
        for move in max_group:
            # We get the neighbours of the max group of enemies
            neighbours = go.neighbors(*move)
            for position in neighbours:
                if go.valid_place_check(*position, piece_type, test_check=True):
                    greedy_moves.append(position)
        return greedy_moves, len(max_group)

    def move(self, go, piece_type):
        # go.visualize_board()
        greedy_moves, _ = self.get_greedy_moves(go, piece_type)
        if not greedy_moves:
            return 'PASS'
        return random.choice(greedy_moves)


if __name__ == '__main__':
    board_reader = BoardReader()
    piece_type, previous_board, current_board = board_reader.read_board()
    move_number = board_reader.get_move_number(current_board, previous_board)
    go = GO(N)
    go.n_move = move_number
    go._set_board(piece_type, previous_board, current_board)

    my_player = GreedyPlayer()
    move = my_player.move(go, piece_type)

    board_writer = BoardWriter()
    board_writer.write_move(move)

