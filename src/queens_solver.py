import math
from backtracker import solve

LINKED_IN_COLORS = ['#bb9ae9', '#f2cf89', '#f2cf89', '#b9e495', '#dfdfdf', '#e9815d', '#e9815d', '#b6b49b']
PRINTABLE_COLORS = ['31', '32', '33', '34', '35', '36', '37', '93', '94', '95', '96']

def get_grid_size():
    try:
        size = int(input("Enter the size of the grid (N): "))
        if size <= 0:
            raise ValueError("Size must be a positive integer.")
        return size
    except ValueError as e:
        print(f"Invalid input: {e}")
        return get_grid_size()

def get_colors(grid_size):
    print('Enter the colors for each column in the row and then press enter. Use the same one (1) character for each color.', end='\n')
    colors = []
    color_key = {}
    for i in range(grid_size):
        color = input(f"Enter color for column {i + 1}: ")
        if len(color) != grid_size:
            print(f"Invalid input: Each row must be {grid_size} characters long.")
            print("Please enter the colors again.")
            return get_colors(grid_size)
        for character in color:
            if character not in color_key:
                color_key[character] = len(color_key) + 1
            colors.append(color_key[character])
    return colors

class Configuration:
    def __init__(self, grid_size, colors, queens=None, color_key=None, next_queen_row=0):
        self.grid_size = grid_size
        self.colors = colors
        self.color_key = color_key
        self.queens = queens if queens is not None else int('0' * (grid_size * grid_size), 2)
        self.next_queen_row = next_queen_row

        if self.color_key is None:
            self.color_key = dict()
            for c in set(colors):
                mask = ''
                for v in colors:
                    if c == v:
                        mask = '1' + mask
                    else:
                        mask = '0' + mask
                self.color_key[int(c)] = int(mask, 2)

        if self.grid_size <= 0:
            raise ValueError("Grid size must be a positive integer.")
        if len(self.colors) != self.grid_size * self.grid_size:
            raise ValueError("The number of colors must be equal to grid_size * grid_size.")

    def is_valid(self):
        if self.count_number_in_mask(self.queens) > self.grid_size:
            return False

        for i in range(self.grid_size):
            row_mask = int('1' * self.grid_size, 2) << (i * self.grid_size)
            if self.count_number_in_mask(row_mask & self.queens) > 1:
                return False

            col_mask = int(('0' * i + '1' + '0' * (self.grid_size - (i + 1))) * self.grid_size, 2)
            if self.count_number_in_mask(col_mask & self.queens) > 1:
                return False

            color_mask = self.color_key[i + 1]
            if self.count_number_in_mask(color_mask & self.queens) > 1:
                return False
            
            for j in range(self.grid_size):
                this_square = 1 << (i * self.grid_size + j)
                if self.count_number_in_mask(this_square & self.queens) == 1:
                    has_above = i > 0
                    has_below = i < self.grid_size - 1
                    has_left = j > 0
                    has_right = j < self.grid_size - 1

                    top_left = 1 << (i - 1) * self.grid_size + (j - 1) if has_above and has_left else 0
                    top_right = 1 << (i - 1) * self.grid_size + (j + 1) if has_above and has_right else 0
                    bottom_left = 1 << (i + 1) * self.grid_size + (j - 1) if has_below and has_left else 0
                    bottom_right = 1 << (i + 1) * self.grid_size + (j + 1) if has_below and has_right else 0

                    if self.count_number_in_mask(top_left & self.queens) == 1:
                        return False
                    if self.count_number_in_mask(top_right & self.queens) == 1:
                        return False
                    if self.count_number_in_mask(bottom_left & self.queens) == 1:
                        return False
                    if self.count_number_in_mask(bottom_right & self.queens) == 1:
                        return False
        return True

    def get_next_configurations(self):
        if self.is_solved():
            return []
        result = []
        for i in range(self.next_queen_row * self.grid_size, (self.next_queen_row * self.grid_size) + self.grid_size):
            if self.queens & (1 << i) == 0:
                new_queens = self.queens | (1 << i)
                new_configuration = Configuration(self.grid_size, self.colors, new_queens, self.color_key, math.floor(i / self.grid_size) + 1)
                if new_configuration.is_valid():
                    result.append(new_configuration)
        return result

    def is_solved(self):
        return self.count_number_in_mask(self.queens) == self.grid_size        

    def __str__(self):
        result = ""
        for i in range(self.grid_size * self.grid_size):
            if i % self.grid_size == 0:
                result += "\n"
            character = '■'
            if self.queens & (1 << i):
                character = 'Q'
            result += "\033[{}m{}\033[00m ".format(PRINTABLE_COLORS[self.colors[i] - 1], character)
        return result

    def mask_to_string(self, mask):
        result = ""
        for i in range(self.grid_size * self.grid_size):
            if i % self.grid_size == 0:
                result += "\n"
            character = '.'
            if mask & (1 << i):
                character = '■'
            result += character + " "
        return result

    def count_number_in_mask(self, mask):
        count = 0
        while mask > 0:
            count += mask & 1
            mask >>= 1
        return count

def solve_queens():
    grid_size = get_grid_size()
    colors = get_colors(grid_size)

    configuration = Configuration(grid_size, colors)
    print("\nInitial configuration:")
    print(configuration)
    result = solve(configuration)
    if result:
        print("\nSolution found:")
        print(result)
    else:
        print("\nNo solution found.")
