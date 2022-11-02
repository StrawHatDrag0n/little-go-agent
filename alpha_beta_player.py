from copy import deepcopy

import numpy as np

from alpha_beta_search_tree import AlphaBetaSearchTree
from board_reader import BoardReader
from board_writer import BoardWriter
from go import GO
from player import Player

N = 5
#   0 1 2 3 4
# 0     E
# 1   C   C
# 2 E       E
# 3   C   C
# 4     E


class AlphaBetaPlayer(Player):

    corners = [
        (2, 2),
        (1, 1),
        (1, 3),
        (3, 1),
        (3, 3),
        (0, 2),
        (2, 0),
        (4, 2),
        (2, 4)
    ]

    def __init__(self, alpha=-np.infty, beta=np.infty, depth=3, branching_factor=10):
        self.alpha = alpha
        self.beta = beta
        self.depth = depth
        self.branching_factor = branching_factor

        self.search_tree: AlphaBetaSearchTree
        super(AlphaBetaPlayer, self).__init__()

    def search_alphabeta(self, go, piece_type):
        self.search_tree = AlphaBetaSearchTree(deepcopy(go), piece_type,
                                               alpha=self.alpha, beta=self.beta,
                                               depth=self.depth, branching_factor=self.branching_factor)
        self.search_tree.search()

    def initial_move(self, go, piece_type):
        moves = go._get_legal_moves(piece_type)
        for corner_move in self.corners:
            if corner_move in moves:
                return corner_move
        return None

    def attack_move(self, go, piece_type):
        possible_moves = list(go._get_legal_moves(piece_type).keys())
        attack_moves = list()
        for move in possible_moves:
            board = np.copy(go.board)
            GO.place_piece(*move, piece_type, board)
            attack_dead_pieces = GO.find_dead_pieces(GO.opposite(piece_type), board)
            GO.place_piece(*move, GO.EMPTY, board)
            if len(attack_dead_pieces) >= 1:
                attack_moves.append((len(attack_dead_pieces), move))
        attack_moves.sort(reverse=True)
        return attack_moves[0][1] if attack_moves else None

    def defend_move(self, go, piece_type):
        possible_moves = list(go.get_empty_places())
        defend_moves = list()
        for move in possible_moves:
            # Defend Power
            board = np.copy(go.board)
            GO.place_piece(*move, GO.opposite(piece_type), board)
            defend_dead_pieces = GO.find_dead_pieces(piece_type, board)
            GO.place_piece(*move, GO.EMPTY, board)
            success, error = go._valid_place_check(*move, piece_type)
            if len(defend_dead_pieces) >= 1 and success:
                defend_moves.append((len(defend_dead_pieces), move))
        defend_moves.sort(reverse=True)
        return defend_moves[0][1] if defend_moves else None

    def move(self, go, piece_type):
        # import ipdb
        # ipdb.set_trace()
        if go.n_move >= 24:
            return 'PASS'
        attack_move = self.attack_move(go, piece_type)
        if attack_move:
            return attack_move
        defend_move = self.defend_move(go, piece_type)
        if defend_move:
            return defend_move
        num_possible_moves = len(go.get_empty_places())
        if num_possible_moves >= 15:
            move = self.initial_move(go, piece_type)
            if move:
                return move
        if num_possible_moves < 10:
            self.depth = 4
        self.search_alphabeta(go, piece_type)
        search_move = self.search_tree.get_best_move()
        return search_move


if __name__ == '__main__':
    board_reader = BoardReader()
    piece_type, previous_board, current_board = board_reader.read_board()
    move_number = board_reader.get_move_number(current_board, previous_board)

    go = GO(N)
    go.n_move = move_number
    go._set_board(piece_type, previous_board, current_board)

    my_player = AlphaBetaPlayer()
    move = my_player.move(go, piece_type)

    board_writer = BoardWriter()
    board_writer.write_move(move, True)
