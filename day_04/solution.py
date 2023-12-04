#!/usr/bin/env python3

# ---------------------------------------------------------------------------------------------------------------------
#%% Load data

use_test = False
data_path = "test.txt" if use_test else "input.txt"
with open(data_path) as infile:
    puzzle_txt = infile.read()
    if use_test: print("*** USING TEST ***")

'''
Input looks like:
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
etc.
'''

lines = puzzle_txt.splitlines()


# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 1

num_matches_per_card_list = []
points_per_card_list = []
for each_line in lines:
    
    # Break line: "Card 1: 1 2 3 4 | 5 6 7 8" -> "Card 1:", "1 2 3 4 | 5 6 7 8"
    #  ...cont'd:  " 1 2 3 4 | 5 6 7 8" -> " 1 2 3 4", " 5 6 7 8"
    card_num_str, number_strs = each_line.split(":")
    winning_nums_str, our_nums_str = number_strs.split("|")
    
    # Remove trails spaces and double-spaces (occurs when we have single-digit numbers)
    winning_nums_str = winning_nums_str.replace("  ", " ").strip()
    our_nums_str = our_nums_str.replace("  ", " ").strip()
    
    # Create set out of numbers, so we can find matches (set intersection)
    win_num_set = set(int(item) for item in winning_nums_str.split(" "))
    our_num_set = set(int(item) for item in our_nums_str.split(" "))
    matching_num_set = our_num_set.intersection(win_num_set)
    
    # *** Record number of matches for part 2 ***
    num_matches = len(matching_num_set)
    num_matches_per_card_list.append(num_matches)
    
    # Count points per line (i.e. per card)
    num_points = 2 ** (num_matches - 1) if num_matches > 0 else 0
    points_per_card_list.append(num_points)

answer_1 = sum(points_per_card_list)
print("Part 1:", answer_1)


# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 2

# Set up count of how many cards we have (we start with 1 of every card)
num_cards = len(num_matches_per_card_list)
total_num_card_copies = {(idx + 1): 1 for idx in range(num_cards)}

for list_idx, each_num_matches in enumerate(num_matches_per_card_list):
    
    # Check how many copies of the given card we already have (from previous runs)
    card_idx = list_idx + 1
    number_of_base_card = total_num_card_copies[card_idx]
    
    # Make 'N' copies of later cards according to number of matches (N is number of copies of given card)
    for k in range(each_num_matches):
        card_copy_idx = card_idx + k + 1
        total_num_card_copies[card_copy_idx] += number_of_base_card
    
    pass

answer_2 = sum(total_num_card_copies.values())
print("Part 2:", answer_2)

