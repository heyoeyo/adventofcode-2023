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
Time:        34     90     89     86
Distance:   204   1713   1210   1780
'''

line_time, line_dist = puzzle_txt.split("\n")[0:2]


# ---------------------------------------------------------------------------------------------------------------------
#%% Functions

def get_num_record_beaters(race_time, record_distance):
    
    num_record_beaters = 0
    for hold_time_ms in range(1, race_time):
        # Check if given hold time will result in distance that beats the record
        # Note: boat speed (mm/ms) value is equal to hold_time_ms
        time_remaining_ms = race_time - hold_time_ms
        dist_travelled = hold_time_ms * time_remaining_ms
        if dist_travelled > record_distance:
            num_record_beaters += 1
    
    return num_record_beaters


# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 1

# Split time & distance inputs according to part 1 parsing
time_nums = [int(num_str) for num_str in line_time.split()[1:]]
dist_nums = [int(num_str) for num_str in line_dist.split()[1:]]

# Compute product of number of record beating strategies per race
answer_1 = 1
for each_race_time, each_record_dist in zip(time_nums, dist_nums):
    num_record_beaters = get_num_record_beaters(each_race_time, each_record_dist)
    answer_1 *= num_record_beaters

print("Part 1:", answer_1)


# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 2

# Parse time/distance according to part 2 parsing
time_p2 = int("".join(line_time.split()[1:]))
dist_p2 = int("".join(line_dist.split()[1:]))

# Brute-force check runs fast enough for me...
answer_2 = get_num_record_beaters(time_p2, dist_p2)
print("Part 2:", answer_2)

