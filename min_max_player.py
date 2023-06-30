from copy import deepcopy
from board_reader import BoardReader
from board_writer import BoardWriter
from go import GO
from min_max_search_tree import MinMaxSearchTree
from player import Player

N = 5


class MinMaxPlayer(Player):

    initial_moves = [
        (1, 1),
        (1, 3),
        (3, 3),
        (3, 2),
        (1, 2),
        (3, 2)
    ]

    def __init__(self, move_number=0, depth=2, branching_factor=10):
        self.move_number = move_number
        self.depth = depth
        self.branching_factor = branching_factor

        self.search_tree: MinMaxSearchTree = None

    def search_minimax(self, go, piece_type):
        self.search_tree = MinMaxSearchTree(deepcopy(go), piece_type, self.move_number, depth=self.depth,
                                            branching_factor=self.branching_factor)
        self.search_tree.search()

    def initial_move(self, go, piece_type):
        moves = go._get_legal_moves(piece_type)
        for initial_move in self.initial_moves:
            if initial_move in moves:
                return initial_move
        return None

    def max_move(self, go, piece_type):
        moves = go._get_legal_moves(GO.opposite(piece_type))
        max_move = None
        max_move_value = 0
        for move in moves:
            go.place_piece(*move, GO.opposite(piece_type))
            dead_pieces = go.find_dead_pieces(piece_type)
            go.place_piece(*move, GO.EMPTY)
            if len(dead_pieces) >= 1 and len(dead_pieces) > max_move_value:
                max_move_value = len(dead_pieces)
                max_move = move
        return max_move

    def move(self, go, piece_type):
        move = self.initial_move(go, piece_type)
        if move:
            return move
        # attack_move = self.max_move(go, GO.opposite(piece_type))
        # print('Attack Move', attack_move)
        # if attack_move:
        #     return attack_move
        # defend_move = self.max_move(go, piece_type)
        # print('Defend Move', defend_move)
        # if defend_move:
        #     return defend_move

        self.search_minimax(go, piece_type)
        search_move = self.search_tree.get_best_move()
        print('Search Move', search_move)
        return search_move


if __name__ == '__main__':
    board_reader = BoardReader()
    piece_type, previous_board, current_board = board_reader.read_board()
    move_number = board_reader.get_move_number(current_board, previous_board)

    go = GO(N)
    go.set_board(piece_type, previous_board, current_board)

    my_player = MinMaxPlayer(move_number)
    move = my_player.move(go, piece_type)
    try:
        board_writer = BoardWriter()
        board_writer.write_move(move)
    except Exception as e:
        print(move)
