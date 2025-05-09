from queens_solver import Configuration

def test_count_number_in_mask_0_1():
    config = Configuration(2, [1, 2, 3, 4])

    mask = int('0', 2)
    expected_count = 0
    actual_count = config.count_number_in_mask(mask)
    assert actual_count == expected_count, f"Expected {expected_count}, but got {actual_count}"

def test_count_number_in_mask_0_2():
    config = Configuration(2, [1, 2, 3, 4])

    mask = int('000000000', 2)
    expected_count = 0
    actual_count = config.count_number_in_mask(mask)
    assert actual_count == expected_count, f"Expected {expected_count}, but got {actual_count}"

def test_count_number_in_mask_1():
    config = Configuration(2, [1, 2, 3, 4])

    mask = int('000001000', 2)
    expected_count = 1
    actual_count = config.count_number_in_mask(mask)
    assert actual_count == expected_count, f"Expected {expected_count}, but got {actual_count}"

def test_count_number_in_mask_larger():
    config = Configuration(2, [1, 2, 3, 4])

    mask = int('010001010', 2)
    expected_count = 3
    actual_count = config.count_number_in_mask(mask)
    assert actual_count == expected_count, f"Expected {expected_count}, but got {actual_count}"

def test_is_valid_row_invalid():
    config = Configuration(3, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    config.queens = int('000101000'[::-1], 2)

    expected_result = False
    actual_result = config.is_valid()
    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"

def test_is_valid_row_valid():
    config = Configuration(3, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    config.queens = int('100001000'[::-1], 2)

    expected_result = True
    actual_result = config.is_valid()
    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"

def test_is_valid_col_invalid():
    config = Configuration(3, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    config.queens = int('100001100'[::-1], 2)

    expected_result = False
    actual_result = config.is_valid()
    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"

def test_is_valid_col_valid():
    config = Configuration(3, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    config.queens = int('100000010'[::-1], 2)

    expected_result = True
    actual_result = config.is_valid()
    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"

def test_is_valid_color_invalid():
    config = Configuration(3, [1, 2, 3, 1, 5, 6, 1, 1, 4])
    config.queens = int('100000010'[::-1], 2)

    expected_result = False
    actual_result = config.is_valid()
    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"

def test_is_valid_color_valid():
    config = Configuration(3, [1, 2, 3, 1, 3, 3, 1, 2, 3])
    config.queens = int('100000010'[::-1], 2)

    expected_result = True
    actual_result = config.is_valid()
    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"

def test_is_valid_diagonal_invalid():
    config = Configuration(3, [1, 2, 3, 1, 2, 3, 1, 2, 3])
    config.queens = int('100010000'[::-1], 2)

    expected_result = False
    actual_result = config.is_valid()
    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"