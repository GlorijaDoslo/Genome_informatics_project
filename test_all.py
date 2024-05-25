from burrowsWheeler import bwt_transform, construct_fm_index, search_fm_index
from optimizations import create_tally, find_pattern_position_in_first, suffix_array_optimized, fm_search_optimized

def test_bwt_transform():
    # Test case 1
    text_1 = "banana"
    expected_bwt_1 = "annb$aa"

    assert bwt_transform(text_1) == expected_bwt_1, f"Test 1 failed. Expected: {expected_bwt_1}, Got: {bwt_transform(text_1)}"

    # Test case 2
    text_2 = "mississippi"
    expected_bwt_2 = "ipssm$pissii"

    assert bwt_transform(text_2, True) == expected_bwt_2, f"Test 2 failed. Expected: {expected_bwt_2}, Got: {bwt_transform(text_2)}"

def test_construct_fm_index():
    # Test case 1
    bwt_1 = "annb$aa"
    expected_fm_index_1 = {
        'first_column': ['$', 'a', 'a', 'a', 'b', 'n', 'n'],
        'positions': {'$': 0, 'a': 1, 'b': 4, 'n': 5},
        'occurrence_table': {
            '$': [0, 0, 0, 0, 1, 1, 1],
            'a': [1, 1, 1, 1, 1, 2, 3],
            'b': [0, 0, 0, 1, 1, 1, 1],
            'n': [0, 1, 2, 2, 2, 2, 2]
        }
    }
    
    assert construct_fm_index(bwt_1) == expected_fm_index_1, f"Test 1 failed. Expected: {expected_fm_index_1}, Got: {construct_fm_index(bwt_1)}"

    # Test case 2
    bwt_2 = "ipssm$pissii"
    expected_fm_index_2 = {
        'first_column': ['$', 'i', 'i', 'i', 'i', 'm', 'p', 'p', 's', 's', 's', 's'],
        'positions': {'$': 0, 'i': 1, 'm': 5, 'p': 6, 's': 8},
        'occurrence_table': {
            '$': [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            'i': [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4],
            'm': [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            'p': [0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
            's': [0, 0, 1, 2, 2, 2, 2, 2, 3, 4, 4, 4]
        }
    }
    
    assert construct_fm_index(bwt_2) == expected_fm_index_2, f"Test 2 failed. Expected: {expected_fm_index_2}, Got: {construct_fm_index(bwt_2)}"

def test_search_fm_index():
    # Test case 1
    fm_index_1 = {
        'first_column': ['$', 'a', 'a', 'a', 'b', 'n', 'n'],
        'positions': {'$': 0, 'a': 1, 'b': 4, 'n': 5},
        'occurrence_table': {
            '$': [0, 0, 0, 0, 1, 1, 1],
            'a': [1, 1, 1, 1, 1, 2, 3],
            'b': [0, 0, 0, 1, 1, 1, 1],
            'n': [0, 1, 2, 2, 2, 2, 2]
        }
    }
    pattern_1 = "ana"
    expected_indices_1 = [3, 4]
    
    assert search_fm_index(fm_index_1, pattern_1) == expected_indices_1, f"Test 1 failed. Expected: {expected_indices_1}, Got: {search_fm_index(fm_index_1, pattern_1)}"

    # Test case 2
    fm_index_2 = {
        'first_column': ['$', 'i', 'i', 'i', 'i', 'm', 'p', 'p', 's', 's', 's', 's'],
        'positions': {'$': 0, 'i': 1, 'm': 5, 'p': 6, 's': 8},
        'occurrence_table': {
            '$': [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            'i': [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4],
            'm': [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            'p': [0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
            's': [0, 0, 1, 2, 2, 2, 2, 2, 3, 4, 4, 4]
        }
    }
    pattern_2 = "is"
    expected_indices_2 = [10, 11]

    assert search_fm_index(fm_index_2, pattern_2) == expected_indices_2, f"Test 2 failed. Expected: {expected_indices_2}, Got: {search_fm_index(fm_index_2, pattern_2)}"




Execute tests
test_bwt_transform()
test_construct_fm_index()
test_search_fm_index()



bwt_transform, construct_fm_index, search_fm_index - added tests
count_num_of_characters_in_bwt_string, get_starting_positions_of_characters, create_occurrence_table, indexed_search_using_fm_index



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
    expected_result_1 = (2, 3)

    result_1 = find_pattern_position_in_first(bwt_1, pattern_1, tots_1, 3)
    assert result_1 == expected_result_1, f"Test 1 failed. Expected: {expected_result_1}, Got: {result_1}"

    # Test case 2
    text_2 = "mississippi"
    bwt_2 = "ipssm$pissii"
    pattern_2 = "ipp"
    tots_2 = {'i': 4, 'p': 2, 's': 4, 'm': 1, '$': 1}
    expected_result_2 = (2, 2)

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
    first_col_positions_1 = (2, 3)
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
    first_col_positions_2 = (2, 2)
    suffix_array_2 = [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    suffix_array_checkpoint_2 = 3
    expected_result_2 = [7]

    result_2 = fm_search_optimized(bwt_2, ranks_2, tots_2, first_col_positions_2, suffix_array_2, suffix_array_checkpoint_2)
    assert result_2 == expected_result_2, f"Test 2 failed. Expected: {expected_result_2}, Got: {result_2}"

# test_tally_matrix_creation()
# test_char_position_in_first_col()
# test_suffix_array_optimized()
# test_fm_search_optimized()
