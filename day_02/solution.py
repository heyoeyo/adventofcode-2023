#!/usr/bin/env python3


#%% Load data

use_test = False
data_path = "test.txt" if use_test else "input.txt"
with open(data_path) as infile:
    puzzle_txt = infile.read()
    if use_test: print("*** USING TEST ***")

'''
Input looks like:
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
...
'''

lines = puzzle_txt.splitlines()

#%% Pre-processing

# Break each line in list of sets of colors
game_sets_list = []
for each_game_str in lines:
    
    color_sets_list = []
    _, all_color_sets_str = each_game_str.split(":")
    for each_set_str in all_color_sets_str.split(";"):        
        each_color_count_dict = {}
        for each_num_color_str in each_set_str.split(","):
            num_str, color_str = each_num_color_str.strip().split(" ")
            each_color_count_dict[color_str] = int(num_str)
        color_sets_list.append(each_color_count_dict)
    
    # Store all sets for the given game string
    game_sets_list.append(color_sets_list)


#%% Solution part 1

# Hard-code the cube limits from part 1
max_cube_counts = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

# Find the game indices whose color sets are <= max hard-coded values
possible_game_idx_list = []
for list_idx, each_game_list in enumerate(game_sets_list):
    
    # Look for sets within each game that would be impossible, to rule out the given game
    is_possible = True
    for each_set_dict in each_game_list:
        
        # Look for color counts that are too high
        for each_color_str, each_count in each_set_dict.items():
            is_possible = each_count <= max_cube_counts[each_color_str]
            if not is_possible: break
        
        # Once we find a single set that is impossible, we can ignore remaining sets
        if not is_possible: break
    
    # Only record possible games
    if is_possible:
        game_idx = list_idx + 1
        possible_game_idx_list.append(game_idx)
    
    pass

answer = sum(possible_game_idx_list)
print("Part 1:", answer)


#%% Solution part 2

game_power_list = []
for each_game_list in game_sets_list:
    
    max_count_dict = {"red": 0, "green": 0, "blue": 0}
    for each_set_dict in each_game_list:
        for each_color_str, each_count in each_set_dict.items():
            max_count_dict[each_color_str] = max(each_count, max_count_dict[each_color_str])
    
    each_game_power = 1
    for each_count in max_count_dict.values():
        each_game_power *= each_count
    game_power_list.append(each_game_power)
    pass

answer_2 = sum(game_power_list)
print("Part 2:", answer_2)

