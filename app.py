from burrowsWheeler import bwt_transform, construct_fm_index, indexed_search_using_fm_index, search_fm_index
from constants import FIRST_DATASET_PATTERNS
from helper import read_fasta


# text = "banana"
# pattern = "ana"

# matches = indexed_search_using_fm_index(text, pattern, verbose=True)

# print("Pattern matches at indices:", matches)

file_name = "13443_ref_Cara_1.0_chr1c.fa"

coffee_arabica_sequences = read_fasta(file_name)
# mus_pahari_sequences = read_fasta("10093_ref_PAHARI_EIJ_v1.1_chrX.fa")
coffee_arabica_concatenated_sequence = ''.join(coffee_arabica_sequences)
# mus_pahari_concatenated_sequence = ''.join(mus_pahari_sequences)

matches = indexed_search_using_fm_index(coffee_arabica_concatenated_sequence, FIRST_DATASET_PATTERNS[0], verbose=True, debug=False)




# compute_suffix_array(coffee_arabica_concatenated_sequence, len(coffee_arabica_concatenated_sequence))

# bwt = bwt_transform(text)
# print("Burrows-Wheeler Transform:", bwt)

# fm_index = construct_fm_index(bwt)
# print("FM Index:", fm_index)

# fm_index = {'cumulative_counts': {'$': 0, 'a': 1, 'b': 4, 'n': 5}, 'occurrence_table': {'a': [1, 1, 1, 1, 1, 2, 3], 
#                                                                                         'n': [0, 1, 2, 2, 2, 2, 2], 
#                                                                                         'b': [0, 0, 0, 1, 1, 1, 1], 
#                                                                                         '$': [0, 0, 0, 0, 1, 1, 1]}}

# matches = search_fm_index(text, pattern)
# print("Pattern matches at indices:", matches)