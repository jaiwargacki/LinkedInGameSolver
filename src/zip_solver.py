import copy
from selenium_scraper import Connection
from selenium.webdriver.common.by import By
from backtracker import solve
from shared import Position, extract_position

ZIP_URL = 'https://www.linkedin.com/games/view/zip/desktop'
ZIP_GRID_CLASS = "trail-grid"

MATCH_CHAR = ' %'

SPACE_CHAR = ' '
NEW_LINE_CHAR = '\n'
PATH_CHAR = '■'
WALL_LEFT_RIGHT = '|'
WALL_TOP_BOTTOM = '—'

class Configuration:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.adjacency_matrix = [[0 for _ in range(grid_size * grid_size)] for _ in range(grid_size * grid_size)]
        for row in range(grid_size):
            for col in range(grid_size):
                index = row * grid_size + col
                if row > 0:
                    self.adjacency_matrix[index][index - grid_size] = 1
                if row < (grid_size - 1):
                    self.adjacency_matrix[index][index + grid_size] = 1
                if col > 0:
                    self.adjacency_matrix[index][index - 1] = 1
                if col < (grid_size - 1):
                    self.adjacency_matrix[index][index + 1] = 1
        
        self.dots = dict()
        self.path = []
        self.highest_value = -1
        self.previous_found_value = 0
        self.previous_location = None

    def add_wall(self, position1, position2):
        self.adjacency_matrix[position1.row * self.grid_size + position1.col][position2.row * self.grid_size + position2.col] = 0
        self.adjacency_matrix[position2.row * self.grid_size + position2.col][position1.row * self.grid_size + position1.col] = 0
    
    def add_dot(self, value, position):
        self.dots[position] = value
        if value == 1:
            self.path.append(position)
            self.previous_location = position
            self.previous_found_value = 1
        if value > self.highest_value:
            self.highest_value = value

    def __repr__(self):
        result = ''
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                index = row * self.grid_size + col
                current_position = Position(row, col)

                next_char = '.'
                if current_position in self.dots:
                    next_char = self.dots[current_position]
                elif current_position in self.path:
                    next_char = PATH_CHAR

                result += str(next_char).ljust(2, SPACE_CHAR)

                right_position = Position(row, col + 1) if col < self.grid_size - 1 else None
                if right_position:
                    right_char = SPACE_CHAR
                    if self.adjacency_matrix[index][index + 1] == 1 \
                            and abs((self.path.index(current_position) if current_position in self.path else -1) \
                            - (self.path.index(right_position) if right_position in self.path else -1)) == 1:
                        right_char = PATH_CHAR
                    elif self.adjacency_matrix[index][index + 1] == 0:
                        right_char = WALL_LEFT_RIGHT

                    result += right_char + SPACE_CHAR
            if row < self.grid_size - 1:
                result += NEW_LINE_CHAR
                for col in range(self.grid_size):
                    index = row * self.grid_size + col
                    next_char = SPACE_CHAR
                    current_position = Position(row, col)
                    down_position = Position(row + 1, col) if row < self.grid_size - 1 else None
                    if self.adjacency_matrix[index][index + self.grid_size] == 0:
                        next_char = WALL_TOP_BOTTOM
                    elif abs((self.path.index(current_position) if current_position in self.path else -1) \
                            - (self.path.index(down_position) if down_position in self.path else -1)) == 1:
                        next_char = PATH_CHAR
                    result += next_char + (SPACE_CHAR * 3)
            result += NEW_LINE_CHAR
        return result

    def next_configuration_helper(self, new_location):
        if new_location in self.path:
            return None
        dot_value = self.dots.get(new_location, 0)
        if dot_value == 0 or dot_value == self.previous_found_value + 1:
            new_configuration = copy.deepcopy(self)
            new_configuration.previous_location = new_location
            new_configuration.path.append(new_location)
            new_configuration.previous_found_value += 1 if dot_value > 0 else 0
            return new_configuration
        return None

    def is_valid(self):
        return True

    def get_next_configurations(self):
        if self.is_solved():
            return []
        result = []

        index = self.previous_location.row * self.grid_size + self.previous_location.col
        if self.previous_location.row > 0 and self.adjacency_matrix[index][index - self.grid_size] == 1:
            new_configuration = self.next_configuration_helper(Position(self.previous_location.row - 1, self.previous_location.col))
            if new_configuration:
                result.append(new_configuration)
        if self.previous_location.row < (self.grid_size - 1) and self.adjacency_matrix[index][index + self.grid_size] == 1:
            new_configuration = self.next_configuration_helper(Position(self.previous_location.row + 1, self.previous_location.col))
            if new_configuration:
                result.append(new_configuration)
        if self.previous_location.col > 0 and self.adjacency_matrix[index][index - 1] == 1:
            new_configuration = self.next_configuration_helper(Position(self.previous_location.row, self.previous_location.col - 1))
            if new_configuration:
                result.append(new_configuration)
        if self.previous_location.col < (self.grid_size - 1) and self.adjacency_matrix[index][index + 1] == 1:
            new_configuration = self.next_configuration_helper(Position(self.previous_location.row, self.previous_location.col + 1))
            if new_configuration:
                result.append(new_configuration)
        
        return result

    def is_solved(self):
        return self.previous_found_value == self.highest_value and len(self.path) == self.grid_size * self.grid_size

def scrape_linked_in() -> Configuration:
    connection = Connection(ZIP_URL, ZIP_GRID_CLASS).open()
    
    size_element = connection.driver.find_element("class name", ZIP_GRID_CLASS)
    style = size_element.get_attribute("style")
    grid_size = int(style.split(';')[0].split(':')[1].strip())

    configuration = Configuration(grid_size)
    row = 0
    col = 0
    for i, div in connection.get_game_elements():
        number_divs = div.find_elements(By.CLASS_NAME, 'trail-cell-content')
        if number_divs:
            configuration.add_dot(int(number_divs[0].get_attribute('innerHTML').strip()), Position(row, col))

        wall_helper = [['right', 0, 1], ['left', 0, -1], ['up', 1, 0], ['down', -1, 0]] # TODO: need to test up and down walls
        for wall in wall_helper:
            wall_elements = div.find_elements(By.CLASS_NAME, f'trail-cell-wall--{wall[0]}')
            if wall_elements:
                configuration.add_wall(Position(row, col), Position(row + wall[1], col + wall[2]))

        col += 1
        if col >= grid_size:
            col = 0
            row += 1

    connection.close()
    return configuration

def solve_zip():
    configuration = scrape_linked_in()
    print("Starting configuration:")
    print(configuration)

    result = solve(configuration)
    if result:
        print("\nSolution found:")
        print(result)
    else:
        print("\nNo solution found.")