import random
from copy import deepcopy

from go import GO
from search_tree_node import SearchTreeNode


class MinMaxSearchTreeNode(SearchTreeNode):
    def __init__(self, go, move, node_type, piece_type, board_size=5, value=None):
        self.go = go
        self.board_size = board_size
        self.move = move
        self.node_type = node_type
        self.piece_type = piece_type
        self.value = value
        self.best_child = None
        self.parent = None
        self.children = list()

    def set_best_child(self, child):
        self.best_child = child

    def add_child(self, child):
        self.children.append(child)

    def set_parent(self, parent):
        self.parent = parent

    def __str__(self):
        return f'{self.node_type}: Move {self.move}'

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def display_board(self):
        self.go.visualize_board()

    def get_attack_moves(self):
        """
        Calculates the moves which attacks most pieces
        """
        possible_moves = list(self.go._get_legal_moves(self.piece_type).keys())
        attack_moves = list()
        for move in possible_moves:
            self.go.previous_board = deepcopy(self.go.board)
            self.go.place_piece(*move, self.piece_type)
            self.go.previous_board = deepcopy(self.go.board)
            self.go.previous_board = deepcopy(self.go.board)
            attack_dead_pieces = self.go.find_dead_pieces(GO.opposite(self.piece_type))
            self.go.place_piece(*move, GO.EMPTY)
            if len(attack_dead_pieces) >= 1:
                attack_moves.append((len(attack_dead_pieces), move))
        return attack_moves

    def get_defend_moves(self):
        """
        Calculates the moves which save most pieces
        """
        possible_moves = list(self.go._get_legal_moves(GO.opposite(piece_type=self.piece_type)).keys())
        defend_moves = list()
        for move in possible_moves:
            # Defend Power
            copy_go = deepcopy(self.go)
            copy_go.place_piece(*move, GO.opposite(self.piece_type))
            defend_dead_pieces = copy_go.find_dead_pieces(self.piece_type)
            copy_go.place_piece(*move, GO.EMPTY)
            success, error = self.go.valid_place_check(*move, self.piece_type, test_check=True)
            if len(defend_dead_pieces) >= 1 and success:
                defend_moves.append((len(defend_dead_pieces), move))
        return defend_moves

    def get_moves(self, num_moves=None):
        """
        Calculates the given number of moves possible, given the board.
        """
        possible_moves = set(self.go._get_legal_moves(self.piece_type).keys())
        ad_moves = self.get_attack_moves()
        ad_moves.extend(self.get_defend_moves())
        moves = list()
        for _, ad_move, in ad_moves:
            moves.append(ad_move)
            if ad_move in possible_moves:
                possible_moves.remove(ad_move)
        moves.extend(possible_moves)
        if num_moves is None:
            return moves
        return moves[:num_moves]

    def game_end(self):
        """
        Checks if the game has ended in the node position
        """
        return self.go.game_end(self.piece_type, 'MOVE')

    def evaluate(self):
        """
        Evaluates the board at terminal nodes.
        """
        score1 = self.go.score(GO.WHITE)
        score2 = self.go.score_board(GO.BLACK)
        if self.piece_type == GO.BLACK:
            self.value = score2 - score1
        if self.piece_type == GO.WHITE:
            self.value = score1 - score2
        return self.value

