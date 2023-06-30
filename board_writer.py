class BoardWriter(object):
    def __init__(self, file_path: str = 'output.txt'):
        self.file_path = file_path

    def write_move(self, move, write_move_number=False):
        if move != 'PASS':
            move = ','.join(map(str, move))
        with open(self.file_path, 'w') as output_file:
            output_file.write(F'{move}')
        if write_move_number:
            try:
                with open('move_number.txt', 'r') as move_file:
                    lines = move_file.readlines()
                    move_number = 0
                    if lines:
                        move_number = int(lines[0].strip('\n'))
                move_number += 2
                with open('move_number.txt', 'w') as move_file:
                    move_file.write(f'{move_number}')
            except:
                with open('move_number.txt', 'w+') as move_file:
                    lines = move_file.readlines()
                    move_number = 0
                    if lines:
                        move_number = int(lines[0].strip('\n'))
                    move_number += 2
                    move_file.write(f'{move_number}')

    def write_board(self, piece_type, previous_board, current_board):
        res = ""
        res += str(piece_type) + "\n"
        for item in previous_board:
            res += "".join([str(x) for x in item])
            res += "\n"

        for item in current_board:
            res += "".join([str(x) for x in item])
            res += "\n"

        with open('input.txt', 'w') as input_file:
            input_file.write(res[:-1])


if __name__ == '__main__':
    board_writer = BoardWriter()
    board_writer.write_move((1,1))