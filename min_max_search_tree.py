from copy import deepcopy

import numpy as np

from go import GO
from min_max_search_tree_node import MinMaxSearchTreeNode
from search_tree import SearchTree


class MinMaxSearchTree(SearchTree):
    def __init__(self, go, piece_type, move_number, board_size=5, depth=2, branching_factor=10):
        self.go = go

        self.piece_type = piece_type
        self.move_number = move_number

        self.root = MinMaxSearchTreeNode(go, None, 'MAX', self.piece_type, board_size=board_size)

        self.depth = depth
        self.branching_factor = branching_factor

    def max_level_node(self, node, level, piece_type):
        if level >= 2 * self.depth or node.game_end():
            return node.evaluate()
        max_value = -np.infty
        max_value_node = None
        for move in node.get_moves(self.branching_factor):
            child_go: GO = deepcopy(node.go)
            child_go.place_piece(*move, piece_type)
            child_go.previous_board = deepcopy(child_go.board)
            child = MinMaxSearchTreeNode(child_go, move, 'MAX', piece_type=piece_type)
            node.add_child(child)
            child.set_parent(node)
            value = self.min_level_node(child, level + 1, GO.opposite(piece_type))
            if value > max_value:
                max_value = value
                max_value_node = child
        node.set_best_child(max_value_node)
        return max_value

    def min_level_node(self, node: MinMaxSearchTreeNode, level, piece_type):
        if level >= 2 * self.depth or node.game_end():
            return node.evaluate()
        min_value = np.infty
        min_value_node = None
        for move in node.get_moves(self.branching_factor):
            child_go: GO = deepcopy(node.go)
            child_go.place_piece(*move, piece_type)
            child_go.previous_board = deepcopy(child_go.board)
            child = MinMaxSearchTreeNode(child_go, move, 'MIN', piece_type, board_size=5, value=None)
            node.add_child(child)
            child.set_parent(node)
            value = self.max_level_node(child, level+1, GO.opposite(piece_type))
            if value < min_value:
                min_value = value
                min_value_node = child
        node.set_best_child(min_value_node)
        return min_value

    def search(self):
        return self.max_level_node(self.root, 0, self.piece_type)

    def get_best_move(self):
        if self.root.best_child:
            return self.root.best_child.move
        return 'PASS'
