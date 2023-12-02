#!/usr/bin/env python3


#%% Load data

use_test = False
data_path = "test2.txt" if use_test else "input.txt"
with open(data_path) as infile:
    puzzle_txt = infile.read()
    if use_test: print("*** USING TEST ***")
    
lines = puzzle_txt.splitlines()


#%% Solution part 1

line_numbers = []
for each_line in lines:
    
    # Grab all digits from string
    all_digit_strs = [char for char in each_line if char.isdigit()]
    if len(all_digit_strs) == 0:
        continue
    
    # Combine first/last digits into a single integer
    first_last_str = all_digit_strs[0] + all_digit_strs[-1]
    first_last_int = int(first_last_str)
    
    line_numbers.append(first_last_int)

# Sum of all combined line digits is the answer
answer = sum(line_numbers)
print("Part 1:", answer)


#%% Solution part 2

word_to_digit_lut = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "0": 0,
}

line_numbers_2 = []
for each_line in lines:
    
    # Brute-force search for first-most match to lut
    first_matches_list = []
    for each_key, each_digit in word_to_digit_lut.items():
        try:
            each_idx = each_line.index(each_key)
            first_matches_list.append((each_idx, each_digit))
        except ValueError:
            pass
    sorted_first_matches = sorted(first_matches_list)
    _, first_digit = sorted_first_matches[0]
    
    # Reverse string to search for last-most match to lut
    last_matches_list = []
    rev_line = each_line[::-1]
    for each_key, each_digit in word_to_digit_lut.items():
        rev_key = each_key[::-1]
        try:
            each_idx = rev_line.index(rev_key)
            last_matches_list.append((each_idx, each_digit))
        except ValueError:
            pass
    sorted_last_matches = sorted(last_matches_list)
    _, last_digit = sorted_last_matches[0]
    
    # Bundle first/last matches to form 2-digit results
    first_last_int = int(10*first_digit + last_digit)
    line_numbers_2.append(first_last_int)

# Sum of all combined line digits is the answer
answer_2 = sum(line_numbers_2)
print("Part 2:", answer_2)