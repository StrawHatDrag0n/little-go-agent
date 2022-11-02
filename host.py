import argparse
import os

import ipdb

from board_reader import BoardReader
from board_writer import BoardWriter
from go import GO


class Host(object):
    """
    This is host written by Yash Deepak Vaidya
    """
    def __init__(self, num_games=2, player_1_agent='./greedy_player.py', player_2_agent='./alpha_beta_player.py'):
        self.num_games = num_games
        self.player_1_agent = player_1_agent
        self.player_2_agent = player_2_agent

    @classmethod
    def _clean_input(cls):
        try:
            os.system('rm input.txt')
        except Exception as e:
            pass
    @classmethod
    def _clean_output(cls):
        try:
            os.system('rm output.txt')
        except Exception as e:
            pass
    @classmethod
    def _init_clean_up(cls):
        try:
            os.system('rm output.txt')
            os.system('rm input.txt')
        except Exception as e:
            pass
    @classmethod
    def _init_board(cls, init_board_path='./init/input.txt'):
        os.system(f'cp {init_board_path} input.txt')

    def play_player(self, board_size, moves, player_agent):
        # -1 indicates that the game is going on
        result = -1

        # This will write output.txt
        # if player_agent == self.player_2_agent:
        #     os.system(f'python -m cProfile -s cumtime {player_agent}')
        # else:
        os.system(f'python {player_agent}')
        board_reader = BoardReader()
        piece_type, previous_board, current_board = board_reader.read_board()

        go = GO(board_size)
        go._set_board(piece_type, previous_board, current_board)
        go.n_move = moves

        action, i, j = board_reader.read_move()

        self.log(f'{self.num_games}, {player_agent}, {action},  {(i, j)}\n')
        if action == 'MOVE':
            success, error = go.play_piece(i, j, piece_type)
            if not success:
                self.log(f'{self.num_games}: {error}')
                print(f'Invalid move: {i}, {j}')
                return (3 - piece_type), moves
            go.died_pieces = go._remove_dead_pieces(3 - piece_type)
        self.log(go.encode_board(delim='\n'))
        if go.game_end(piece_type, action):
            result = go._judge_winner()
            return result, -1

        if action == 'PASS':
            go.previous_board = go.board

        moves += 1

        board_writer = BoardWriter()
        board_writer.write_board(3 - piece_type, go.previous_board, go.board)

        return result, moves

    def get_players(self):
        if self.num_games % 2:
            return self.player_1_agent, self.player_2_agent
        return self.player_2_agent, self.player_1_agent

    def display_board(self, board_size=5):
        board_reader = BoardReader()
        piece_type, previous_board, current_board = board_reader.read_board()

        go = GO(board_size)
        go._set_board(piece_type, previous_board, current_board)
        go._visualize_board()

    def log(self, log_line):
        with open('log.txt', 'a') as log_file:
            log_file.write(log_line)

    def clean_log(self):
        os.system('rm log.txt')

    def play_async(self, board_size=5, verbose=False):
        wins = {
            self.player_2_agent: 0,
            self.player_1_agent: 0
        }
        self.clean_log()
        while self.num_games:
            self._init_clean_up()
            self._init_board()
            moves = 0
            # Alternate players between black and white pieces
            player_1, player_2 = self.get_players()
            print(f'{self.num_games}:{player_1} is black and {player_2} is white')
            players = {
                1: player_1,
                2: player_2
            }
            # Single game loop
            while True:
                print(f'player 1: {player_1}')
                result, moves = self.play_player(board_size, moves, player_1)
                if result != -1:
                    self.display_board(board_size)
                    print(result)
                    wins[players[result]] += 1
                    break
                if verbose:
                    self.display_board(board_size)
                    print()
                print(f'player 2: {player_2}')
                result, moves = self.play_player(board_size, moves, player_2)
                if result != -1:
                    self.display_board(board_size)
                    print(result)
                    wins[players[result]] += 1
                    break
            self.num_games -= 1
        print(wins)
        self._init_clean_up()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_games', '-ng', type=int, help="number of games", default=1)
    parser.add_argument('--verbose', '-v', type=bool, help="verbose", default=False)
    args = parser.parse_args()
    host = Host(args.num_games)
    host.play_async(5, args.verbose)
