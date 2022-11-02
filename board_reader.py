import numpy as np
class BoardReader(object):
    def __init__(self, board_size: int = 5, file_path: str = 'input.txt'):
        self.board_size = board_size
        self.file_path = file_path

        self.piece_type = None
        self.previous_board = None
        self.current_board = None

    def read_board(self):
        with open(self.file_path, 'r') as f:
            lines = f.readlines()

            self.piece_type = int(lines[0])
            self.previous_board = np.array([np.array(list(map(int, line.strip("\n"))))
                                            for line in lines[1:self.board_size + 1]])
            self.current_board = np.array([np.array(list(map(int, line.strip("\n"))))
                                           for line in lines[self.board_size + 1: 2 * self.board_size + 1]])
        return self.piece_type, self.previous_board, self.current_board

    def is_empty(self, board):
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 0:
                    return False
        return True

    def get_move_number(self, current_board, previous_board):
        is_current_board_empty = self.is_empty(current_board)
        is_previous_board_empty = self.is_empty(previous_board)
        if is_current_board_empty and is_previous_board_empty:
            move_number = 0
            with open('move_number.txt', 'w') as move_file:
                move_file.write(f'{move_number}')
        if is_previous_board_empty and not is_current_board_empty:
            move_number = 1
            with open('move_number.txt', 'w') as move_file:
                move_file.write(f'{move_number}')
        try:
            with open('move_number.txt', 'r') as move_file:
                lines = move_file.readlines()
                move_number = 0
                if lines:
                    move_number = int(lines[0].strip('\n'))
        except FileNotFoundError:
            move_number = 0
        return move_number

    def read_move(self):
        with open('output.txt', 'r') as output_file:
            line = output_file.readline()
            if line == 'PASS':
                return 'PASS', -1, -1
            line = line.split(',')
            i = int(line[0])
            j = int(line[1])
            return 'MOVE', i, j
