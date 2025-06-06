import copy
from backtracker import solve
from shared import Position, extract_position

GRID_SIZE = 6

MOON = 'M'
SUN = 'S'
CROSS = 'X'
EQUAL = '='

class Rule:
    def __init__(self, position1, position2, rule_type):
        self.position1 = position1
        self.position2 = position2
        self.rule_type = rule_type

    def __repr__(self):
        return f"{self.rule_type}({self.position1}, {self.position2})"

    def validate(self, value1, value2):
        if value1 is None or value2 is None:
            return True
        elif self.rule_type == CROSS:
            return value1 != value2
        elif self.rule_type == EQUAL:
            return value1 == value2
        return True

class Configuration:
    def __init__(self, squares=None, rules=None, prev_row=0, prev_col=0):
        self.squares = squares if squares else [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.rules = rules if rules else []
        self.prev_row = prev_row
        self.prev_col = prev_col

    def make_move(self, position, value):
        if value not in (MOON, SUN):
            raise ValueError("Invalid value. Use 'M' for Moon or 'S' for Sun.")
        elif self.squares[position.row][position.col] is None:
            self.squares[position.row][position.col] = value
        else:
            print(self)
            print(f"Position {position} already occupied with {self.squares[position.row][position.col]}.")
            raise ValueError("Square already occupied.")

    def add_rule(self, rule):
        if rule.rule_type not in (CROSS, EQUAL):
            raise ValueError("Invalid rule type. Use 'X' for Cross or '=' for Equal.")
        self.rules.append(rule)

    def _validate_window(self, window, max_size=3):
        total_moons = window.count(MOON)
        total_suns = window.count(SUN)
        return not (total_moons > max_size or total_suns > max_size)

    def validate_row_window(self, row, col):
        return self._validate_window(self.squares[row][col:min(col + 3, GRID_SIZE)], 2)

    def validate_col_window(self, row, col):
        return self._validate_window([self.squares[i][col] for i in range(row, min(row + 3, GRID_SIZE))], 2)

    def validate_row(self, row):
        return self._validate_window(self.squares[row], 3)

    def validate_col(self, col):
        return self._validate_window([self.squares[i][col] for i in range(GRID_SIZE)], 3)

    def validate_rule(self, rule):
        return rule.validate(self.squares[rule.position1.row][rule.position1.col], self.squares[rule.position2.row][rule.position2.col])

    def get_next_row_col(self, row, col):
        next_col = col + 1 if col < GRID_SIZE - 1 else 0
        next_row = row if next_col > 0 else row + 1
        if next_row >= GRID_SIZE:
            return GRID_SIZE, GRID_SIZE
        elif self.squares[next_row][next_col] is None:
            return next_row, next_col
        else:
            return self.get_next_row_col(next_row, next_col)

    def new_configuration(self, next_row, next_col, symbol):
        next_moon = Configuration(copy.deepcopy(self.squares), self.rules, next_row, next_col)
        next_moon.make_move(Position(next_row, next_col), MOON)
        if next_moon.is_valid():
            result.append(next_moon)

    def __str__(self):
        result = ""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.squares[row][col] == MOON:
                    result += " \033[36m☾\033[00m "
                elif self.squares[row][col] == SUN:
                    result += " \033[33m☀\033[00m "
                else:
                    result += " \033[37m■\033[00m "
            result += "\n"
        return result

    def is_valid(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if not self.validate_row_window(i, j) or not self.validate_col_window(i, j):
                    return False
            if not self.validate_row(i) or not self.validate_col(i):
                return False

        for rule in self.rules:
            if not self.validate_rule(rule):
                return False
        return True

    def get_next_configurations(self):
        if self.is_solved():
            return []
        result = []

        next_row, next_col = self.get_next_row_col(self.prev_row, self.prev_col)
        if next_row >= GRID_SIZE:
            return []

        for symbol in (MOON, SUN):
            next_config = Configuration(copy.deepcopy(self.squares), self.rules, next_row, next_col)
            next_config.make_move(Position(next_row, next_col), symbol)
            if next_config.is_valid():
                result.append(next_config)

        return result

    def is_solved(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.squares[row][col] is None:
                    return False
        return True 

def get_starting_configuration():
    print("Enter the starting configuration for the Tango game.")
    print("For Moon and Sun, use 'M' and 'S' followed by their positions (e.g., 'M A1' or 'S B2').")
    print("For X and =, use 'X' and '=' followed by their two positions (e.g., 'X A1 B1' or '= C2 C3').\n")
    
    for row in range(1, GRID_SIZE + 1):
        for col in range(1, GRID_SIZE + 1):
            print(f"{chr(64 + row)}{col}", end=" ")
        print()
    
    print("\nFor example, 'M A1 S A3 M A5 S B2 S C1 M C3 M C5 S E1 M E2 S E3 X B4 B5 = B5 B6 X D5 E5 X E4 E5 = E5 E6 X E5 F5'.\n")
    user_input = input("Enter the configuration: ").strip().replace(" ", "").upper()

    index = 0
    configuration = Configuration()
    while index < len(user_input):
        try:
            index_increment = 1
            if user_input[index] == MOON or user_input[index] == SUN:
                configuration.make_move(extract_position(user_input, index + 1), user_input[index])
                index_increment += 2
            elif user_input[index] == CROSS or user_input[index] == EQUAL:
                configuration.add_rule(Rule(extract_position(user_input, index + 1), extract_position(user_input, index + 3), user_input[index]))
                index_increment += 4
            else:
                print("Invalid input. Please try again.")
                return None
            index += index_increment
        except IndexError:
            print("Invalid input. Please try again.")
            return None
    return configuration

def solve_tango():
    configuration = get_starting_configuration()
    if configuration is None:
        return
    print("Starting configuration:")
    print(configuration)

    result = solve(configuration)
    if result:
        print("\nSolution found:")
        print(result)
    else:
        print("\nNo solution found.")