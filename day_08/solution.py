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

# Get all nodes that end with 'A'
start_nodes_set = set(node for node in node_lut.keys() if str(node).endswith("A"))

# Run each node through to target (end with 'Z')
# -> If we hit the target after an integer number of rl_str loops, record the step count
# -> We'll make a wild assumption that all nodes meet at the end of full-integer rl_str loops
# -> Then we can find the 'least-common-multiple' of these steps counts to get answer
rl_length = len(rl_str)
cycle_count_per_start_node = {}
for each_start_node in start_nodes_set:
    
    next_node = each_start_node
    num_steps = None
    for step_idx, each_char in enumerate(cycle(rl_str)):
        
        # Check for end condition of each starting node
        next_node = node_lut[next_node][each_char]
        if not next_node.endswith("Z"):
            continue
        
        # Now that we've hit an end node, check if we've stepped through the rl string an integer number of times
        num_steps = step_idx + 1
        is_mult_of_rl_str = (num_steps % rl_length) == 0
        if is_mult_of_rl_str:
            cycle_count_per_start_node[each_start_node] = num_steps
            break

# Find prime factors using 'LCM by division'
# See: https://www.cuemath.com/numbers/lcm-least-common-multiple/
prime_dividers_set = set()
prime_numbers_list = [2]
step_remainders = sorted(cycle_count_per_start_node.values())
while True:
    
    # Do 'LCM-by-division'
    # -> Try dividing each step count by the next highest prime & store results
    # -> If *any* of the numbers divide, record that prime, product of these primes givens LCM answer
    # -> Record divided step counts if divisible, otherwise do nothing, and repeat process
    prev_prime = prime_numbers_list[-1]
    step_dividers_list = [prev_prime if rem % prev_prime == 0 else 1 for rem in step_remainders]
    keep_prime = any(divider > 1 for divider in step_dividers_list)
    if keep_prime:
        prime_dividers_set.add(prev_prime)
        step_remainders = [rem // divider for rem, divider in zip(step_remainders, step_dividers_list)]
    
    # If we've divided down every step count, we're done!
    stop_dividing = all([rem == 1 for rem in step_remainders])
    if stop_dividing:
        break
    
    # Find next prime number
    for n in range(1 + prev_prime, prev_prime*prev_prime*prev_prime):
        is_not_divisible = all([(n % each_prime) != 0 for each_prime in prime_numbers_list])
        if is_not_divisible:
            prime_numbers_list.append(n)
            break
        pass
    pass

# Multiply the primes together to get LCM
answer_2 = 1
for prime in prime_dividers_set:
    answer_2 = answer_2*prime
print("Part 2:", answer_2)
