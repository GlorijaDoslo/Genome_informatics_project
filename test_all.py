from burrowsWheeler import bwt, first_column, index_search, rank_bwt
from constants import ALPHABET_SIZE, L_TYPE, S_TYPE
from sa_is_algorithm import induce_sort, lms_substrings_are_equal, suffix_array
from optimizations import create_tally, find_pattern_position_in_first, suffix_array_optimized, fm_search_optimized


# Tests for methods from BurrowsWheeler.py

def test_bwt():
    assert bwt("banana", [6, 5, 3, 1, 0, 4, 2]) == "annb$aa"
    assert bwt("mississippi", [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]) == "ipssm$pissii"
    assert bwt("abc", [3, 0, 1, 2]) == "c$ab"

def test_index_search():
    bwt_str = "ipssm$pissii"
    suffix_array = [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    ranks, tots = rank_bwt(bwt_str)
    assert index_search(bwt_str, "ssi", suffix_array, ranks, tots) == [5, 2]
    assert index_search(bwt_str, "ip", suffix_array, ranks, tots) == [7]
    assert index_search(bwt_str, "is", suffix_array, ranks, tots) == [4, 1]

def test_first_column():
    counts = {'a': 3, 'b': 1, 'c': 2}
    assert first_column(counts) == {'a': (0, 3), 'b': (3, 4), 'c': (4, 6)}
    counts = {'a': 0, 'b': 0, 'c': 0}
    assert first_column(counts) == {'a': (0, 0), 'b': (0, 0), 'c': (0, 0)}

def test_rank_bwt():
    assert rank_bwt("annb$aa") == ([0, 0, 1, 0, 0, 1, 2], {'a': 3, 'n': 2, 'b': 1, '$': 1})
    assert rank_bwt("ipssm$pissii") == ([0, 0, 0, 1, 0, 0, 1, 1, 2, 3, 2, 3], {'i': 4, 'p': 2, 's': 4, 'm': 1, '$': 1})


# Tests for methods from sa_is_algorithm.py

def test_suffix_array():
    assert suffix_array("banana") == [6, 5, 3, 1, 0, 4, 2]
    assert suffix_array("") == [0]
    assert suffix_array("a!*ba*?") == [7, 1, 5, 2, 6, 0, 4, 3]
    assert suffix_array("Lorem ipsum dolor sit amet, consectetur adipiscing elit.") == [56, 39, 21, 27, 11, 50, 5, 17, 26, 55, 0, 40, 22, 46, 28, 33, 41, 12, 32, 51, 3, 24, 35, 49, 47, 42, 6, 44, 19, 53, 52, 14, 10, 4, 23, 48, 30, 13, 29, 15, 1, 43, 7, 38, 16, 2, 45, 31, 18, 8, 20, 25, 54, 34, 36, 9, 37]
    assert suffix_array("aaaaa") == [5, 4, 3, 2, 1, 0]

def test_lms_substrings_are_equal():
    # Test case 1
    string_1 = b"banana"
    suffix_types_1 = [S_TYPE, L_TYPE, S_TYPE, L_TYPE, S_TYPE, L_TYPE, S_TYPE]
    offset_a_1 = 1
    offset_b_1 = 3
    assert lms_substrings_are_equal(string_1, suffix_types_1, offset_a_1, offset_b_1) == True

    # Test case 2
    string_2 = b"banana"
    suffix_types_2 = [S_TYPE, L_TYPE, S_TYPE, L_TYPE, S_TYPE, L_TYPE, S_TYPE]
    offset_a_2 = 1
    offset_b_2 = 6
    assert lms_substrings_are_equal(string_2, suffix_types_2, offset_a_2, offset_b_2) == False

    # Test case 3
    string_3 = b"banana"
    suffix_types_3 = [S_TYPE, L_TYPE, S_TYPE, L_TYPE, S_TYPE, L_TYPE, S_TYPE]
    offset_a_3 = 0
    offset_b_3 = 6
    assert lms_substrings_are_equal(string_3, suffix_types_3, offset_a_3, offset_b_3) == False

def test_induce_sort():
    # Test case 1
    encoded_text_1 = b"banana"
    guessed_suffix_array_1 = [6, -1, -1, -1, -1, 4, 2]
    bucket_sizes_1 = [0] * ALPHABET_SIZE

    for char in encoded_text_1:
        bucket_sizes_1[char] += 1
        
    suffix_types_1 = [S_TYPE, L_TYPE, S_TYPE, L_TYPE, S_TYPE, L_TYPE, S_TYPE]
    induce_sort(encoded_text_1, guessed_suffix_array_1, bucket_sizes_1, suffix_types_1)
    assert guessed_suffix_array_1 == [6, 5, 3, 1, 0, 4, 2]

    # Test case 2
    encoded_text_2 = b""
    guessed_suffix_array_2 = [0]
    bucket_sizes_2 = [0] * ALPHABET_SIZE

    for char in encoded_text_2:
        bucket_sizes_2[char] += 1
    
    suffix_types_2 = []
    induce_sort(encoded_text_2, guessed_suffix_array_2, bucket_sizes_2, suffix_types_2)
    assert  guessed_suffix_array_2 == [0]

    # # Test case 3
    encoded_text_3 = b"a!*ba*?"
    guessed_suffix_array_3 = [7, -1, -1, 2, 6, -1, 4, -1]
    bucket_sizes_3 = [0] * ALPHABET_SIZE

    for char in encoded_text_3:
        bucket_sizes_3[char] += 1
    
    suffix_types_3 = [S_TYPE, L_TYPE, S_TYPE, L_TYPE, S_TYPE, L_TYPE, S_TYPE]
    induce_sort(encoded_text_3, guessed_suffix_array_3, bucket_sizes_3, suffix_types_3)
    assert guessed_suffix_array_3 == [7, 1, 5, 2, 6, 0, 4, 3]



# Testing optimization methods
def test_tally_matrix_creation():
    # Test case 1
    text_1 = "banana"
    bwt_1 = "annb$aa"
    tally_checkpoint_1 = 3
    expected_result_1 = {'a': [1, 1, 3], 'n': [0, 2, 2], 'b': [0, 1, 1]}

    result_1 = create_tally(bwt_1, tally_checkpoint_1)
    assert result_1 == expected_result_1, f"Test 1 failed. Expected: {expected_result_1}, Got: {result_1}"

    # Test case 2
    text_2 = "mississippi"
    bwt_2 = "ipssm$pissii"
    tally_checkpoint_2 = 5
    expected_result_2 = {'i': [1, 1, 3], 'p': [0, 1, 2], 's': [0, 2, 4], 'm': [0, 1, 1]}

    result_2 = create_tally(bwt_2, tally_checkpoint_2)
    assert result_2 == expected_result_2, f"Test 2 failed. Expected: {expected_result_2}, Got: {result_2}"

def test_char_position_in_first_col():
    # Test case 1
    text_1 = "banana"
    bwt_1 = "annb$aa"
    pattern_1 = "ana"
    tots_1 = {'a': 3, 'n': 2, 'b': 1, '$': 1}
    expected_result_1 = [2, 3]

    result_1 = find_pattern_position_in_first(bwt_1, pattern_1, tots_1, 3)
    assert result_1 == expected_result_1, f"Test 1 failed. Expected: {expected_result_1}, Got: {result_1}"

    # Test case 2
    text_2 = "mississippi"
    bwt_2 = "ipssm$pissii"
    pattern_2 = "ipp"
    tots_2 = {'i': 4, 'p': 2, 's': 4, 'm': 1, '$': 1}
    expected_result_2 = [2, 2]

    result_2 = find_pattern_position_in_first(bwt_2, pattern_2, tots_2, 3)
    assert result_2 == expected_result_2, f"Test 2 failed. Expected: {expected_result_2}, Got: {result_2}"

def test_suffix_array_optimized():
    # Test case 1
    text_1 = "banana"
    suffix_array_1 = [6, 5, 3, 1, 0, 4, 2]
    suffix_array_checkpoint_1 = 3
    expected_result_1 = [6, 1, 2]

    result_1 = suffix_array_optimized(suffix_array_1, suffix_array_checkpoint_1)
    assert result_1 == expected_result_1, f"Test 1 failed. Expected: {expected_result_1}, Got: {result_1}"

    # Test case 2
    text_2 = "mississippi"
    suffix_array_2 = [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    suffix_array_checkpoint_2 = 4
    expected_result_2 = [11, 1, 6]

    result_2 = suffix_array_optimized(suffix_array_2, suffix_array_checkpoint_2)
    assert result_2 == expected_result_2, f"Test 2 failed. Expected: {expected_result_2}, Got: {result_2}"

def test_fm_search_optimized():
    # Test case 1
    text_1 = "banana"
    bwt_1 = "annb$aa"
    pattern_1 = "ana"
    tots_1 = {'a': 3, 'n': 2, 'b': 1, '$': 1}
    ranks_1 = [0, 0, 1, 0, 0, 1, 2]
    first_col_positions_1 = [2, 3]
    suffix_array_1 = [6, 5, 3, 1, 0, 4, 2]
    suffix_array_checkpoint_1 = 2
    expected_result_1 = [3, 1]

    result_1 = fm_search_optimized(bwt_1, ranks_1, tots_1, first_col_positions_1, suffix_array_1, suffix_array_checkpoint_1)
    assert result_1 == expected_result_1, f"Test 1 failed. Expected: {expected_result_1}, Got: {result_1}"

    # Test case 2
    text_2 = "mississippi"
    bwt_2 = "ipssm$pissii"
    pattern_2 = "ipp"
    tots_2 = {'i': 4, 'p': 2, 's': 4, 'm': 1, '$': 1}
    ranks_2 = [0, 0, 0, 1, 0, 0, 1, 1, 2, 3, 2, 3]
    first_col_positions_2 = [2, 2]
    suffix_array_2 = [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    suffix_array_checkpoint_2 = 3
    expected_result_2 = [7]

    result_2 = fm_search_optimized(bwt_2, ranks_2, tots_2, first_col_positions_2, suffix_array_2, suffix_array_checkpoint_2)
    assert result_2 == expected_result_2, f"Test 2 failed. Expected: {expected_result_2}, Got: {result_2}"

# test_tally_matrix_creation()
# test_char_position_in_first_col()
# test_suffix_array_optimized()
# test_fm_search_optimized()
