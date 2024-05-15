from helper import count_num_of_each_character

batch_size = 10


def bwt_transform(text, verbose = False, debug = False):

    # ovo napuni ram memoriju za 2s, a batch verziju nisam ni probala
    # kopirala sam i kod sa prezentacije predavanja i radi isto

    if verbose:
        print("Doing the Burrows-Wheeler Transform...")

    text += "$"

    if debug:
        bwt_array = []
        bwt_array.append(text)
        for i in range(1,len(text),1):
            bwt_array.append(text[i::]+text[:i:])

        bwt_array.sort()

        for i in bwt_array:
            print(i)        
    
    # print("Batch size is", batch_size)

    # i = 1
    # def rotations_generator():
    #     for i in range(0, len(text), batch_size):
    #         for j in range(i, min(i + batch_size, len(text))):
    #             yield text[j:] + text[:j]

    #         i = i + 1
    #         print("Finished batch number", i)

    def rotations_generator():
        for i in range(len(text)):
            yield text[i:] + text[:i]

    # rotations = [text[i:] + text[:i] for i in range(len(text))]

    print()
    sorted_rotations = sorted(rotations_generator())
    print("finished sorting")
    bwt = "".join(rotation[-1] for rotation in sorted_rotations)

    return bwt


from operator import itemgetter

argsort = lambda l: [i for i, _ in sorted(enumerate(l), key=itemgetter(1))]


def suffix_array(arr):
    arr_size = len(arr)
    arr_int = {v: k for k, v in enumerate(sorted(set(arr)))}
    arr = [arr_int[x] for x in arr]
    arr.append(-1)
    suf = [[i, arr[i], arr[i + 1]] for i in range(arr_size)]
    suf.sort(key=itemgetter(1, 2))
    idx = [0] * arr_size
    k = 2
    while k < arr_size:
        r = 0
        prev_r = suf[0][1]
        for i in range(arr_size):
            if suf[i][1] != prev_r or suf[i - 1][2] != suf[i][2]:
                r += 1
            prev_r = suf[i][1]
            suf[i][1] = r
            idx[suf[i][0]] = i
        for i in range(arr_size):
            next_idx = suf[i][0] + k
            suf[i][2] = suf[idx[next_idx]][1] if next_idx < arr_size else -1
        suf.sort(key=itemgetter(1, 2))
        k <<= 1
    return [x[0] for x in suf]


def bwt(data):
    data_ref = suffix_array(data)
    return (x - 1 for x in data_ref), data_ref.index(0)


def cmp_func(x, y):
    return (x[1] > y[1]) - (x[1] < y[1])
 
 
def compute_suffix_array(input_text, len_text):
    print("Computing suffix array")
    #suffix_arr = []
    bwt_arr = ""
    batchCount = 0
    with open("bwt.txt", 'w') as f:
        for i in range(0, len_text, batch_size):
            suff = [(j, input_text[j:]) for j in range(i, min(i + batch_size, len_text))]
        
            suff.sort(key=lambda x: x[1])
            suffix_arr = [i for i, _ in suff]
            for i in range(batch_size):
                # Computes the last char which is given by 
                # input_text[(suffix_arr[i] + n - 1) % n]
                j = suffix_arr[i] - 1
                if j < 0:
                    j = j + batch_size
                bwt_arr += input_text[j]

            f.write(bwt_arr)
            #suffix_arr.extend(j for j, _ in suffixes)
            batchCount = batchCount + 1
            print("Finished batch number", batchCount)
            #suffix_arr = [i for i, _ in suff]
 
    print("Returning suffix array")
 

# ne koristim je jer ne mogu ni suffix array da napravim a kamoli da nadjem zadnju kolonu
def find_last_char(input_text, suffix_arr, n): 
    bwt_arr = ""

    with open("sa.txt", 'r') as f:
        suffix_arr = [int(line.strip()) for line in f]

    for i in range(n):
        # Computes the last char which is given by 
        # input_text[(suffix_arr[i] + n - 1) % n]
        j = suffix_arr[i] - 1
        if j < 0:
            j = j + n
        bwt_arr += input_text[j]
 
    return bwt_arr


