#!/usr/bin/env python3


# ---------------------------------------------------------------------------------------------------------------------
#%% Load data

input_select = 0
input_names_list = ["input.txt","test1.txt","test2.txt","test3.txt","test4.txt"]
data_path = input_names_list[input_select]
with open(data_path) as infile:
    puzzle_txt = infile.read()
    if input_select > 0: print("*** USING TEST ({}) ***".format(input_select))

'''
Input looks like:
.....
.S-7.
.|.|.
.L-J.
.....
'''

lines = puzzle_txt.strip().split("\n")


# ---------------------------------------------------------------------------------------------------------------------
#%% Preprocessing

# Find starting 'S' location (row,column)
col_idx = None
for row_idx, line in enumerate(lines):
    if "S" in line:
        col_idx = line.index("S")
        break
start_rowcol = (row_idx, col_idx)

# Define table for mapping (drow,dcol) pairs to direction terms and vice-versa
# - Assumes 'image' coordinate system: up is -y, down is +y
direction_to_drdc_lut = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
get_dr = lambda direction_str: direction_to_drdc_lut[direction_str][0]
get_dc = lambda direction_str: direction_to_drdc_lut[direction_str][1]

# Define lookup to say which way to move when encountering 'pipes' after a given movement
# - Takes in direction used to 'move into the given pipe'
# - Lookup returns the direction to move 'from the given pipe'
redirect_lut = {
    "up": {"7": "left", "F": "right", "|": "up"},       # L, J, - not usable on up moves
    "down": {"L": "right", "J": "left", "|": "down"},   # F, 7, - not usable on down moves
    "left": {"L": "up", "F": "down", "-": "left"},      # 7, J, | not usable on left moves
    "right": {"7": "down", "J": "up", "-": "right"},    # L, F, |, not usable on right moves
}


# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 1

# Compute first move, by randomly selecting one of the valid directions to move from starting point
start_r, start_c = start_rowcol
valid_next_dir = []
for dir_str in ["up", "right", "down", "left"]:
    
    # Check letter if we step in the given direction
    dr, dc = direction_to_drdc_lut[dir_str]
    r_step = start_r + dr
    c_step = start_c + dc
    letter = lines[r_step][c_step]
    
    # Check if the letter makes sense given the step direction (otherwise it's invalid)
    next_dir_str = redirect_lut[dir_str].get(letter, None)
    is_valid = (next_dir_str is not None)
    if is_valid: valid_next_dir.append(dir_str)

# Step in all valid directions until the paths meet
all_pipe_rc_list = []
rc_dir_list = [((start_r + get_dr(dir_str), start_c + get_dc(dir_str)), dir_str) for dir_str in valid_next_dir]
step_count = 1
while True:
    
    new_rcd_list = []
    for (curr_r, curr_c), prev_dir_str in rc_dir_list:
        letter = lines[curr_r][curr_c]
        next_dir_str = redirect_lut[prev_dir_str][letter]
        dr, dc = direction_to_drdc_lut[next_dir_str]
        
        next_rc = (curr_r + dr, curr_c + dc)
        new_rcd_list.append((next_rc, next_dir_str))
    
    # Record new points for next step
    step_count += 1
    rc_dir_list = new_rcd_list
    
    # Record coords of pipe pieces, for part 2
    all_pipe_rc_list.append([(r,c) for (r,c), d in rc_dir_list])
    
    # Check if the points have met up, which is when we stop!
    is_meet_at_r = len(set([r for (r,c), d in rc_dir_list])) == 1
    is_meet_at_c = len(set([c for (r,c), d in rc_dir_list])) == 1
    if is_meet_at_r and is_meet_at_c:
        break
    
    pass

answer_1 = step_count
print("Part 1:", answer_1)
    

# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 2

# Approach:
# - Make map indicating which cells contain the loop pipes
# - Make map indicating which cells are inside the loop (None if not check, True if inside, False if outside)
# 1. Figure out orientation of loop (i.e. if we move in one direction, is it clockwise or ccw?)
# 2. Traverse loop, marking all points next to pipe (on inside) that are not the pipe itself
#   -> Only need to check -, | pipes
# 3. For all parts marked in (2) look up/down/left/right and mark any non-loop points not already marked
# 4. Repeat step 3 on all newly marked points, keep repeating until we don't add any new points
# 5. Count up all marked points to get answer

# Make lookup for direction to check when looking for 'inside' side of pipe, assuming clockwise-traversal
cw_inside_dir_lut = {"up": "right", "down": "left", "left": "up", "right": "down"}
# ^^^ To get ccw lut, flip values: up<->down, left<->right

answer_2 = None
print("Part 2:", answer_2)
