# #Pattern matching algorithm that uses modified boyer moore
def pattern_matching(txt, pat):
    ORD_START_ALPHABET = 37
    ORD_END_ALPHABET = 126
    ALPHABET_SIZE = ORD_END_ALPHABET - ORD_START_ALPHABET + 1
    result = []
    n = len(pat)
    shift = len(txt) - 1
    start = -1

    modfied_rx_table = preprocess_rx_table(pat, ALPHABET_SIZE, ORD_START_ALPHABET)
    modified_good_suffix_rule = preprocess_good_suffix_rule_modified(pat)

    while shift >= n - 1:
        curr_index_pat = n - 1
        while curr_index_pat >= 0 and pat[curr_index_pat] == txt[curr_index_pat + (shift - n + 1)]:
            if start != -1:
                curr_index_pat = start
                start = -1
            else:
                curr_index_pat -= 1
        if curr_index_pat >= 0:
            mismatch_index = curr_index_pat
            mismatch_txt_index = mismatch_index + (shift - n + 1)
            ord_of_mismatch_txt_char = ord(txt[mismatch_txt_index]) - 37

            rx_pos = modfied_rx_table[mismatch_index][ord_of_mismatch_txt_char]

            p = modified_good_suffix_rule[mismatch_index+1]

            if p != -1 and rx_pos != -1 and pat[rx_pos] == pat[p-1]:
                shift -= n - p
                start = p - 1
            else:
                if rx_pos != -1:
                    shift -= n - rx_pos
                    start = -1
                else:
                    shift = mismatch_txt_index - 1
                    start = -1
        else:
            #Pattern has been found
            start_point_match = shift-n+1
            result.append(start_point_match)
            #This would mean that there exists a beta starting at index 0 of pat
            if modified_good_suffix_rule[0] != -1:
                shift -= n - modified_good_suffix_rule[0]
                start = modified_good_suffix_rule[0] -1
            #This would mean no beta exist starting at index point 0 of pat
            else:
                shift -= n
                start = -1

    return result

def z_algorithm_for_boyer_moore(pat):
    str = pat
    z_array = [-1] * len(str)
    left = 0
    right = 0
    for k in range(1, len(str)):
        if k > right:
            counter = 0
            while counter+k < len(str) and str[counter] == str[counter + k]:
                counter += 1
            z_array[k] = counter
            if z_array[k] > 0:
                left = k
                right = k + z_array[k] - 1
        else:
            #red box is smaller than the green box
            if z_array[k-left] < right - k + 1:
                z_array[k] = z_array[k-left]
            else:
                #red box is equal to or greater than the green
                counter = right - k + 1
                z_array[k] = counter
                while counter+k < len(str) and str[counter] == str[counter + k]:
                    counter += 1
                z_array[k] = counter
                left = k
                right = k + z_array[k] - 1

    return z_array

#######################
# Preprocess Functions
#######################

# def preprocess_bad_char_rule_modified(pat, ALPHABET_SIZE, START_ALPHABET):
#     # Creates an Rk(x) table where for each character x, 
#     # store the leftmost position of occurances of x in pat to the right of k
#     table = []
#     prev_row = [-1 for _ in range(ALPHABET_SIZE)]
#     for i in range(len(pat)-1, -1, -1):
#         table.append(prev_row.copy())
#         prev_char_index = ord(pat[i]) - START_ALPHABET
#         prev_row[prev_char_index] = i
#     table.reverse()
#     return table

def preprocess_rx_table(pat, ALPHABET_SIZE, START_ALPHABET):
    # Creates an Rx(k) table where for each character x, 
    # store the rightmost position of occurances of x in pat to the right of k
    table = []
    prev_row = [-1 for _ in range(ALPHABET_SIZE)]
    for i in range(len(pat)-1, -1, -1):
        table.append(prev_row.copy())
        prev_char_index = ord(pat[i]) - START_ALPHABET
        if prev_row[prev_char_index] == -1:
            prev_row[prev_char_index] = i
    table.reverse()
    return table

def preprocess_good_suffix_rule_modified(pat):

    good_suffix = []

    #Getting the z suffix of the pattern
    reversed_pat = pat[::-1]
    z_arr = z_algorithm_for_boyer_moore(reversed_pat)
    z_suffix = z_arr[::-1]

    for j in range(len(pat)+1):
        good_suffix.append(-1)
    
    for i in range(len(pat)-1, -1, -1):    # backwards for leftmost p
        L = z_suffix[i]
        if L > 0:
            p = len(pat) - L       # where beta (suffix) starts
            k1 = i - L + 1         # alpha start = k+1
            good_suffix[k1] = p    # when mismatch at k=k1-1, shift to p

    # print("Z Suffix:", z_suffix)
    # print("Good Suffix", good_suffix)

    return good_suffix

txt = "babbaababaababaababab"
pat = "abcdeabcdeabcde"
pat1 = "cabbaabb"
pat2 = "aababaabab"
# preprocess_bad_char_rule_modified(pat, 126-37+1, ord('%'))
# preprocess_good_suffix_rule_modified(pat)
# preprocess_good_suffix_rule_modified(pat1)
# preprocess_good_suffix_rule_modified(pat2)
# print(preprocess_bad_char_rule_modified(pat1, 5, ord('a')))
# print(pattern_matching(txt, pat2))
# print(pattern_matching("abcabcabc","abc"))
# preprocess_good_suffix_rule_modified("aaa")
# preprocess_good_suffix_rule_modified("abcab")
# print(pattern_matching("abcxxabcababcab", "abcab"))
pattern_matching("abbabbaabba", "abba")
# preprocess_good_suffix_rule_modified("acaaa")
# print(preprocess_rx_table("aacab", 3, ord('a')))