def bwt_transform2(text, verbose = False, debug = False):

    # ova implementacija mi je radila batch dok mi ceo operativni sistem nije pukao i 
    # onda sam koristeci chkdsk popravila hard disk na kome je trebao da bude sacuvan fajl

    if verbose:
        print("Doing the Burrows-Wheeler Transform...")
 
    text += "$"

    compute_suffix_array(text, len(text))
    # bwt_arr = find_last_char(text, suffix_arr, len(text))

    # bwt_arr = bwt(text)
    
    # print(bwt_arr)
    # return bwt_arr

def bwt_transform3(text, verbose = False, debug = False):

    # ovo je jedna od implementacija, memorija bude na 75% skoci na 98% pa padne na 75% i tako dok
    # operativni sistem ne ubije proces

    if verbose:
        print("Doing the Burrows-Wheeler Transform...")

    text += "$"

    bwt_arr = bwt(text)

    print(bwt_arr)
    # return bwt_arr

def get_starting_positions_of_characters(character_counts):
    occurrences_table = {}
    cumulative_count = 0

    for char, count in sorted(character_counts.items()):
        occurrences_table[char] = cumulative_count
        cumulative_count += count

    return occurrences_table

def create_occurrence_table(bwt_string):
    occurrence_table = {}

    for i, char in enumerate(bwt_string):
        if char not in occurrence_table:
            occurrence_table[char] = [0] * len(bwt_string)
        occurrence_table[char][i] += 1

    for char in occurrence_table:
        count = 0
        for i in range(len(bwt_string)):
            count += occurrence_table[char][i]
            occurrence_table[char][i] = count

    return occurrence_table

def construct_fm_index(bwt, verbose = False):
 
    if verbose:
        print("Constructing the FM Index...")

    first_column = sorted(bwt)

    character_counts = count_num_of_each_character(first_column)
    starting_positions = get_starting_positions_of_characters(character_counts)
    occurrence_table = create_occurrence_table(bwt)

    fm_index = {'first_column': first_column, 'positions': starting_positions, 'occurrence_table': occurrence_table }

    return fm_index

def search_fm_index(fm_index, pattern, verbose = False, debug = False):

    if verbose:
        print("Searching FM Index for matches for pattern ", pattern)

    first_column = fm_index['first_column'] 
    starting_positions = fm_index['positions']
    occurrence_table = fm_index['occurrence_table']

    if (debug):
        print("Starting positions of each characters are", starting_positions)
        print("Ocurrence table is", occurrence_table)
        print("Pattern is", pattern)

    i = 0
    result = []

    if (len(pattern) == 1):
        return [i + 1 for i, x in enumerate(list(first_column)) if x == pattern]

    last_char = pattern[-1]
    positions = [i for i, x in enumerate(list(first_column)) if x == last_char]
    
    try:
        start = min(positions)
        end = max(positions)
    except ValueError:
        if debug:
            print("Last character doesn't match any character in first_column")

        return []

    if debug:
        print("Last character in given pattern is", last_char)
        print("Positions of that character in first column of BWT is", positions)
        print("Start:", start, " End:", end)

    for char in reversed(pattern[:-1]):
        if char not in occurrence_table:
            return []  # Character not found in occurrence table
        
        start = starting_positions[char] + occurrence_table[char][start] - 1
        end = starting_positions[char] + occurrence_table[char][end] - 1
        
        if (debug):
            print("Start:", start, " End:", end)

        result = [start + 1, end + 1] # Adding +1 because I counted from 0 instead of 1

    return result

def indexed_search_using_fm_index(text, pattern, verbose = False, debug = False):
    """
    Performs indexed search of the given pattern within the text using BWT and FM index.

    Parameters:
    - text (str): The input text.
    - pattern (str): The pattern to search for.

    Returns:
    - list: A list of indices where the pattern occurs in the text.
    """

    if verbose:
        print("Doing index search using FM Index...")

    bwt_text = bwt_transform2(text, verbose=verbose, debug=debug)

    if debug:
        print("BWT of the text is", bwt_text)

    fm_index = construct_fm_index(bwt_text, verbose=verbose)

    if debug:
        print("FM index is", fm_index)

    matches = search_fm_index(fm_index, pattern, verbose=verbose, debug=debug)

    if debug:
        print("Matches that are found are", matches)

    return matches
