#Completed
def pattern_matching(txt, pat):
    ORD_START_ALPHABET = 37
    ORD_END_ALPHABET = 126
    ALPHABET_SIZE = ORD_END_ALPHABET - ORD_START_ALPHABET + 1
    result = []
    n = len(pat)
    shift = len(txt) - 1
    start = -1

    p_table = preprocess_p_table(pat, ALPHABET_SIZE, ORD_START_ALPHABET)
    modified_rx_table = modified_preprocess_rx_table(pat, ALPHABET_SIZE, ORD_START_ALPHABET)


    while shift  >= n - 1:
        curr_index_pat = n - 1

        if start != -1:
            curr_index_pat = start
            start -= 1
        

        while curr_index_pat >= 0 and pat[curr_index_pat] == txt[curr_index_pat + (shift - n + 1)]:

            curr_index_pat -= 1
        
        if curr_index_pat >= 0 and curr_index_pat != n-1:

            total_matches = (n-1) - (curr_index_pat+1) + 1
            mismatch_txt_index = curr_index_pat + (shift - n + 1)
            ord_mismtach_txt_char = ord(txt[mismatch_txt_index]) - ORD_START_ALPHABET

            p = p_table[curr_index_pat+1][ord_mismtach_txt_char]

            # print("J:", shift-(n-1), "K + 1", curr_index_pat+1, "P Value", p)


            if p != -1:
                # shift -= n - p - 1
                shift -= total_matches - (n - p)
                start = p - 2
            else:
                leftmost_mismatch_to_right_of_k = modified_rx_table[curr_index_pat][ord_mismtach_txt_char]
                if leftmost_mismatch_to_right_of_k != -1:
                    shift -= leftmost_mismatch_to_right_of_k - curr_index_pat
                    start = -1
                else:
                    shift = mismatch_txt_index - 1
                    start = -1
        elif curr_index_pat == n-1:
            shift -= 1
            start = -1
        else:
            #Pattern has been found
            # print("J:", shift-(n-1), "K + 1", curr_index_pat+1, "P Value", p_table[0])
            start_point_match = shift-n+1
            result.append(start_point_match)
            #This would mean that there exists a beta starting at index 0 of pat
            if p_table[0] != -1:
                shift -= n - (n - p_table[0])
                start = p_table[0] -1
            #This would mean no beta exist starting at index point 0 of pat
            else:
                shift -= n
                start = -1
    
    return result

#######################
# Preprocess Functions
#######################

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

#COMPLETED
def preprocess_p_table(pat, ALPHABET_SIZE, ORD_START_ALPHABET):
    p_table = []
    m = len(pat)

    reversed_pat = pat[::-1]
    Z = z_algorithm_for_boyer_moore(reversed_pat)
    z_suffix = Z[::-1]

    p_table.append(-1)

    for i in range(1, m):
        p_table.append([])
        for j in range(ALPHABET_SIZE):
            p_table[i].append(-1)
    
    for j in range(m-1):
        L = z_suffix[j]
        if L == 0:
            continue
        start = j - L + 1
        if start == 0:
            p_table[0] = m - L
            continue
        p_value = m - L
        char_before_p = pat[m-L-1]
        p_table[start][ord(char_before_p)-ORD_START_ALPHABET] = p_value

    return p_table

#Completed
def modified_preprocess_rx_table(pat, ALPHABET_SIZE, START_ALPHABET):
    # Creates an Rx(k) table where for each character x,
    # store the leftmost position of occurrences of x in pat to the right of k
    table = []
    prev_row = [-1 for _ in range(ALPHABET_SIZE)]
    for i in range(len(pat) - 1, -1, -1):
        table.append(prev_row.copy())
        prev_char_index = ord(pat[i]) - START_ALPHABET
        prev_row[prev_char_index] = i   # always overwrite
    table.reverse()
    return table

# print((z_algorithm_for_boyer_moore(pat1[::-1]))[::-1])
# print(preprocess_p_table("aaaaaa", 2, ord('a')))
# print(pattern_matching("aaaaabaaaaaaaaaabaaaaa","aaaaabaaaaa"))
# print(pattern_matching("babbaababaababaababab","aababaabab"))
# print(modified_preprocess_rx_table("aadabcd", 4, ord('a')))
