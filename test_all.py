from burrowsWheeler import bwt_transform, construct_fm_index, search_fm_index

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




# Execute tests
# test_bwt_transform()
# test_construct_fm_index()
# test_search_fm_index()



# bwt_transform, construct_fm_index, search_fm_index - added tests
# count_num_of_characters_in_bwt_string, get_starting_positions_of_characters, create_occurrence_table, indexed_search_using_fm_index