from constants import ALPHABET_SIZE, L_TYPE, S_TYPE

def suffix_array(text):
    """
    Generates the suffix array for the given input text using the SA-IS algorithm.

    Parameters:
        text (str): The input text for which the suffix array is to be generated.

    Returns:
        list: The generated suffix array.
    """

    encoded_text = text.encode('utf-8')
    print(encoded_text)

    sa_array = sa_is_algorithm(encoded_text, ALPHABET_SIZE)

    return sa_array


def sa_is_algorithm(encoded_text, alphabet_size):
    """
    Implements the SA-IS algorithm to generate the suffix array.

    Parameters:
        encoded_text (bytes): The encoded text (in UTF-8) for which the suffix array is to be generated.
        alphabet_size (int): The size of the alphabet (number of unique characters) in the text.

    Returns:
        list: The suffix offsets representing the suffix array.
    """

    # mark each suffix of the data as S_TYPE or L_TYPE

    suffix_types = bytearray(len(encoded_text) + 1)
    bucket_sizes = [0] * alphabet_size
    
    suffix_types[-1] = S_TYPE # The empty suffix after the last character

    if len(encoded_text):
        suffix_types[-2] = L_TYPE # The suffix containing only the last character must necessarily be larger than the empty suffix

        for i in range(len(encoded_text) - 2, -1, -1): # going from right to left
            if encoded_text[i] > encoded_text[i + 1]: # if current suffix is bigger than his right suffix
                suffix_types[i] = L_TYPE
            elif encoded_text[i] == encoded_text[i + 1] and suffix_types[i + 1] == L_TYPE: # suffix_types[i + 1] is the type of previous suffix
                suffix_types[i] = L_TYPE
            else:
                suffix_types[i] = S_TYPE

            bucket_sizes[encoded_text[i]] += 1 # find number of occurrences of each character

        bucket_sizes[encoded_text[len(encoded_text) - 1]] += 1 # add one missing character from for loop

    # Create a suffix array with room for a pointer to every suffix of
    # the string, including the empty suffix at the end
    offset = 1
    bucket_tails = []
    for size in bucket_sizes:
        offset += size
        bucket_tails.append(offset - 1)

    guessed_suffix_array = [-1] * (len(encoded_text) + 1)

    for i in range(len(encoded_text)):
        # Check if not the start of an LMS suffix
        if not (i != 0 and suffix_types[i] == S_TYPE and suffix_types[i - 1] == L_TYPE):
            continue

        guessed_suffix_array[bucket_tails[encoded_text[i]]] = i
        bucket_tails[encoded_text[i]] -= 1

    # The empty suffix is defined to be an left-most S character or LMS-substring and it is located on 0 index
    guessed_suffix_array[0] = len(encoded_text)

    induce_sort(encoded_text, guessed_suffix_array, bucket_sizes, suffix_types)


    lms_names = [-1] * (len(encoded_text) + 1)
    currentName = 0

    lms_names[guessed_suffix_array[0]] = currentName
    last_lms_suffix_offset = guessed_suffix_array[0]

    for i in range(1, len(guessed_suffix_array)):
        suffix_offset = guessed_suffix_array[i]

        # We only care about LMS suffixes.
        if not (suffix_offset != 0 and suffix_types[suffix_offset] == S_TYPE and suffix_types[suffix_offset - 1] == L_TYPE):
            continue

        if not lms_substrings_are_equal(encoded_text, suffix_types, last_lms_suffix_offset, suffix_offset):
            currentName += 1

        last_lms_suffix_offset = suffix_offset

        lms_names[suffix_offset] = currentName

    # Now lmsNames contains all the characters of the suffix string in the correct order, 
    # but it also contains a lot of unused indexes we don't care about and which we want to remove
    summary_suffix_offsets = []
    summary_string = []
    for index, name in enumerate(lms_names):
        if name == -1:
            continue
        summary_suffix_offsets.append(index)
        summary_string.append(name)

    if ((currentName + 1) == len(summary_string)): # currentName + 1 is summary alphabet size
        summary_suffix_array = [-1] * (len(summary_string) + 1)

        summary_suffix_array[0] = len(summary_string)

        for x in range(len(summary_string)):
            y = summary_string[x]
            summary_suffix_array[y + 1] = x

    else:
        summary_suffix_array = sa_is_algorithm(summary_string, currentName + 1)


    # accumulate lms sort

    offset = 1
    bucket_tails = []
    for size in bucket_sizes:
        offset += size
        bucket_tails.append(offset - 1)

    suffix_offsets = [-1] * (len(encoded_text) + 1)

    for i in range(len(summary_suffix_array) - 1, 1, -1):
        stringIndex = summary_suffix_offsets[summary_suffix_array[i]]

        suffix_offsets[bucket_tails[encoded_text[stringIndex]]] = stringIndex
        bucket_tails[encoded_text[stringIndex]] -= 1

    suffix_offsets[0] = len(encoded_text)

    induce_sort(encoded_text, suffix_offsets, bucket_sizes, suffix_types)

    return suffix_offsets
    

