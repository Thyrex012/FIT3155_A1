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
                        f   g
               txt = ...baaaabaaaa
                         012345678
                     eg) aaaabaaaa say we have a full match so p_table[0]['b'] = 5, start = p-2 = 3
                     
                     When we start the next iteration instead of doing comparisons from 6<-7<-8 etc we immediatly skip
                     to 3 and perform comparisons from there to 0 until there's a mismatch with txt or a full match. We can
                     do this as we shifted the pattern leftwards so that pat's[4..8] now matches with txt's[f..g] shown below

               txt = ...baaaabaaaa
                    012345678
                eg) aaaabaaaa 

                     However as we perform our right to left scanning what happens when there's a mismatch and the p value
                     at k+1 is -1? That means that no p exist so we'll need to shift pat leftwards so that the mismatch txt
                     will now align with the end point of pat. Reason why this shift is safe is discussed in the report.

                     When there's a mismatch at pat[n-1] != txt[shift] that means that the alpha = 0, beta = 0, p = -1 so we 
                     shift leftwards by 1 and perform comparisons from there.
    
    Time Complexity: worst case O(n+m) where n is the length of pat and m is the length of txt. Reasoning in report

    Sapce Complexity: worst case O(n+m) where n is the length of pat and m is the length of txt. Reasoning in report
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
                # What we do here is we shift the pattern leftwards so that the mismatch's txt now aligns with the
                # the last character of pat, reasoning why this is safe is discussed in the report.
                shift = mismatch_txt_index
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

            if shift > n - 1:
                #Since its a full match we'll need to ensure that we can access the text index because if
                #shift = n-1 then that means that the txt index can potentially point past index 0 which is undefined
                txt_index = curr_index_pat + (shift - n + 1)
                textChar_index = ord(txt[txt_index]) - ORD_START_ALPHABET
                if p_table[0][textChar_index] != -1:
                    # Log this iteration: k+1 is 0 on a full match; p is p_table[0][textChar_index].
                    runlog.append((shift-(n-1), curr_index_pat+1, p_table[0][textChar_index]))
                    #This would mean that there exists a beta starting at index 0 of pat that also 
                    #matches with the text character
                    shift -= n - (n - p_table[0][textChar_index])
                    start = p_table[0][textChar_index] - 1
                else:
                    # Log this iteration: k+1 is 0 on a full match; p is -1 to represent no p.
                    runlog.append((shift-(n-1), curr_index_pat+1, -1))
                    #This would mean no beta exist starting at index point 0 of pat
                    shift -= n
                    start = -1
            else:
                # Log this iteration: k+1 is 0 on a full match; p is -1 to represent no p.
                runlog.append((shift-(n-1), curr_index_pat+1, -1))
                shift -= n
                start = -1
    
    return result, runlog

#######################
# Preprocess Functions
#######################

def z_algorithm(pat):
    """
    Gusfield's z algorithm that was learned during week 1 of the semeseter. It performs left to right shifting to get
    the Z array where z[i] represents the length of the longest substring starting at index i of str that matches its
    prefix. The algorithm runs in O(m) time where m is the length of the pattern.
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

    for i in range(0, m):
        p_table.append([])
        for j in range(ALPHABET_SIZE):
            p_table[i].append(-1)
    
    # We loop forward
    for j in range(m-1):
        L = z_suffix[j]
        if L == 0:
            continue
        start = j - L + 1
        p_value = m - L
        char_before_p = pat[p_value-1]
        p_table[start][ord(char_before_p)-ORD_START_ALPHABET] = p_value

    return p_table

def read_file(file_path: str) -> str:
    f = open(file_path, 'r')
    content = f.read()
    f.close()
    return content.rstrip('\n')

if __name__ == '__main__':
    #retrieve the file paths from the commandline arguments
    _, filename1, filename2 = sys.argv
    print("Number of arguments passed:", len(sys.argv))

    # Read the text and pattern strings.
    txt = read_file(filename1)
    pat = read_file(filename2)

    print("txt is", txt)
    print("pat is", pat)

    result, runlog = pattern_matching(txt, pat)

    with open('output_a1q1.txt', 'w') as f:
        for pos in result:
            f.write(str(pos+1) + '\n')
    
    with open("runlog_a1q1.txt", 'w') as f:
        for j, k_plus_one, p in runlog:
            f.write(str(j) + " " + str(k_plus_one) + " " + str(p) + "\n")