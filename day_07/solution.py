#!/usr/bin/env python3

from collections import Counter


# ---------------------------------------------------------------------------------------------------------------------
#%% Load data

use_test = False
data_path = "test.txt" if use_test else "input.txt"
with open(data_path) as infile:
    puzzle_txt = infile.read()
    if use_test: print("*** USING TEST ***")

'''
Input looks like:
88223 818
66JQ9 398
6T9AT 311
53TT3 43
J6266 762
etc...
'''

lines = puzzle_txt.strip().split("\n")


# ---------------------------------------------------------------------------------------------------------------------
#%% Functions

def get_tiebreaker_scores(cards_list, base15_lut):
    
    ''' Function which interprets each card as a base15 number, which can then be used as a tiebreaker score '''
    
    # Helper function to convert characters (e.g. "A", "7", "J") into integers, according to lut
    char_to_int = lambda char: int(char) if char.isdigit() else base15_lut[char]
    
    # Convert each character into a base15 number using the given lut
    # Example: '32T3K' -> b15 digits: [3, 2, 10, 3, 13] -> place values: [3*15^4, 2*15^3, 10*15^2, 3*15^1, 13*15^0]
    scores_list = []
    for each_card_seq in cards_list:
        b15_digits = [char_to_int(each_char) for each_char in each_card_seq]
        place_values = [digit * (15**place_idx) for place_idx, digit in enumerate(reversed(b15_digits))]
        scores_list.append(sum(place_values))
    
    return scores_list


# ---------------------------------------------------------------------------------------------------------------------
#%% Preprocessing

# Split lines into cards & bids
cards_list, bids_list = zip(*(each_line.split() for each_line in lines))

# Helper used to figure out card seq. strength, by looking at (sorted) count of unique cards
unique_counts_to_strength_lut = {
    (1,1,1,1,1): 0, # all-different
    (1,1,1,2)  : 1, # one-pair
    (1,2,2)    : 2, # two-pair
    (1,1,3)    : 3, # 3-oaK
    (2,3)      : 4, # full-house
    (1,4)      : 5, # 4-oaK
    (5,)       : 6, # 5-oaK
}


# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 1

# Determine 'strength' of each hand, using lookup-table
p1_strength_list = []
for each_card_seq in cards_list:
    card_counts = Counter(each_card_seq)
    sorted_counts = sorted(card_counts.values())
    seq_strength = unique_counts_to_strength_lut[tuple(sorted_counts)]
    p1_strength_list.append(seq_strength)

# Determine the tie-breaker strength of each card
p1_base15_lut = {"A":14, "K":13, "Q":12, "J":11, "T":10}
p1_tiebreaker_list = get_tiebreaker_scores(cards_list, p1_base15_lut)

# Sort by strength first, then tiebreaker value, along with bid
# Note: 'sorted(...)' handles the cascaded sorting automatically (i.e. sort by strength, then tiebreaker)
#       -> bids is only included so we get it sorted at output (not expecting to sort by it)
_, _, p1_ordered_bids = zip(*sorted(zip(p1_strength_list, p1_tiebreaker_list, bids_list)))
p1_score_per_listing = [(1+list_idx)*int(each_bid) for list_idx, each_bid in enumerate(p1_ordered_bids)]

answer_1 = sum(p1_score_per_listing)
print("Part 1:", answer_1)


# ---------------------------------------------------------------------------------------------------------------------
#%% Solution part 2

# Determine strength as before, but use joker counts to 'upgrade' each hand as much as possible
p2_strength_list = []
for each_card_seq in cards_list:
    
    # Remove jokers before doing character counts
    card_counts = Counter(each_card_seq.replace("J", ""))
    sorted_counts = sorted(card_counts.values())
    
    # Handle case where we get all jokers, just to make sure we have a number in the list
    # (this makes sure we can index the 'last list element' later on)
    if len(sorted_counts) == 0:
        sorted_counts = [0]
    
    # Add joker count to highest non-joker count, since that's always the best upgrade strategy
    joker_count = each_card_seq.count("J")
    sorted_counts[-1] += joker_count
    seq_strength = unique_counts_to_strength_lut[tuple(sorted_counts)]
    p2_strength_list.append(seq_strength)

# Get new tiebreaker scores (i.e. with altered joker scoring)
p2_base15_lut = {"A":14, "K":13, "Q":12, "T":10, "J":1}
p2_tiebreaker_list = get_tiebreaker_scores(cards_list, p2_base15_lut)

# Compute scoring for each card listing (bid value * ordered ranking)
_, _, p2_ordered_bids = zip(*sorted(zip(p2_strength_list, p2_tiebreaker_list, bids_list)))
p2_score_per_listing = [(1+list_idx)*int(each_bid) for list_idx, each_bid in enumerate(p2_ordered_bids)]

answer_2 = sum(p2_score_per_listing)
print("Part 2:", answer_2)
