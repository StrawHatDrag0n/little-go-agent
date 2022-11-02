import random
import numpy as np
from go import GO
from search_tree_node import SearchTreeNode


class AlphaBetaSearchTreeNode(SearchTreeNode):
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
            board = np.copy(self.go.board)
            GO.place_piece(*move, self.piece_type, board)
            attack_dead_pieces = GO.find_dead_pieces(GO.opposite(self.piece_type), board)
            GO.place_piece(*move, GO.EMPTY, board)
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
            board = np.copy(self.go.board)
            defend_dead_pieces = GO.find_dead_pieces(self.piece_type, board)
            GO.place_piece(*move, GO.EMPTY, board)
            success, error = self.go._valid_place_check(*move, self.piece_type)
            if len(defend_dead_pieces) >= 1 and success:
                defend_moves.append((len(defend_dead_pieces), move))
        return defend_moves

    def get_max_neighbour_moves(self):
        possible_moves = set(self.go._get_legal_moves(self.piece_type).keys())
        max_neighbour_moves = list()
        for move in possible_moves:
            neighbours = self.go._detect_ally_neighbors(*move)
            if len(neighbours) >= 1:
                max_neighbour_moves.append((len(neighbours), move))
        return max_neighbour_moves

    def filter_moves(self, moves):
        m = set(moves)
        moves_to_be_removed = set()
        for move in m:
            self.go._place_piece(*move, self.piece_type)
            possible_moves = list(self.go._get_legal_moves(GO.opposite(piece_type=self.piece_type)).keys())
            for pm in possible_moves:
                self.go._place_piece(*pm, GO.opposite(self.piece_type))
                dead_pieces = self.go._find_dead_pieces(self.piece_type)
                self.go._place_piece(*pm, GO.EMPTY)
                if move in dead_pieces:
                    if pm not in moves_to_be_removed:
                        moves_to_be_removed.add(move)
        for move_to_be_removed in moves_to_be_removed:
            m.remove(move_to_be_removed)
        return list(m)

    def get_moves(self, num_moves=None):
        """
        Calculates the given number of moves possible, given the board.
        """
        possible_moves = set(self.go._get_legal_moves(self.piece_type).keys())
        ad_moves = self.get_defend_moves()
        ad_moves.extend(self.get_attack_moves())
        ad_moves.sort(reverse=True)
        moves = list()
        for _, ad_move, in ad_moves:
            moves.append(ad_move)
            if ad_move in possible_moves:
                possible_moves.remove(ad_move)
        possible_moves = list(possible_moves)
        random.shuffle(possible_moves)
        moves.extend(possible_moves)
        moves = self.filter_moves(moves)

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
        score1 = self.go._score(GO.WHITE)
        score2 = self.go._score(GO.BLACK)
        if self.piece_type == GO.BLACK:
            self.value = score2 - score1
        if self.piece_type == GO.WHITE:
            self.value = score1 - score2
        return self.value

