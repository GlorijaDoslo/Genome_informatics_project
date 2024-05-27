from burrowsWheeler import first_column

def fm_search_optimized(bwt_string, pattern, ranks, tots, tally, tally_checkpoint, suffix_array, suffix_array_checkpoint=1):
    """
    Optimized search for a pattern using the found pattern positions in the first column and suffix array
    with checkpoints to get indexes of pattern in original text.

    Parameters:
        bwt_string (str): The last column of BWT matrix.
        pattern (str): Pattern to be found.
        ranks (list): The ranks list calculated from BWT.
        tots (dict): The total counts of characters in BWT.
        tally (dict): Tally matrix.
        tally_checkpoint (int): Checkpoint where values are found.
        suffix_array (list): Suffix array of the original text.
        suffix_array_checkpoint (int): Checkpoint where values are found.
    
    Returns:
        indexes (list): Indexes of the pattern in the original text.
    """

    indexes = []

    if suffix_array_checkpoint < 1:
        print("Not allowed value for suffix array checkpoint.")
        return indexes
    
    first_col = first_column(tots)
    first_col_positions = find_pattern_position_in_first(bwt_string, pattern, first_col, tots, tally, tally_checkpoint)

    if first_col_positions == []:
        return indexes

    for index in range(first_col_positions[0], first_col_positions[1] + 1):
        if index % suffix_array_checkpoint == 0:
            indexes.append(suffix_array[index // suffix_array_checkpoint])
        else:
            row = index
            count = 0
            while row % suffix_array_checkpoint != 0:
                count = count + 1
                bwt_c = bwt_string[row]
                row = first_col[bwt_c][0] + ranks[row]
            indexes.append((suffix_array[row // suffix_array_checkpoint] + count) % len(bwt_string)) 

    return indexes

def precalculate_tally_and_suffix_array(bwt_string, tally_checkpoint, suffix_array, suffix_array_checkpoint):
    """
    Pre-calculates tally matrix and suffix array.

    Parameters:
        bwt_string (str): The last column of BWT matrix.
        tally_checkpoint (int): Checkpoint where values are found.
        suffix_array (list): Suffix array of the original text.
        suffix_array_checkpoint (int): Checkpoint where values are found.

    Returns:
        tally (dict): Created tally matrix.
        suffix_array_opt (list): Optimized suffix array which is containing only values in checkpoints.
    """

    tally = create_tally(bwt_string, tally_checkpoint)
    suffix_array_opt = suffix_array_optimized(suffix_array, suffix_array_checkpoint)
    return tally, suffix_array_opt

def suffix_array_optimized(suffix_array, suffix_array_checkpoint=1):
    """
    Creates optimized suffix array with checkpoints.

    Parameters:
        suffix_array (list): Suffix array of the original text.
        suffix_array_checkpoint (int): Checkpoint where values are found.
        
    Returns:
        suffix_array_opt (list): Optimized suffix array which is containing only values in checkpoints.
    """

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

def find_pattern_position_in_first(bwt_string, pattern, first_col, tots, tally, tally_checkpoint=1):
    """
    Finds range where pattern occurs in first column of BWT matrix.
        
    Parameters:
        bwt_string (str): The last column of BWT matrix.
        pattern (str): Pattern to be found.
        first_col (dict): First column of BWT matrix with positions.
        tots (dict): The total counts of characters in BWT.
        tally (dict): Tally matrix.
        tally_checkpoint (int): Checkpoint where values are found.

    Returns:
        first_col_positions (list): The range of pattern occurrences in the first column.
    """

    if not pattern or tally_checkpoint < 0:
        print("No pattern or invalid value for tally checkpoint (must be >= 1).")
        return []

    if pattern[-1] not in first_col:
        print("Pattern not found.")
        return []
    
    lower_index_ex, upper_index_incl = first_col[pattern[-1]]
    pattern_index = len(pattern) - 2

    lower_index_ex = lower_index_ex - 1
    upper_index_incl = upper_index_incl - 1

    for i in range(pattern_index, -1, -1):
        char_to_find = pattern[i]

        if lower_index_ex % tally_checkpoint == 0:
            lower_rank = tally[char_to_find][lower_index_ex // tally_checkpoint]
        else:
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
            return []

        lower_index_ex = first_col[char_to_find][0] + lower_rank - 1
        upper_index_incl = first_col[char_to_find][0] + lower_rank + char_occurences_num - 1

    first_col_positions = [lower_index_ex + 1, upper_index_incl]
    return first_col_positions

def find_occurrences_to_the_checkpoint(bwt_string, limit_index, char_to_find, tally_checkpoint):
    """
    Called when certain character is not in tally matrix. Finds that character in BWT last column 
    and counts the occurrences of it. Counting stops when the tally checkpoint is reached.

    Parameters:
        bwt_string (str): The last column of BWT matrix.
        limit_index (int): Starting index for character search.
        char_to_find (str): Character to be found.
        tally_checkpoint (int): Checkpoint where values are found.
        
    Returns:
        current_index (int): Index of found character in the checkpoint.
        count (int): Number of occurrences of the character in the way to the checkpoint.
    """

    count = 0
    current_index = limit_index

    while current_index % tally_checkpoint != 0:
        if bwt_string[current_index] == char_to_find:
            count = count + 1
        current_index = current_index - 1
    
    return current_index, count



def create_tally(bwt_string, tally_checkpoint):
    """
    Creates tally matrix.

    Parameters:
        bwt_string (str): The last column of BWT matrix.
        tally_checkpoint(int): Checkpoint where values are found.

    Returns:
        tally (dict): Created tally matrix.
    """

    char_occurrences = {}
    tally = {}

    for char in bwt_string:
        if char != '$':
            if char not in char_occurrences:
                char_occurrences[char] = 0
                tally[char] = []

    for index, char in enumerate(bwt_string):
        if char != '$':
            char_occurrences[char] += 1
            if index % tally_checkpoint == 0:    
                for char in tally.keys():
                    tally[char].append(char_occurrences[char])
        elif char == '$':
            if index % tally_checkpoint == 0:
                for char in tally.keys():
                    tally[char].append(char_occurrences[char])
    
    return tally