def lms_substrings_are_equal(string, suffix_types, offset_a, offset_b):
    """
    Check if two LMS (Longest Minimal Substring) substrings are equal.

    This function compares two LMS substrings starting at offset_a and offset_b
    respectively in the given string and determines whether they are equal.

    Parameters:
        string (bytes): The input string.
        suffix_types (list): A list indicating whether each suffix is of S_TYPE or L_TYPE.
        offset_a (int): The starting offset of the first LMS substring.
        offset_b (int): The starting offset of the second LMS substring.

    Returns:
        bool: True if the LMS substrings are equal, False otherwise.
    """
    
    # No other substring is equal to the empty suffix.
    if offset_a == len(string) or offset_b == len(string):
        return False

    i = 0
    while True:
        a_substring_is_lms = (i + offset_a) != 0 and suffix_types[i + offset_a] == S_TYPE and suffix_types[i + offset_a - 1] == L_TYPE
        b_substring_is_lms = (i + offset_b) != 0 and suffix_types[i + offset_b] == S_TYPE and suffix_types[i + offset_b - 1] == L_TYPE

        if (i > 0 and a_substring_is_lms and b_substring_is_lms):
            return True

        if string[i + offset_a] != string[i + offset_b] or a_substring_is_lms != b_substring_is_lms:
            return False

        i += 1


def induce_sort(encoded_text, guessed_suffix_array, bucket_sizes, suffix_types):
    """
    Performs the induce-sort step of the SA-IS algorithm to further sort the suffix array.

    This method refines the suffix array by inducing sorting on the L-type and S-type suffixes.

    Parameters:
        encoded_text (bytes): The encoded text (in UTF-8) for which the suffix array is generated.
        guessed_suffix_array (list): The initial guessed suffix array before inducing sorting.
        bucket_sizes (list): A list containing the sizes of each bucket corresponding to characters in the alphabet.
        suffix_types (list): A list indicating whether each suffix is of S_TYPE or L_TYPE.

    Returns:
        None: The suffix array is updated in place.

    Notes:
        This method modifies the guessed suffix array in place to produce the final sorted suffix array.
        It operates on L-type and S-type suffixes separately, using bucket pointers to efficiently place them in the correct order.
    """
    offset_for_tails = 1
    offset_for_heads = 1
    bucket_tails = []
    bucket_heads = []
    for size in bucket_sizes:
        offset_for_tails += size
        bucket_tails.append(offset_for_tails - 1)
        bucket_heads.append(offset_for_heads)
        offset_for_heads += size
    
    for i in range(len(guessed_suffix_array)):
        if guessed_suffix_array[i] == -1: # no offset is recorded here
            continue

        # We're interested in the suffix that begins to the left of the suffix this entry points at.
        j = guessed_suffix_array[i] - 1

        if j < 0:
            continue
        if suffix_types[j] != L_TYPE: # We're only interested in L-type suffixes
            continue

        guessed_suffix_array[bucket_heads[encoded_text[j]]] = j
        bucket_heads[encoded_text[j]] += 1

    for i in range(len(guessed_suffix_array) - 1, -1, -1):
        j = guessed_suffix_array[i] - 1

        if j < 0:
            continue
        if suffix_types[j] != S_TYPE: # We're only interested in S-type suffixes
            continue

        guessed_suffix_array[bucket_tails[encoded_text[j]]] = j
        bucket_tails[encoded_text[j]] -= 1