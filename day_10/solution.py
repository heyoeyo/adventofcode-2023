#!/usr/bin/env python3


# ---------------------------------------------------------------------------------------------------------------------
#%% Load data

input_select = 0
input_names_list = ["input.txt","test1.txt","test2.txt","test3.txt","test4.txt", "test5.txt"]
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
all_pipe_rc_list = [start_rowcol]
rc_dir_list = [((start_r + get_dr(dir_str), start_c + get_dc(dir_str)), dir_str) for dir_str in valid_next_dir]
step_count = 1
while True:
    
    # Record coords of pipe pieces, for part 2
    for each_rowcol_pair, each_dir in rc_dir_list:
        all_pipe_rc_list.append(each_rowcol_pair)
    
    # Step each row/col/dir entry forward according to direction and record next row/col/dir
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
    
    # Check if the points have met up, which is when we stop!
    is_meet_at_r = len(set([r for (r,c), d in rc_dir_list])) == 1
    is_meet_at_c = len(set([c for (r,c), d in rc_dir_list])) == 1
    if is_meet_at_r and is_meet_at_c:
        # Record last row/col entry to all pipes listing for part 2
        all_pipe_rc_list.append(rc_dir_list[0][0])
        break
    
    pass

answer_1 = step_count
print("Part 1:", answer_1)


# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 2

# Approach:
# For any given point, we can decide if we're inside the loop
# by 'firing' a ray from outside the grid and counting how many times
# we pass over an edge of the loop structure.
# If we pass over the loop once, we're inside, a second pass over
# means we're back outside, a third pass means we're back inside etc.
# -> If we have passed the loop an odd number of times by the time
# our ray hits the target point we're checking, then it is inside
# the loop.
# -> This check is complicated by hitting corners! We can avoid this
# by pretending we're checking slightly left/right of each cell,
# so that we never hit straight on to a corner or end up co-linear
# with one of the pipes

# For convenience
num_rows = len(lines)
num_cols = len(lines[0])

# Want to create top-down ray-firing toggle map, which indicates which tiles toggle us in/out of the loop
# -> Assumes rays are fired 'slightly left' of the actual grid cells, so we don't hit corners/colinear pipes
# -> From these assumptions, we only toggle on pipes: 7, J, -
toggle_letters_set = {"7", "J", "-"}
toggle_map_2d = [[0] * num_cols for _ in range(num_rows)]

# Build boolean map indicating position of all loop pipe elements along with toggle map
loop_map_2d = [[False] * num_cols for _ in range(num_rows)]
for row_idx, col_idx in all_pipe_rc_list:
    loop_map_2d[row_idx][col_idx] = True
    pipe_letter = lines[row_idx][col_idx]
    if pipe_letter in toggle_letters_set:
        toggle_map_2d[row_idx][col_idx] = 1

# Determine whether the starting point (letter 'S') is an edge we need to count for toggling
# -> Only counts if the S point corresponds to a 7, J or - pipe
# -> Check (delta y, delta x) of two directions leading from starting point
# -> After sorting, the two (delta y, delta x) pairs are as follows for target letters:
#    7: (0, -1) & (+1, 0),   J: (-1, 0) & (0, -1),  -: (0, -1) & (0, +1)
start_delta_a = [next_a - origin for next_a, origin in zip(all_pipe_rc_list[1], all_pipe_rc_list[0])]
start_delta_b = [next_b - origin for next_b, origin in zip(all_pipe_rc_list[2], all_pipe_rc_list[0])]
delta_a, delta_b = sorted(zip(start_delta_a, start_delta_b))
S_is_a_7 = (delta_a == (0,-1)) and (delta_b == (1, 0))
S_is_a_J = (delta_a == (-1,0)) and (delta_b == (0, -1))
S_is_a_minus = (delta_a == (0,-1)) and (delta_b == (0, 1))
if S_is_a_7 or S_is_a_J or S_is_a_minus:
    toggle_map_2d[start_r][start_c] = 1

# Traverse toggle map from top-to-bottom and find cumulative sum of toggles down each column
traversal_map_2d = [[*toggle_map_2d[0]]]
for row_idx, toggle_map_one_row in enumerate(toggle_map_2d[1:], start=1):
    new_traversal_row = [*traversal_map_2d[row_idx - 1]]
    for col_idx, toggle_value in enumerate(toggle_map_one_row):
        new_traversal_row[col_idx] += toggle_value
    traversal_map_2d.append(new_traversal_row)

# Finally, count up the number of odd entries in the traversal map which aren't also loop pipe cells
debug_interior_map_2d = [[0] * num_cols for _ in range(num_rows)]
interior_cell_count = 0
for row_idx, (traversal_map_one_row, loop_map_one_row) in enumerate(zip(traversal_map_2d, loop_map_2d)):
    for col_idx, (traversal_value, is_loop_cell) in enumerate(zip(traversal_map_one_row, loop_map_one_row)):
        is_interior = (traversal_value % 2) == 1
        if is_interior and not is_loop_cell:
            interior_cell_count += 1
            debug_interior_map_2d[row_idx][col_idx] = 1

answer_2 = interior_cell_count
print("Part 2:", answer_2)
