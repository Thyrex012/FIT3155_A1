import sys

def pattern_matching(txt, pat):
    """
    Given a txt and pat, the algorithm will match all occurances of pat in txt by breaking it down into 2 phases which
    is the preprocess and iterating phase.

    Preprocess Phase: During this phase we'll be running the preprocess_p_table to return the p_table such that when 
                      p_table[k+1][ord(mismatch_txt)-ord('%')] would return p such that both conditions within the 
                      assignment are satisfied. We'll also need to preprocess for the modified_rx_table which is a
                      modified version of the extended bad character table where instead of the table[i]['a']
                      showing the index of the rightmost 'a' thats to the left of index i we'll do the oppsite
                      where it'll represent the leftmost 'a' thats to the right of index i. The purpose of this
                      tbale will be discussed below
    
    Iteration Phase: During this phase we'll perform right to left scanning and shifting where the "shift" variable 
                     represents the end point of txt which aligns with the end point of pat. "start" variable 
                     represents the starting index within pat so that the next iteration can skip over a suffix 
                     that matched with the proper prefix of pat in the previous iteration. 

                         012345678
                     eg) aaaabaaaa say we have a full match so p_table[0] = 5, start = p-1 = 4
                     
                     When we start the next iteration instead of doing comparisons from 6<-7<-8 etc we immediatly skip
                     to 4 and perform comparisons from there to 0 until there's a mismatch with txt or a full match. However
                     if a mismatch occurs before index 0 of pat then when we shift pat to the left we'll start our comparison
                     at start = p - 2(only if p exists at pat[k+1]['x']) instead. The reason why is because we know that the 
                     mismatched character 'x' of txt in the previous iteration now aligns with the pat at index p - 1.

                     However as we perform our right to left scanning what happens when there's a mismatch and the p value
                     at k+1 is -1? That means that no p exist so another way we can safely shift leftwards is we can use the
                     modified_rx_table[k][mismatch_txt_char] to determine the leftmost occurance of the mismatch_txt_char 
                     thats to the right of k. If the table returns -1 then we know that there's no occurance at all to the 
                     right of k so we can perform an aggressive shift leftwards past the mismatch_txt_char. If the table 
                     returns a value t != -1 then we can shift the pat leftwards so that the mismatch_txt_char aligns with 
                     the pat[t] for the next iteration. We'll need to set the "start" for these 2 scenarios to -1 as we need 
                     to perform explicit comparisons from 0<-n-1 (n is length of pat).

                     When there's a mismatch at pat[n-1] != txt[shift] that means that the alpha = 0, beta = 0, p = -1 so we 
                     shift leftwards by 1 and perform comparisons from there.
    
    Time Complexity: Given n as the length of pat and m as the length of txt, The time complexity of the algorithm is bounded 
                     by the construction of p table, modified rx table and the number of comparisons performed. Both the p 
                     table and modified rx table takes O(n) time as the size of the alphabet for the algorithm is fixed at 
                     126-37+1 = 90. The numner of comparisons performed is bounded by m instead so the summation of these
                     3 would result in O(n+n+m) = O(n+m).

    Sapce Complexity: Given n as the length of pat and m as the length of txt the space complexity is bounded by the summation of
                      space of p table, modified rx table, result and runlog table. Both the p table and modified rx table are
                      bounded by O(n). Both the result and runlog table are bounded by O(m). Add these together we get
                      O(2n+2m) = O(n+m).
    """
    ORD_START_ALPHABET = 37
    ORD_END_ALPHABET = 126
    ALPHABET_SIZE = ORD_END_ALPHABET - ORD_START_ALPHABET + 1
    result = []
    runlog = []
    n = len(pat)
    m = len(txt)
    shift = len(txt) - 1
    start = -1

    if n > m:
        return result, runlog

    p_table = preprocess_p_table(pat, ALPHABET_SIZE, ORD_START_ALPHABET)
    modified_rx_table = modified_preprocess_rx_table(pat, ALPHABET_SIZE, ORD_START_ALPHABET)

    # The while loop stops when our shift value ends at n-1 as shifting leftwards past 
    # this will make the pattern go out of bound.
    while shift  >= n - 1:
        curr_index_pat = n - 1

        # Check to see if there is a start value from the previous iteration so that we can skip
        if start != -1:
            curr_index_pat = start
            start -= 1
        
        while curr_index_pat >= 0 and pat[curr_index_pat] == txt[curr_index_pat + (shift - n + 1)]:

            curr_index_pat -= 1
        
        if curr_index_pat >= 0 and curr_index_pat != n-1:

            total_matches = (n-1) - (curr_index_pat+1) + 1
            mismatch_txt_index = curr_index_pat + (shift - n + 1)
            mismtach_txt_char = ord(txt[mismatch_txt_index]) - ORD_START_ALPHABET

            p = p_table[curr_index_pat+1][mismtach_txt_char]

            # Log this iteration: j, k+1, p
            runlog.append((shift-(n-1), curr_index_pat + 1, p))

            if p != -1:
                # p value exists that satisfies condition 1 and 2 so we can shift the pattern to the left so that
                # the mismatched txt char aligns with p-1 and the proper prefix of alpha/pat [k+1...n-1] aligns with
                # a suffix of alpha/pat.
                shift -= total_matches - (n - p)
                start = p - 2
            else:
                leftmost_mismatch_to_right_of_k = modified_rx_table[curr_index_pat][mismtach_txt_char]
                if leftmost_mismatch_to_right_of_k != -1:
                    # p value doesnt exist so instead of naively shifting leftwards by 1 what we can do is we can determine
                    # the leftmost instance of the mismatched character(in txt) thats to the right of k in pat instead. This
                    # allows for a much more aggressive shift that is safe as well since txt[mismatch_txt_index] aligns
                    # with the leftmost occurance pat[leftmost_mismatch_to_right_of_k]
                    shift -= leftmost_mismatch_to_right_of_k - curr_index_pat
                    start = -1
                else:
                    # Since the mismatched character doesn't exist then we know for sure that txt[mismatch_txt_index] 
                    # wouldnt match with characters from pat[k+1..m-1] so we'll shift our pattern past this point.
                    shift = mismatch_txt_index - 1
                    start = -1
        elif curr_index_pat == n-1:
            # Mismatch at the last character in pattern, can shift pat by 1 leftwards.
            runlog.append((shift-(n-1), curr_index_pat + 1, -1))
            shift -= 1
            start = -1
        else:
            #Pattern has been found
            start_point_match = shift-n+1
            result.append(start_point_match)

            # Log this iteration: k+1 is 0 on a full match; p is p_table[0].
            runlog.append((shift-(n-1), curr_index_pat+1, p_table[0]))

            if p_table[0] != -1:
                #This would mean that there exists a beta starting at index 0 of pat
                shift -= n - (n - p_table[0])
                start = p_table[0] -1
            else:
                #This would mean no beta exist starting at index point 0 of pat
                shift -= n
                start = -1
    
    # return result, runlog
    return result

