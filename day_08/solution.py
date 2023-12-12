#!/usr/bin/env python3


from itertools import cycle

# ---------------------------------------------------------------------------------------------------------------------
#%% Load data

input_select = 0
input_names_list = ["input.txt", "test1.txt", "test2.txt", "test3.txt"]
data_path = input_names_list[input_select]
with open(data_path) as infile:
    puzzle_txt = infile.read()
    if input_select > 0: print("*** USING TEST ({}) ***".format(input_select))

'''
Input looks like:
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
'''

lines = puzzle_txt.strip().split("\n")


# ---------------------------------------------------------------------------------------------------------------------
#%% Preprocessing

# Get navigation string (series of 'R'/'L' characters)
rl_str = lines[0]

# Build lookup table of node names (e.g. 'AAA') to left/right outcomes
node_lut = {}
for each_node_str in lines[2:]:
    node_name, left_right_pair = each_node_str.split(" = ")
    left_node, right_node = left_right_pair.removeprefix("(").removesuffix(")").split(", ")
    node_lut[node_name] = {"L": left_node, "R": right_node}


# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 1

# For clarity
next_node = "AAA"
target_node = "ZZZ"

# Only do part 1 if we have correct nodes! Otherwise fails for part 2 test input...
if (next_node in node_lut) and (target_node in node_lut):
    
    # Traverse the rl sequence using the node lookup table to find target node
    num_steps = None
    for step_idx, each_char in enumerate(cycle(rl_str)):
        next_node = node_lut[next_node][each_char]
        if next_node == target_node:
            num_steps = step_idx + 1
            break
    print("Part 1:", num_steps)
    
else:
    print("Part 1: Skipped, due to invalid input")


# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 2

if input_select == 0:
    print("", "WARNING: Part 2 solution takes forever", sep="\n", flush = True)

# Get all nodes that end with 'A'
next_nodes_set = set(node for node in node_lut.keys() if str(node).endswith("A"))

# Loop through rl sequence as before, but map multiple nodes forward
num_steps = None
for step_idx, each_char in enumerate(cycle(rl_str)):
    
    # Map every node for given character and stop once they all end with 'Z'
    next_nodes_set = set(node_lut[each_node][each_char] for each_node in next_nodes_set)
    is_done = all(node.endswith("Z") for node in next_nodes_set)
    if is_done:
        num_steps = step_idx + 1
        break
    
answer_2 = num_steps
print("Part 2:", answer_2)
