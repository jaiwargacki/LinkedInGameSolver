class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return f"Position({self.row}, {self.col})"

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

def extract_position(user_input, offset):
    position_str = user_input[offset:offset + 2]
    if len(position_str) != 2:
        raise "Invalid input. Please try again."
    return Position(ord(position_str[0]) - 65, int(position_str[1]) - 1)