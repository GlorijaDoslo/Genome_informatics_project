
def bwt(text, s_array):
    text += '$'
    bwt_string = ['$' if elem == 0 else text[elem - 1] for elem in s_array]
    return ''.join(bwt_string)


def index_search(bwt_string, pattern, suffix_array, ranks, tots):

    if not pattern:
        return []
    
    first = first_column(tots)

    if pattern[-1] not in first or pattern[-1] == '$':
        return []
    
    left, right = first[pattern[-1]]

    i = len(pattern) - 2

    while i >= 0 and right > left:
        char = pattern[i]
        # scan from left, looking for occurrences of char
        j = left
        while j < right:
            if bwt_string[j] == char:
                left = first[char][0] + ranks[j]
                break
            j += 1

        if j == right:
            left = right
            break  # no occurrences

        right -= 1
        while bwt_string[right] != char:
            right -= 1
        right = first[char][0] + ranks[right] + 1
        i -= 1
    
    list1 = list(suffix_array)
    return list1[left:right]


def first_column(counts):
    first = {}
    total_count = 0
    for char, count in sorted(counts.items()):
        first[char] = (total_count, total_count + count)
        total_count += count
    return first


def rank_bwt(bw):
    counts = dict() 
    ranks = [] 
    for char in bw:
        if char not in counts:
            counts[char] = 0
        ranks.append(counts[char])
        counts[char] += 1

    return ranks, counts