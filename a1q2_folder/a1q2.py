#########################################
#  Pattern Match and Distance 1 Matches
#########################################
def pattern_match(txt, pat):

    STARTING_CHARACTER = ord('$')
    ENDING_CHARACTER = 126
    ALPHABET_SIZE = ENDING_CHARACTER - STARTING_CHARACTER + 1 #this includes the $ character
    n = len(pat)
    m = len(txt)+1 #length of text with dollar character
    result = []

    sp = 0
    ep = m-1

    #Preprocessing the txt
    bwt, suffix_arr, rank_arr, occ_table = construction_of_bwt(txt, STARTING_CHARACTER, ALPHABET_SIZE)

    #Pattern matching phase
    for i in range(n-1, -1, -1):
        char_index = ord(pat[i]) - STARTING_CHARACTER
        sp = rank_arr[char_index] + occ_table[sp][char_index]
        ep = rank_arr[char_index] + occ_table[ep+1][char_index] - 1
        if ep < sp:
            return []
    
    # recover txt positions from suffix array
    for i in range(sp, ep+1):
        result.append(suffix_arr[i])

    return result

######################################
#  BWT, F, Occ and Rank Construction
#####################################
def construction_of_bwt(txt, STARTING_CHARACTER, ALPHABET_SIZE):
    txt_with_dollar = txt + "$"
    suffix_array = []
    bwt = []

    # create (suffix_string, index) pairs
    pairs = []
    for i in range(len(txt_with_dollar)):
        pairs.append((txt_with_dollar[i:], i))

    # sort by suffix string (first element of pair)
    pairs.sort()

    # extract just the indices
    for suffix, i in pairs:
        suffix_array.append(i)

    # creating the bwt using SA indices
    for i in range(len(txt_with_dollar)):
        bwt.append(txt_with_dollar[suffix_array[i] - 1])

    #Getting the occurance table and rank array
    occ_table = build_occ_table(bwt, ALPHABET_SIZE, STARTING_CHARACTER)
    rank_array = build_rank_array(occ_table, bwt, ALPHABET_SIZE)

    return bwt, suffix_array, rank_array, occ_table

def build_occ_table(bwt, ALPHABET_SIZE, STARTING_CHARACTER):
    occ = [[0] * ALPHABET_SIZE]
    
    for char in bwt:
        char_index = ord(char) - STARTING_CHARACTER
        # copy entire previous row at once
        new_row = occ[-1].copy()
        new_row[char_index] += 1
        occ.append(new_row)
    return occ

def build_rank_array(occ_table, bwt, ALPHABET_SIZE):
    rank_array = [0] * ALPHABET_SIZE
    total = 0
    for i in range(ALPHABET_SIZE):
        rank_array[i] = total
        total_i_characters = occ_table[len(bwt)][i]
        total += total_i_characters
    return rank_array

print(pattern_match("googol","go"))