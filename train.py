import numpy as np

from alpha_beta_player import AlphaBetaPlayer
from go import GO
from player import Player
from q_player import QPlayer
from greedy_player import GreedyPlayer
from random_player import RandomPlayer

N = 5


class Train(object):

    @staticmethod
    def _initial_board():
        return np.zeros((5, 5))

    @classmethod
    def play_player(cls, move_number, player: Player, piece_type, previous_board, board, history):
        try:
            go = GO(N)
            go.n_move = move_number
            go._set_board(piece_type, previous_board, board)
            move = player.move(go, piece_type)
            action = 'PASS'
            history.append((GO.encode_board(board, ','), move))
            if not isinstance(move, str):
                action = 'MOVE'
                success, error = go.play_piece(*move, piece_type)
                if not success:
                    return np.copy(go.previous_board), np.copy(go.board), GO.opposite(piece_type)
                go.died_pieces = go._remove_dead_pieces(3 - piece_type)
            if go.game_end(piece_type, action):
                result = go._judge_winner()
                return np.copy(go.previous_board), np.copy(go.board), result
            if action == 'PASS':
                go.previous_board = go.board
            return np.copy(go.previous_board), np.copy(go.board), 0
        except Exception as e:
            print(e, player)

    @classmethod
    def play(cls, player1, player2, train):
        move_number = 0
        board = cls._initial_board()
        previous_board = cls._initial_board()
        player1_history = list()
        player2_history = list()
        while move_number <= 24:
            if move_number % 2:
                previous_board, board, result = cls.play_player(move_number, player2(), GO.WHITE, np.copy(previous_board), np.copy(board), player2_history)
            else:
                previous_board, board, result = cls.play_player(move_number, player1(), GO.BLACK, np.copy(previous_board), np.copy(board), player1_history)
            if result != 0:
                break
            move_number += 1
        go = GO(N)
        go.n_move = move_number
        go._set_board(GO.BLACK, np.copy(previous_board), np.copy(board))
        winner = go._judge_winner()
        # if winner == GO.BLACK and player1 == QPlayer:
        #     print(go.board)
        # if winner == GO.WHITE and player2 == QPlayer:
        #     print(go.board)
        if train and player1 == QPlayer:
            player1_history.reverse()
            player1().learn(winner, player1_history)
        if train and player2 == QPlayer:
            player2_history.reverse()
            player2().learn(winner, player2_history)
        return winner

    @classmethod
    def train(cls, total_games, train=False):
        num_games = 1
        total_games_won = dict()
        total_games_won = {
            RandomPlayer.__name__: 0,
            QPlayer.__name__: 0
        }
        while num_games <= total_games:
            if num_games % 2:
                player1, player2 = RandomPlayer, QPlayer
            else:
                player1, player2 = QPlayer, RandomPlayer
            winner = cls.play(player1, player2, train)
            if winner == GO.BLACK:
                total_games_won[player1.__name__] += 1
                print(f'Black({player1.__name__}) wins game {num_games}')
            elif winner == GO.WHITE:
                total_games_won[player2.__name__] += 1
                print(f'White({player2.__name__}) wins game {num_games}')
            else:
                print('Draw')
            num_games += 1
        print(total_games_won)

if __name__ == '__main__':
    Train.train(1000, True)