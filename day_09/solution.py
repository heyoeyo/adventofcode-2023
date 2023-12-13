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
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''

lines = puzzle_txt.strip().split("\n")


# ---------------------------------------------------------------------------------------------------------------------
#%% Preprocessing

# Compute 'hierarchy' of differences per starting line
diffs_per_lines_list = []
for each_line_str in lines:
    
    # Consider the first line of numbers to be a line of differences themselves
    line_diffs_list = [[int(item) for item in each_line_str.split()]]
    
    # Keep computing the differences between consecutive entries of previous line
    while True:
        prev_diffs = line_diffs_list[-1]
        new_diffs = [b - a for a,b in zip(prev_diffs[:-1], prev_diffs[1:])]
        line_diffs_list.append(new_diffs)
        
        # Stop once all entries are zero
        # WARNING: can't just check sum is zero, since there are sometimes negative diffs!
        is_all_zeros = all(val == 0 for val in new_diffs)
        if is_all_zeros:
            break
    
    # Record difference hierarchy for each of the lines of input
    diffs_per_lines_list.append(line_diffs_list)


# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 1

# For each line in input, work backwards through diff hierarchy to find top-most 'new end value'
new_first_line_end_vals_list = []
for each_line_diffs in diffs_per_lines_list:
    
    # Loop backwards over diffs to compute new end values for each diff line
    prev_end_val = 0
    end_vals_per_line_list = []
    for each_diffs in reversed(each_line_diffs):
        prev_end_val = each_diffs[-1] + prev_end_val
        end_vals_per_line_list.append(prev_end_val)
    
    # Only care about storing the top-most (i.e. last list entry, since we're in reverse) new end value for answer
    new_first_line_end_vals_list.append(end_vals_per_line_list[-1])

answer_1 = sum(new_first_line_end_vals_list)
print("Part 1:", answer_1)
    

# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 2

# For each line in input, work backwards through diff hierarchy to find top-most 'new start value'
new_first_line_start_vals_list = []
for each_line_diffs in diffs_per_lines_list:
    
    # Loop backwards again, now computing new start values for each diff line
    prev_start_val = 0
    start_vals_per_line_list = []
    for each_diffs in reversed(each_line_diffs):
        prev_start_val = each_diffs[0] - prev_start_val
        start_vals_per_line_list.append(prev_start_val)
    
    # As before, only store top-most (i.e. last list entry) new start value for answer
    new_first_line_start_vals_list.append(start_vals_per_line_list[-1])

answer_2 = sum(new_first_line_start_vals_list)
print("Part 2:", answer_2)