#######################
# Preprocess Functions
#######################

def z_algorithm(pat):
    """
    Gusfield's z algorithm that was learned during week 1 of the semeseter. It performs left to right shifting to get
    the Z array where z[i] represents the length of the longest substring starting at index i of str that matches its
    prefix. The algorithm runs in O(m) time where m is the length of the pattern because the right value always moves
    forward in every iteration.
    """
    str = pat
    z_array = [-1] * len(str)
    left = 0
    right = 0
    for k in range(1, len(str)):
        # This means that we have move past the right most z box so far so we're forced
        # to do explicit comparisons until there's a mismatch and if the length is greater than
        # 0 then we can set the left and right values to the right most z box's start and end
        if k > right:
            counter = 0
            while counter+k < len(str) and str[counter] == str[counter + k]:
                counter += 1
            z_array[k] = counter
            if z_array[k] > 0:
                left = k
                right = k + z_array[k] - 1
        else:
            if z_array[k-left] < right - k + 1:
                # This branch represents a scenario where k <= right and red box is smaller than the green box. 
                # As a result we can take advantage of the previous z's boxes value at index k-left to determine 
                # the z value at k.
                z_array[k] = z_array[k-left]
            else:
                # This branch represents a scenario where k <= right and red box is equal to or greater than the green box.
                # we know that str[k..right] matches with str[k-left...right-left] so we'll need to perform comparisons
                # from str[counter] with str[counter+k] or str[r+1] and onwards as we're unsure if they'll match each other.
                counter = right - k + 1
                z_array[k] = counter
                while counter+k < len(str) and str[counter] == str[counter + k]:
                    counter += 1
                z_array[k] = counter
                left = k
                right = k + z_array[k] - 1

    return z_array

