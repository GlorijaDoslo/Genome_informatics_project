from Bio import SeqIO
import os

data_directory = os.path.dirname(os.path.abspath(__file__)) + "/datasets/"

def read_fasta(file_name):
    sequences = []
    for record in SeqIO.parse(data_directory + file_name, "fasta"):
        sequences.append(str(record.seq))

    return sequences


def count_num_of_each_character(text):
    character_counts = {}
    for char in text:
        if char not in character_counts:
            character_counts[char] = 0

        character_counts[char] += 1

    return character_counts
