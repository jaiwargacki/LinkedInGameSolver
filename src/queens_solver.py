from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time

import math
from backtracker import solve

LINKED_IN_COLORS = ['#bba3e2', '#ffc992', '#96beff', '#b3dfa0', '#dfdfdf', '#ff7b60', '#e6f388', '#dfa0bf', '#a3d2d8', '#62efea', '#ff93f3', '#8acc6d', '#729aec', '#c387e0', '#ffe04b']

def get_printable_colors():
    printable_colors = []
    for color in LINKED_IN_COLORS:
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        printable_colors.append(f"38;2;{r};{g};{b}")
    return printable_colors

PRINTABLE_COLORS = get_printable_colors()

QUEENS_URL = "https://www.linkedin.com/games/view/queens/desktop/"
START_BUTTON_ID = "launch-footer-start-button"
QUEEN_GRID_ID = "queens-grid"

def scrape_linked_in() -> tuple[int, list[str]]:
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    driver.get(QUEENS_URL)
    time.sleep(1)
    start_button = driver.find_element("id", START_BUTTON_ID)
    start_button.click()
    time.sleep(1)
    board_element = driver.find_element("id", QUEEN_GRID_ID)
    divs = board_element.find_elements("tag name", "div")
    color_map = dict()
    colors = []
    for i, div in enumerate(divs):
        label = div.get_attribute("aria-label")
        if label is None:
            continue

        elements = label.split(", ")
        color = elements[0].split('color ')[1]
        row = elements[1].replace('row ', '')
        col = elements[2].replace('column ', '')

        if color not in color_map:
            color_map[color] = len(color_map) + 1
        colors.append(color_map[color])

    driver.quit()
    grid_size = int(math.sqrt(len(colors)))
    if grid_size * grid_size != len(colors):
        raise ValueError("The number of colors does not form a perfect square grid.")
    return grid_size, colors

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
    grid_size, colors = scrape_linked_in()

    configuration = Configuration(grid_size, colors)
    print("\nInitial configuration:")
    print(configuration)
    result = solve(configuration)
    if result:
        print("\nSolution found:")
        print(result)
    else:
        print("\nNo solution found.")