def preprocess_p_table(pat, ALPHABET_SIZE, ORD_START_ALPHABET):
    """
    The helper function is used to construct p_table[k+1][ord(x)] = p where k+1 is the position just after mismatch k, x is
    the character before index p and p represents the leftmost index > k+1 such that it satisfies 2 conditions. The time and
    space complexity to construct the table is O(m*E) where m is the length of the pattern and E is the size of the alphabet. 
    Since the size of the alphabet used for the assignment is constant at 90 then that means that the time and space 
    complexity is bounded by m only so time and space complexity becomes O(m).

    Condition 1: pat[k+1...k+m-p+1] = pat[p..m] where 0 <= k <= m. Another way to think about this is that pat[k+1...k+m-p+1]
                 is the proper prefix of pat[k+1...m] = alpha that matches with a suffix of pat.
    
    Condition 2: pat[p-1] = txt[j+k-1] where we'll align the pat[p-1..m] with txt[j+k-1..beta] in the next iteration
    """
    p_table = []
    m = len(pat)

    # The z_suffix[i] stores the length of the longest substring ending at 
    # index i that matches with the suffix of pat
    reversed_pat = pat[::-1]
    Z = z_algorithm(reversed_pat)
    z_suffix = Z[::-1]

    # The p_table's index starts from 0 to m-1 due to the append before the for loop. 
    # Each p_table[1 to m-1] will contain E number of elements where E is the size of the 
    # alphabet with the exception at index 0 where it'll only contain a number
    p_table.append(-1)
    for i in range(1, m):
        p_table.append([])
        for j in range(ALPHABET_SIZE):
            p_table[i].append(-1)
    
    # The left most p would mean that the beta is bigger and moving from left to right within 
    # the z_suffix, the length increases so that means that if we go further rightward if we encounter 
    # another z_suffix value that starts at the same point via start = j - L + 1 and the char_before_p
    # is the same then we'll overwrite p_table[start][ord(char_before_p)-ORD_START_ALPHABET] with 
    # the new p_value. This also applies to a scenario where the start point is 0 and we dont need to worry about
    # the char_before_p in this case because the character before index 0 is always null.
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

def modified_preprocess_rx_table(pat, ALPHABET_SIZE, START_ALPHABET):
    """
    Creates an Rx[k]['x'] = t table where k represents an index in pat, 'x' is one of the possible characters 
    within the alphabet and t is the leftmost occurance of 'x' that is to the right of k. If Rx[k]['x'] = -1 then 
    that means that no character x exists that is to the right of index k of pat

    The time and space complexity of the algorithm is O(m) where is the length of pat. as the size of the alphabet 
    is constant. The process of reversing the elements within the table takes m time as well and the for loop run 
    based off of m so O(m+m) = O(2m) = O(m)
    """
    table = []
    prev_row = [-1 for _ in range(ALPHABET_SIZE)]
    for i in range(len(pat) - 1, -1, -1):
        table.append(prev_row.copy())
        prev_char_index = ord(pat[i]) - START_ALPHABET
        prev_row[prev_char_index] = i
    table.reverse()
    return table

# def read_file(file_path: str) -> str:
#     f = open(file_path, 'r')
#     content = f.read()
#     f.close()
#     return content.rstrip('\n')

# if __name__ == '__main__':
#     #retrieve the file paths from the commandline arguments
#     _, filename1, filename2 = sys.argv
#     print("Number of arguments passed:", len(sys.argv))

#     # Read the text and pattern strings.
#     txt = read_file(filename1)
#     pat = read_file(filename2)

#     print("txt is", txt)
#     print("pat is", pat)

#     result, runlog = pattern_matching(txt, pat)

#     with open('output_a1q1.txt', 'w') as f:
#         for pos in result:
#             f.write(str(pos+1) + '\n')
    
#     with open("runlog_a1q1.txt", 'w') as f:
#         for j, k_plus_one, p in runlog:
#             f.write(str(j) + " " + str(k_plus_one) + " " + str(p) + "\n")