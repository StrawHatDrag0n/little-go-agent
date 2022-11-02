from copy import deepcopy
from collections import defaultdict


# FOR TAs: This files contains code derived from host.py provided in the homework 2 assignment
########################################################################################################################
class GO:
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def __init__(self, board_size=5):
        """
        Go game.

        :param n: size of the board n*n
        """
        self.size = board_size
        self.piece_type_locations = defaultdict(dict)
        self.dead_pieces = set()
        self.verbose = False
        self.n_move = 0
        self.max_move = board_size * board_size - 1
        self.komi = board_size / 2
        self.board = None
        self.previous_board = None

    @classmethod
    def opposite(cls, piece_type):
        return 3 - piece_type

    @classmethod
    def is_eye(cls, i, j, piece_board, board):
        neighbours = cls.neighbors(i, j, board)
        for i, j in neighbours:
            if board[i][j] != piece_board:
                return False
        return True

    def get_enemy_groups(self, piece_type):
        discovered = dict()
        groups = list()
        for position in self.piece_type_locations.get(self.opposite(piece_type), list()):
            if discovered.get(position):
                continue
            discovered[position] = True
            allies = self.ally_dfs(*position)
            for ally in allies:
                discovered[ally] = True
            group = list()
            group.extend(allies)
            groups.append(group)
        return groups

    def _set_board(self, piece_type, previous_board, board):
        '''
        Initialize board status.
        :param previous_board: previous board state.
        :param board: current board state.
        :return: None.
        '''

        # 'X' pieces marked as 1
        # 'O' pieces marked as 2
        for i in range(self.size):
            for j in range(self.size):
                if self.get_piece(i, j, previous_board) == piece_type and self.get_piece(i, j, board) != piece_type:
                    self.dead_pieces.add((i, j))
                else:
                    self._add_piece_to_piece_location(i, j, piece_type)
        self.previous_board = previous_board
        self.board = board

    @classmethod
    def compare_board(cls, board1, board2):
        for i in range(len(board1)):
            for j in range(len(board1)):
                if cls.get_piece(i, j, board1) != cls.get_piece(i, j, board2):
                    return False
        return True

    def copy_board(self):
        '''
        Copy the current board for potential testing.

        :param: None.
        :return: the copied board instance.
        '''
        return deepcopy(self)

    @classmethod
    def neighbors(cls, i, j, board):
        neighbors = []
        # Detect borders and add neighbor coordinates
        if i > 0:
            neighbors.append((i - 1, j))
        if i < len(board) - 1:
            neighbors.append((i + 1, j))
        if j > 0:
            neighbors.append((i, j - 1))
        if j < len(board) - 1:
            neighbors.append((i, j + 1))
        return neighbors

    def _neighbors(self, i, j):
        return self.neighbors(i, j, self.board)

    @classmethod
    def get_piece(cls, i, j, board):
        return board[i][j]

    def _get_piece(self, i, j):
        return self.get_piece(i, j, self.board)

    @classmethod
    def detect_ally_neighbors(cls, i, j, board):
        neighbors = cls.neighbors(i, j, board)
        ally_neighbors = list()
        for neighbor in neighbors:
            if cls.get_piece(*neighbor, board) == cls.get_piece(i, j, board):
                ally_neighbors.append(neighbor)
        return ally_neighbors

    def _detect_ally_neighbors(self, i, j):
        return self.detect_ally_neighbors(i, j, self.board)

    @classmethod
    def detect_neighbor_ally(cls, i, j, board):
        neighbors = cls.neighbors(i, j, board)
        group_allies = []
        for piece in neighbors:
            if cls.get_piece(*piece, board) == cls.get_piece(i, j, board):
                group_allies.append(piece)
        return group_allies

    def _detect_neighbor_ally(self, i, j):
        return self.detect_neighbor_ally(i, j, self.board)

    @classmethod
    def ally_dfs(cls, i, j, board):
        stack = [(i, j)]
        ally_members = set()
        while stack:
            piece = stack.pop()
            ally_members.add(piece)
            neighbor_allies = cls.detect_neighbor_ally(*piece, board)
            for ally in neighbor_allies:
                if ally not in stack and ally not in ally_members:
                    stack.append(ally)
        return ally_members

    def _ally_dfs(self, i, j):
        return self.ally_dfs(i, j, self.board)

    @classmethod
    def find_liberty(cls, i, j, board):
        ally_members = cls.ally_dfs(i, j, board)
        for member in ally_members:
            neighbors = cls.neighbors(*member, board)
            for piece in neighbors:
                if cls.get_piece(*piece, board) == 0:
                    return True
        return False

    def _find_liberty(self, i, j):
        return self.find_liberty(i, j, self.board)

    @classmethod
    def find_dead_pieces(cls, piece_type, board):
        died_pieces = []
        for i in range(len(board)):
            for j in range(len(board)):
                # Check if there is a piece at this position:
                if cls.get_piece(i, j, board) == piece_type:
                    # The piece die if it has no liberty
                    if not cls.find_liberty(i, j, board):
                        died_pieces.append((i, j))
        return died_pieces

    def _find_dead_pieces(self, piece_type):
        return self.find_dead_pieces(piece_type, self.board)

    @classmethod
    def remove_dead_pieces(cls, piece_type, board):
        died_pieces = cls.find_dead_pieces(piece_type, board)
        if not died_pieces:
            return list()
        cls.remove_certain_pieces(died_pieces, board)
        return died_pieces

    def _remove_dead_pieces(self, piece_type):
        return self.remove_dead_pieces(piece_type, self.board)

    @classmethod
    def remove_certain_pieces(cls, positions, board):
        for i, j in positions:
            board[i][j] = 0

    def _remove_certain_pieces(self, positions):
        '''
        Remove the stones of certain locations.

        :param positions: a list containing the pieces to be removed row and column(row, column)
        :return: None.
        '''
        board = self.board
        for i, j in positions:
            piece_type = board[i][j]
            self._remove_piece_from_piece_locations(i, j, piece_type)
            board[i][j] = 0
        self._update_board(board)

    def _remove_piece_from_piece_locations(self, i, j, piece_type):
        for ptype in [GO.EMPTY, GO.BLACK, GO.WHITE]:
            if self.piece_type_locations[ptype].get((i, j)):
                self.piece_type_locations[ptype].pop((i, j))

    def _add_piece_to_piece_location(self, i, j, piece_type):
        for ptype in [GO.EMPTY, GO.BLACK, GO.WHITE]:
            if ptype == piece_type:
                self.piece_type_locations[piece_type][(i, j)] = True
            elif self.piece_type_locations[ptype].get((i, j)):
                self.piece_type_locations[ptype].pop((i, j))

    @classmethod
    def place_piece(cls, i, j, piece_type, board):
        board[i][j] = piece_type

    def _place_piece(self, i, j, piece_type):
        board = self.board
        board[i][j] = piece_type
        self._add_piece_to_piece_location(i, j, piece_type)
        self._update_board(board)

    def _diff(self):
        self.diff_boards(self.board, self.previous_board)

    def play_piece(self, i, j, piece_type):
        '''
        Place a chess stone in the board as a concrete move.

        :param i: row number of the board.
        :param j: column number of the board.
        :param piece_type: 1('X') or 2('O').
        :return: boolean indicating whether the placement is valid.
        '''
        board = self.board
        valid_place, error = self.valid_place_check(i, j, piece_type, self.previous_board, self.board)
        if not valid_place:
            return False, error
        self.previous_board = deepcopy(board)
        board[i][j] = piece_type
        self._add_piece_to_piece_location(i, j, piece_type)
        self._update_board(board)
        return True, None

    @classmethod
    def diff_boards(cls, board1, board2):
        diffs = list()
        for i in range(len(board1)):
            for j in range(len(board1)):
                if cls.get_piece(i, j, board1) != cls.get_piece(i, j, board2):
                    diffs.append((i, j))
        print(diffs)

    @classmethod
    def valid_place_check(cls, i, j, piece_type, previous_board, board, verbose=False):
        # Check if the place is in the board range
        if not (0 <= i < len(board)):
            if verbose:
                print('Invalid placement. row should be in the range 1 to {}.'.format(len(board) - 1))
            return False, 'Invalid placement. row should be in the range 1 to {}.'.format(len(board) - 1)
        if not (0 <= j < len(board)):
            if verbose:
                print('Invalid placement. column should be in the range 1 to {}.'.format(len(board) - 1))
            return False, 'Invalid placement. column should be in the range 1 to {}.'.format(len(board) - 1)

        if board[i][j] != 0:
            if verbose:
                print('Invalid placement. There is already a chess in this position.')
            return False, 'Invalid placement. There is already a chess in this position.'

        test_board = deepcopy(board)
        cls.place_piece(i, j, piece_type, test_board)
        liberty = cls.find_liberty(i, j, test_board)
        if liberty:
            return True, None

        if not liberty:
            if verbose:
                print('Invalid placement. No liberty found in this position.')
            return False, 'Invalid placement. No liberty found in this position.'
        else:
            if cls.compare_board(board, previous_board):
                if verbose:
                    print('Invalid placement. A repeat move not permitted by the KO rule.')
                return False, 'Invalid placement. A repeat move not permitted by the KO rule.'
        return True, None

    def _valid_place_check(self, i, j, piece_type, test_check=False):
        '''
        Check whether a placement is valid.

        :param i: row number of the board.
        :param j: column number of the board.
        :param piece_type: 1(white piece) or 2(black piece).
        :param test_check: boolean if it's a test check.
        :return: boolean indicating whether the placement is valid.
        '''
        board = self.board
        verbose = self.verbose
        if test_check:
            verbose = False

        # Check if the place is in the board range
        if not (0 <= i < len(board)):
            if verbose:
                print('Invalid placement. row should be in the range 1 to {}.'.format(len(board) - 1))
            return False, 'Invalid placement. row should be in the range 1 to {}.'.format(len(board) - 1)
        if not (0 <= j < len(board)):
            if verbose:
                print('Invalid placement. column should be in the range 1 to {}.'.format(len(board) - 1))
            return False, 'Invalid placement. column should be in the range 1 to {}.'.format(len(board) - 1)

        # Check if the place already has a piece
        if board[i][j] != 0:
            if verbose:
                print('Invalid placement. There is already a chess in this position.')
            return False, 'Invalid placement. There is already a chess in this position.'

        # Copy the board for testing
        test_go = self.copy_board()
        test_board = test_go.board

        # Check if the place has liberty
        test_board[i][j] = piece_type
        test_go._update_board(test_board)
        if test_go._find_liberty(i, j):
            return True, None

        # If not, remove the died pieces of opponent and check again
        test_go._remove_dead_pieces(3 - piece_type)
        if not test_go._find_liberty(i, j):
            if verbose:
                print('Invalid placement. No liberty found in this position.')
            return False, 'Invalid placement. No liberty found in this position.'

        # Check special case: repeat placement causing the repeat board state (KO rule)
        else:
            if self.dead_pieces and self.compare_board(self.previous_board, test_go.board):
                if verbose:
                    print('Invalid placement. A repeat move not permitted by the KO rule.')
                return False, 'Invalid placement. A repeat move not permitted by the KO rule.'
        return True, None

    def _update_board(self, new_board):
        '''
        Update the board with new_board

        :param new_board: new board.
        :return: None.
        '''
        self.board = new_board

    def _visualize_board(self):
        self.visualize_board(self.board)

    @classmethod
    def visualize_board(cls, board):
        '''
        Visualize the board.

        :return: None
        '''
        # print(' ', end='')
        # print('-' * len(board) * 2)
        print('  ', end='')
        for i in range(0, len(board)):
            print(f'{i}', end=' ')
        print()
        for i in range(len(board)):
            print(str(i), end=' ')
            for j in range(len(board)):
                if board[i][j] == 0:
                    print(' ', end=' ')
                elif board[i][j] == 1:
                    print('X', end=' ')
                else:
                    print('O', end=' ')
            print()
        # print(' ', end='')
        # print('-' * len(board) * 2)
        print('  ', end='')
        for i in range(0, len(board)):
            print(f'{i}', end=' ')
        print()

    def game_end(self, piece_type, action="MOVE"):
        # Case 1: max move reached
        if self.n_move >= self.max_move:
            return True
        # Case 2: two players all pass the move.
        if self.compare_board(self.previous_board, self.board) and action == "PASS":
            return True
        return False

    @classmethod
    def score(cls, piece_type, board):
        cnt = 0
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == piece_type:
                    cnt += 1
        return cnt

    def _score(self, piece_type):
        return self.score(piece_type, self.board)

    @classmethod
    def judge_winner(cls, komi=0.0, board=None):
        cnt_1 = cls.score(1, board)
        cnt_2 = cls.score(2, board)
        if cnt_1 > cnt_2 + komi:
            return 1
        elif cnt_1 < cnt_2 + komi:
            return 2
        else:
            return 0

    def _judge_winner(self):
        return self.judge_winner(self.komi, self.board)

    @classmethod
    def get_legal_moves(cls, piece_type, previous_board, board):
        legal_moves = dict()
        for i in range(len(board)):
            for j in range(len(board)):
                success, error = cls.valid_place_check(i, j, piece_type,  previous_board, board)
                if success:
                    legal_moves[(i, j)] = True
        return legal_moves

    def _get_legal_moves(self, piece_type):
        return self.get_legal_moves(piece_type, self.previous_board, self.board)

    @classmethod
    def inverse_board_encoding(cls, board_encoding: str):
        res = ''
        for place in board_encoding.split(','):
            if place == '1':
                res += '2'
            elif place == '2':
                res += '1'
            else:
                res += '0'
        return res

    def get_empty_places(self):
        empty_places = dict()
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == GO.EMPTY:
                    empty_places[(i, j)] = True
        return empty_places

    def _encode_board(self, delim=None):
        return self.encode_board(self.board, delim)

    @classmethod
    def encode_board(cls, board, delim=None):
        res = ""
        for item in board:
            res += f"{delim}".join([str(int(x)) for x in item])
            if delim:
                res += delim
        return res[:-1]
########################################################################################################################