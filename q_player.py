from collections import defaultdict

import pickle as pkl
import numpy as np
import json
from board_reader import BoardReader
from board_writer import BoardWriter
from go import GO

WIN_REWARD = 25.0
DRAW_REWARD = 0.0
LOSS_REWARD = -25.0

N = 5


class QPlayer(object):
    def __init__(self, piece_type=None, alpha=0.5, gamma=0.5, initial_q_value=0.5):
        self.type = 'leaner'
        self.alpha = alpha
        self.gamma = gamma
        self.piece_type = piece_type
        self.q_values = defaultdict(dict)
        self.initial_q_value = initial_q_value

    def _read_q_values(self):
        try:
            with open('q_values.pickle', 'rb') as q_values_file:
                self.q_values = pkl.load(q_values_file)
        except Exception as e:
            pass

    def _write_q_values(self):
        with open('q_values.pickle', 'wb') as q_values_file:
            pkl.dump(self.q_values, q_values_file, protocol=pkl.HIGHEST_PROTOCOL)

    @classmethod
    def create_board_from_encoding(cls, board_encoding: str):
        pcs = board_encoding.strip().split(',')
        row = 0
        board = np.zeros((5, 5))
        for index, pc in enumerate(pcs):
            board[row][index % 5] = int(pc)
            if index % 5 == 0 and index > 5:
                row += 1
        return board

    def Q(self, board_encoding):
        inverse_board_encoding = GO.inverse_board_encoding(board_encoding)

        board = self.create_board_from_encoding(board_encoding)
        inverse_board = self.create_board_from_encoding(inverse_board_encoding)

        q_values = self.q_values.get(board_encoding)
        if q_values is not None: return q_values
        q_values = self.q_values.get(GO.encode_board(board=np.rot90(board, k=1), delim=','))
        if q_values is not None: return q_values
        q_values = self.q_values.get(GO.encode_board(board=np.rot90(board, k=2), delim=','))
        if q_values is not None: return q_values
        q_values = self.q_values.get(GO.encode_board(board=np.rot90(board, k=3), delim=','))
        if q_values is not None: return q_values

        q_values = self.q_values.get(inverse_board_encoding)
        if q_values is not None: return q_values
        q_values = self.q_values.get(GO.encode_board(board=np.rot90(inverse_board, k=1), delim=','))
        if q_values is not None: return q_values
        q_values = self.q_values.get(GO.encode_board(board=np.rot90(inverse_board, k=2), delim=','))
        if q_values is not None: return q_values
        q_values = self.q_values.get(GO.encode_board(board=np.rot90(inverse_board, k=3), delim=','))
        if q_values is not None: return q_values
        q_values = np.full((5, 5), self.initial_q_value, dtype=float)
        return q_values

    def learn(self, result, history_states):
        self._read_q_values()
        if result == 0:
            result_reward = DRAW_REWARD
        elif result != self.piece_type:
            result_reward = LOSS_REWARD
        else:
            result_reward = WIN_REWARD
        max_q_value = -1.0
        for history_state in history_states:
            board, move = history_state
            q_values = self.Q(board)
            if max_q_value < 0:
                q_values[move[0]][move[1]] = result_reward
            else:
                q_values[move[0]][move[1]] = q_values[move[0]][move[1]] * (1 - self.alpha) + self.alpha * self.gamma * max_q_value
            max_q_value = np.max(q_values)
            self.q_values[board] = q_values
        self._write_q_values()

    def select_best_move(self, go, piece_type):
        q_values = self.Q(go._encode_board(delim=','))
        possible_moves = go.get_empty_places()
        max_move = None
        max_q_value = -np.infty
        for i, j in possible_moves:
            if max_q_value < q_values[i][j]:
                max_q_value = q_values[i][j]
                max_move = (i, j)
        return max_move

    def move(self, go, piece_type):
        move = self.select_best_move(go, piece_type)
        if move is None:
            import ipdb
            ipdb.set_trace()
        return move


if __name__ == '__main__':
    board_reader = BoardReader()
    piece_type, previous_board, current_board = board_reader.read_board()
    move_number = board_reader.get_move_number(current_board, previous_board)

    go = GO(N)
    go._set_board(piece_type, previous_board, current_board)

    my_player = QPlayer(move_number)
    move = my_player.move(go, piece_type)
    board_writer = BoardWriter()
    board_writer.write_move(move, True)
