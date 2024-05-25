from burrowsWheeler import first_column

def fm_search_optimized(bwt_string, ranks, tots, first_col_positions, suffix_array, suffix_array_checkpoint=1):
    if suffix_array_checkpoint < 1:
        print("Not allowed value for suffix array checkpoint.")
        return -1
    
    suffix_array_opt = suffix_array_optimized(suffix_array, suffix_array_checkpoint)
    first_col = first_column(tots)

    indexes = []

    for index in range(first_col_positions[0], first_col_positions[1] + 1):
        if index % suffix_array_checkpoint == 0:
            indexes.append(suffix_array_opt[index // suffix_array_checkpoint])
        else:
            row = index
            count = 0
            while row % suffix_array_checkpoint != 0:
                count = count + 1
                s = bwt_string[row]
                row = first_col[s][0] + ranks[row]
            indexes.append((suffix_array_opt[row // suffix_array_checkpoint] + count) % len(bwt_string)) 

    return indexes

# optimize already created suffix array - save just checkpoints
def suffix_array_optimized(suffix_array, suffix_array_checkpoint=1):
    if suffix_array_checkpoint < 1:
        print("Not allowed value for suffix array checkpoint.")
        return -1

    if suffix_array_checkpoint == 1:
        return suffix_array

    suffix_array_opt = []
    for index in range(0, len(suffix_array)):
        if index % suffix_array_checkpoint == 0:
            suffix_array_opt.append(suffix_array[index])

    return suffix_array_opt

# returns position of pattern in first column
def find_pattern_position_in_first(bwt_string, pattern, tots, tally_checkpoint=1):
    if not pattern or tally_checkpoint < 0:
        print("No pattern or invalid value for tally checkpoint (must be >= 1).")
        return
    
    first_col = first_column(tots)

    if pattern[-1] not in first_col:
        print("Pattern not found.")
        return

    tally = create_tally(bwt_string, tally_checkpoint)
    
    lower_index_ex, upper_index_incl = first_col[pattern[-1]]
    pattern_index = len(pattern) - 2

    lower_index_ex = lower_index_ex - 1
    upper_index_incl = upper_index_incl - 1

    for i in range(pattern_index, -1, -1):
        char_to_find = pattern[i]

        if lower_index_ex % tally_checkpoint == 0:
            # rank can be found in tally since in it is the index of checkpoint
            lower_rank = tally[char_to_find][lower_index_ex // tally_checkpoint]
        else:
            # find rank using the checkpoint
            index, count = find_occurrences_to_the_checkpoint(bwt_string, lower_index_ex, char_to_find, tally_checkpoint)
            lower_rank = tally[char_to_find][index // tally_checkpoint] + count

        if upper_index_incl % tally_checkpoint == 0:
            upper_rank = tally[char_to_find][upper_index_incl // tally_checkpoint]
        else:
            index, count = find_occurrences_to_the_checkpoint(bwt_string, upper_index_incl, char_to_find, tally_checkpoint)
            upper_rank = tally[char_to_find][index // tally_checkpoint] + count

        char_occurences_num = upper_rank - lower_rank
        if char_occurences_num == 0:
            print("Pattern not found.")
            return

        # since ranks are found for last column, we search it in the first column, so
        # we need to set lower_index_ex and upper_index_incl to correspond the char in the first column
        lower_index_ex = first_col[char_to_find][0] + lower_rank - 1
        upper_index_incl = first_col[char_to_find][0] + lower_rank + char_occurences_num - 1

    return lower_index_ex + 1, upper_index_incl


# calculate how much char_to_find characters are found in the way to the checkpoint
def find_occurrences_to_the_checkpoint(bwt_string, limit_index, char_to_find, tally_checkpoint):
    count = 0
    current_index = limit_index

    while current_index % tally_checkpoint != 0:
        if bwt_string[current_index] == char_to_find:
            count = count + 1
        current_index = current_index - 1
    
    return current_index, count



def create_tally(bwt_string, tally_checkpoint):
    char_occurrences = {}
    tally = {}

    # initialize
    for char in bwt_string:
        if char != '$':
            if char not in char_occurrences:
                char_occurrences[char] = 0
                tally[char] = []

    # char_occurences contains current count number for each character
    # not all rows from tally are saved, it depends on checkpoint length
    # since we are not storing all tally rows, char_occurrences is needed to save count of not stored values
    # so we can use it to calculate the next checkpoints
    for index, char in enumerate(bwt_string):
        if char != '$':
            char_occurrences[char] += 1
            if index % tally_checkpoint == 0:    
                for char in tally.keys():
                    tally[char].append(char_occurrences[char])
        elif char == '$':
            # if char is $, add occurrences row for it
            if index % tally_checkpoint == 0:
                for char in tally.keys():
                    tally[char].append(char_occurrences[char])
    
    return tally
