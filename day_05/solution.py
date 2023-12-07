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
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

etc.

*** also has sections:
fertilizer-to-water map
water-to-light map
light-to-temperature map
temperature-to-humidity map
humidity-to-location map
'''

# Break text into blocks starting with ["sometext: ...", "othertext: ...", "moretext: ...", etc.]
section_blocks_list = puzzle_txt.split("\n\n")


# ---------------------------------------------------------------------------------------------------------------------
#%% Functions

def build_sequence_dict(src_number, range_map_per_section_lut, search_seq_list):
    
    # Fill out first 'src' key, so we can reference it in our loop, as though we found it on a 'previous iteration'
    first_key = search_seq_list[0]
    seq_dict = {first_key: src_number}
    
    # Loop over all src-to-dst pairs, in proper sequence
    for src_key, dst_key in zip(search_seq_list[:-1], search_seq_list[1:]):
        
        # Get range src/dst start/end listings for the current src-to-dst section
        section_key = (src_key, dst_key)
        range_map_listing = range_map_per_section_lut[section_key]

        # Get src number for current src-to-dst check
        src_num = seq_dict[src_key]
        
        # Check if src number is in one of the range listings
        is_in_range = False
        for each_listing_dict in range_map_listing:
            
            # Check if the src number overlaps the source range
            src_start, src_end = each_listing_dict["src_start"], each_listing_dict["src_end"]
            is_in_range = src_start <= src_num <= src_end
            if is_in_range:
                
                # Find the corresponding destination number in the destination range
                start_delta = src_num - src_start
                dst_start = each_listing_dict["dst_start"]
                dst_entry = dst_start + start_delta
                
                # Store number for give destination (will be the 'src' key for the next iteration)
                seq_dict[dst_key] = dst_entry
                break
            
            pass
        
        # If we don't find a range match, then the dst number is equal to the src number
        if not is_in_range:
            seq_dict[dst_key] = src_num
        
        pass
    
    return seq_dict


# ---------------------------------------------------------------------------------------------------------------------
#%% Preprocessing

# Get seed numbers (all on first line) for part 1
seeds_line_str = section_blocks_list[0]
_, seed_num_strs_list = seeds_line_str.split(":")
seed_nums_list = [int(num_str) for num_str in seed_num_strs_list.strip().split(" ")]

# Get all range values for each 'source-to-destination' section
range_map_per_section_lut = {}
for section_block_str in section_blocks_list[1:]:
    
    # Break apart section block so we can get range strings and section naming
    block_lines_list = section_block_str.splitlines()
    src_to_dst_name, _ = block_lines_list[0].split(" ")
    src_name, dst_name = src_to_dst_name.split("-to-")
    
    # Grab all range listing from each section
    new_range_listing = []
    for each_range_line_str in block_lines_list[1:]:
        dst_start, src_start, range_len = [int(item) for item in each_range_line_str.split(" ")]
        src_end = src_start + range_len - 1
        dst_end = dst_start + range_len - 1
        new_range_entry = {"src_start": src_start, "src_end": src_end,
                           "dst_start": dst_start, "dst_end": dst_end}
        new_range_listing.append(new_range_entry)
    
    # Store all listing for each x-to-y section
    section_key = (src_name, dst_name)
    range_map_per_section_lut[section_key] = new_range_listing


# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 1

# Hard-code search sequence
search_seq = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]

# Build sequence number dict for every seed
seed_seq_dict = {}
for each_seed_num in seed_nums_list:
    seed_seq_dict[each_seed_num] = build_sequence_dict(each_seed_num, range_map_per_section_lut, search_seq)

# Pull out the location number for every seed so we can get the minimum to answer part 1
location_nums_list = []
for _, each_seq_dict in seed_seq_dict.items():
    location_nums_list.append(each_seq_dict["location"])
answer_1 = min(location_nums_list)
print("Part 1:", answer_1)


# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 2

# Can't solve part 2 in straightforward way, because seed range is too large, takes too long!

# Considered working backwards:
# - Pick smallest location number (start at 0)
# - Work through sequence in reverse to find corresponding seed number
# - If seed number is in our given listing, then we're done! The location number we started with is the answer
# - If the seed number doesn't land in our listing, increment the location by 1 and repeat the process
#   -> This still takes too long!!!


answer_2 = None
print("Part 2:", answer_2)

