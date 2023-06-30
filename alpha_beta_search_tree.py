import time
from copy import deepcopy

import numpy as np

from alpha_beta_search_tree_node import AlphaBetaSearchTreeNode
from go import GO
from search_tree import SearchTree


class AlphaBetaSearchTree(SearchTree):
    def __init__(self, go, piece_type, board_size=5, alpha=-np.infty, beta=np.infty, depth=2,
                 branching_factor=10):
        self.go = go
        self.piece_type = piece_type

        self.root = AlphaBetaSearchTreeNode(go, None, 'MAX', self.piece_type, board_size=board_size)

        self.alpha = alpha
        self.beta = beta
        self.depth = depth
        self.branching_factor = branching_factor

    def max_level_node(self, node, level, piece_type, start_time):
        if level >= 2 * self.depth or node.game_end() or start_time - time.time() > 8:
            return node.evaluate()
        max_value = -np.infty
        max_value_node = None
        moves = node.get_moves(self.branching_factor)
        moves.extend(['PASS'])
        for move in moves:
            child_go: GO = deepcopy(node.go)
            if not isinstance(move, str):
                child_go._place_piece(*move, piece_type)
                child_go.previous_board = np.copy(child_go.board)
            child_go.n_move = node.go.n_move + 1
            child = AlphaBetaSearchTreeNode(child_go, move, 'MAX', piece_type=piece_type)
            node.add_child(child)
            child.set_parent(node)

            value = self.min_level_node(child, level + 1, GO.opposite(piece_type), start_time)

            if value > max_value:
                max_value = value
                max_value_node = child

            self.alpha = max(value, self.alpha)
            if self.beta <= self.alpha:
                break

        node.set_best_child(max_value_node)
        return max_value

    def min_level_node(self, node: AlphaBetaSearchTreeNode, level, piece_type, start_time):
        if level >= 2 * self.depth or node.game_end() or start_time - time.time() > 9:
            return node.evaluate()
        min_value = np.infty
        min_value_node = None
        moves = node.get_moves(self.branching_factor)
        moves.extend(['PASS'])
        for move in moves:
            child_go: GO = deepcopy(node.go)
            if not isinstance(move, str):
                child_go._place_piece(*move, piece_type)
                child_go.previous_board = np.copy(child_go.board)
            child_go.n_move = node.go.n_move + 1
            child = AlphaBetaSearchTreeNode(child_go, move, 'MIN', piece_type, board_size=5, value=None)
            node.add_child(child)
            child.set_parent(node)
            value = self.max_level_node(child, level+1, GO.opposite(piece_type), start_time)
            if value < min_value:
                min_value = value
                min_value_node = child
            self.beta = min(value, self.beta)
            if self.beta <= self.alpha:
                break
        node.set_best_child(min_value_node)
        return min_value

    def search(self):
        start_time = time.time()
        return self.max_level_node(self.root, 0, self.piece_type, start_time)

    def get_best_move(self):
        if self.root.best_child:
            return self.root.best_child.move
        return 'PASS'
