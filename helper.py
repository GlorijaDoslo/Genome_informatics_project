from Bio import SeqIO
import os

data_directory = os.path.dirname(os.path.abspath(__file__)) + "/datasets/"

def read_fasta(file_name):
    sequences = []
    for record in SeqIO.parse(data_directory + file_name, "fasta"):
        sequences.append(str(record.seq))

    return sequences