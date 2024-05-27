import argparse
import time

from pympler import asizeof 
from burrowsWheeler import bwt, index_search, rank_bwt
from constants import ALL_PATTERNS
from helper import read_fasta
from sa_is_algorithm import suffix_array
from optimizations import precalculate_tally_and_suffix_array, fm_search_optimized

file_names = ["13443_ref_Cara_1.0_chr1c.fa", "10093_ref_PAHARI_EIJ_v1.1_chrX.fa", "223781_ref_bAquChr1.2_chr4.fa"]

# args for checkpoints
parser = argparse.ArgumentParser()
parser.add_argument("tally_checkpoint", nargs='?', type = int, help = "Tally matrix checkpoint")
parser.add_argument("suffix_array_checkpoint", nargs='?', type = int, help = "Suffix array checkpoint")
args = parser.parse_args()
tally_checkpoint = args.tally_checkpoint if args.tally_checkpoint is not None else 1
suffix_array_checkpoint = args.suffix_array_checkpoint if args.suffix_array_checkpoint is not None else 1


for file_name in file_names:
    print(f"File: {file_name}")
    sequences_from_fasta = read_fasta(file_name)
    sequences_from_fasta_concatenated = ''.join(sequences_from_fasta)

    for file_patterns in ALL_PATTERNS:
        for pattern in file_patterns:
            print(f"Pattern: {pattern}")
            suffix_array_init = suffix_array(sequences_from_fasta_concatenated)
            bwt_text = bwt(sequences_from_fasta_concatenated, suffix_array_init)
            ranks, tots = rank_bwt(bwt_text)

            # TIME
            # time for search without optimizations
            start_search_time = time.process_time()
            find_sequence = index_search(bwt_text, pattern, suffix_array_init, ranks, tots)
            end_search_time = time.process_time()
            search_time = end_search_time - start_search_time
            print(f"Search time without optimizations: {search_time} seconds")

            tally, suffix_array_opt = precalculate_tally_and_suffix_array(bwt_text, tally_checkpoint, suffix_array_init, suffix_array_checkpoint)

            # time for optimized search
            search_time_start = time.process_time()
            find_sequence = fm_search_optimized(bwt_text, pattern, ranks, tots, tally, tally_checkpoint, suffix_array_opt, suffix_array_checkpoint)
            search_time_end = time.process_time()
            search_time = search_time_end - search_time_start
            print(f"Search time with optimizations: {search_time} seconds")

            # MEMORY - can be outside of for - same for all patterns in one file
            # memory usage without optimization [bwt, rank and suffix array]
            suffix_array_init_memory = asizeof.asizeof(suffix_array_init)
            # bwt_memory = asizeof.asizeof(bwt_text)
            # ranks_memory = asizeof.asizeof(ranks)
            # memory_without_optimization = (bwt_memory + ranks_memory + suffix_array_memory) / (1024 * 1024)
            memory_without_optimization = (suffix_array_init_memory) / (1024 * 1024)
            print(f"Memory usage without optimization: {memory_without_optimization} MB")

            # memory usage with optimization [bwt, rank, tally matrix and suffix array optimized]
            suffix_array_optimized_memory = asizeof.asizeof(suffix_array_opt)
            tally_memory = asizeof.asizeof(tally)
            # memory_with_optimization = (bwt_memory + ranks_memory + tally_memory + suffix_array_optimized_memory) / (1024 * 1024)
            memory_with_optimization = (tally_memory + suffix_array_optimized_memory) / (1024 * 1024)
            print(f"Memory usage with optimization: {memory_with_optimization} MB")
            