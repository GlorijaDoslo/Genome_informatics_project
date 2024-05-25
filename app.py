from burrowsWheeler import bwt, index_search, rank_bwt
from constants import FIRST_DATASET_PATTERNS, SECOND_DATASET_PATTERNS
from helper import read_fasta
from sa_is_algorithm import suffix_array
from optimizations import find_character_position_in_first, create_tally, fm_search_optimized

fileNames = ["13443_ref_Cara_1.0_chr1c.fa", "10093_ref_PAHARI_EIJ_v1.1_chrX.fa"]

coffee_arabica_sequences = read_fasta(fileNames[0])
mus_pahari_sequences = read_fasta(fileNames[1])

coffee_arabica_concatenated_sequence = ''.join(coffee_arabica_sequences)
mus_pahari_concatenated_sequence = ''.join(mus_pahari_sequences)

coffee_arabica_concatenated_sequence = "banana"

s_array_coffee_arabica = suffix_array(coffee_arabica_concatenated_sequence)
print(s_array_coffee_arabica)
bwt_text = bwt(coffee_arabica_concatenated_sequence, s_array_coffee_arabica)
print(bwt_text)

ranks, tots = rank_bwt(bwt_text)
print(ranks)
print(tots)

find_coffee_arabica = index_search(bwt_text, "ana", s_array_coffee_arabica, ranks, tots)
print(f"Found without optimization: {find_coffee_arabica}")

# Optimizations - tally matrix and suffix array
tally = create_tally(bwt_text, 3)
print(f"Tally - {tally}")

first_col_positions = find_character_position_in_first(bwt_text, "ana", tots, tally, 3)
print(f"Positions in first column [including] -> {positions}")

find_coffee_arabica = fm_search_optimized(bwt_text, ranks, tots, first_col_positions, s_array_coffee_arabica, 3)
print(f"Found with optimization: {find_coffee_arabica}")



# s_array_mus_pahari = suffix_array(mus_pahari_concatenated_sequence)
# bwt_text_mus_pahari = bwt(mus_pahari_concatenated_sequence, s_array_mus_pahari)
# ranks, tots = rank_bwt(bwt_text_mus_pahari)
# find_mus_pahari = index_search(bwt_text_mus_pahari, SECOND_DATASET_PATTERNS[0], s_array_mus_pahari, ranks, tots)
# print(find_mus_pahari)