#!/usr/bin/env python3

import re


# ---------------------------------------------------------------------------------------------------------------------
#%% Load data

use_test = False
data_path = "test.txt" if use_test else "input.txt"
with open(data_path) as infile:
    puzzle_txt = infile.read()
    if use_test: print("*** USING TEST ***")

'''
Input looks like:
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
etc.
'''

lines = puzzle_txt.splitlines()


# ---------------------------------------------------------------------------------------------------------------------
#%% Pre-processing

# Get coordinates of all symbols & numbers
symbol_row_col_val_list = []
number_row_col1_col2_val_list = []
for row_idx, each_line in enumerate(lines):    
    
    # Find (row, column) index of every non-number/dot ('symbols')
    for col_idx, each_char in enumerate(each_line):
        is_symbol = not (each_char.isdigit() or each_char == ".")
        if is_symbol:
            symbol_row_col_val_list.append((row_idx, col_idx, each_char))
        pass
    pass

    # Find (row, col_start, col_end, value) index of every number
    all_num_matches = re.finditer("\d+", each_line)
    for each_num_match in all_num_matches:
        col_start_idx, col_end_idx_plus1 = each_num_match.span()
        last_col_idx = col_end_idx_plus1 - 1
        value = int(each_num_match.group())
        number_row_col1_col2_val_list.append((row_idx, col_start_idx, last_col_idx, value))
    
    pass


# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 1

# Loop over every number, checking if any of the symbols are nearby
part_numbers_list = []
for num_row_idx, col1_idx, col2_idx, num_value in number_row_col1_col2_val_list:
    
    # Create 'bounding box' coords for the number
    y1, y2 = num_row_idx - 1, num_row_idx + 1
    x1, x2 = col1_idx - 1, col2_idx + 1
    
    # Check for symbol overlap with number bounding-box
    is_overlap = False
    for sym_row_idx, sym_col_idx, _ in symbol_row_col_val_list:
        is_y_overlap = y1 <= sym_row_idx <= y2
        is_x_overlap = x1 <= sym_col_idx <= x2
        is_overlap = is_y_overlap and is_x_overlap
        if is_overlap: break
    
    # Only add numbers if they overlap (are adjacent) with symbols
    if is_overlap:
        part_numbers_list.append(num_value)
    
    pass

answer_1 = sum(part_numbers_list)
print("Part 1:", answer_1)


# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 2

# Filter out the 'gear' symbols: *
gear_row_col_list = [(r, c) for r, c, v in symbol_row_col_val_list if v == "*"]

# Rever of part one, find overlap of gear symbosl with numbers and record them to get 'gear ratio' product
gear_ratios_list = []
for gear_row_idx, gear_col_idx in gear_row_col_list:
    
    # Record all numbers adjacent to the given gear
    adjacent_nums_list = []
    for num_row_idx, col1_idx, col2_idx, num_value in number_row_col1_col2_val_list:
        y1, y2 = num_row_idx - 1, num_row_idx + 1
        x1, x2 = col1_idx - 1, col2_idx + 1
        is_y_overlap = y1 <= gear_row_idx <= y2
        is_x_overlap = x1 <= gear_col_idx <= x2
        if (is_y_overlap and is_x_overlap):
            adjacent_nums_list.append(num_value)
        pass
    
    # Get product of every pair of numbers (not expecting >2 numbers, ignore single numbers they don't count)
    assert len(adjacent_nums_list) < 3, "Got more than 2 adjacent numbers!"
    has_two_nums = len(adjacent_nums_list) == 2
    if has_two_nums:
        gear_ratio = adjacent_nums_list[0] * adjacent_nums_list[1]
        gear_ratios_list.append(gear_ratio)
    pass

answer_2 = sum(gear_ratios_list)
print("Part 2:", answer_2)

