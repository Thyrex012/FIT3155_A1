#########################################
#  Pattern Match and Distance 1 Matches
#########################################
def pattern_match(txt):
    
    return


######################################
#  BWT, F, Occ and Rank Construction
######################################
def construction_of_bwt(txt):
    STARTING_CHARACTER = ord('$')
    ENDING_CHARACTER = 126
    ALPHABET_SIZE = ENDING_CHARACTER - STARTING_CHARACTER + 1 #this includes the $ character
    txt_with_dollar = txt + "$"
    suffix_array = []
    F = []
    bwt = []
    #creating and sorting the suffix array
    for i in range(len(txt_with_dollar)):
        suffix_array.append(txt_with_dollar[i:])
    suffix_array = sorted(suffix_array)

    #creating the bwt
    for i in range(len(txt_with_dollar)):
        length_of_suffix = len(suffix_array[i])
        start_index = len(txt_with_dollar) - length_of_suffix
        bwt.append(txt_with_dollar[start_index - 1])
    
    #Getting the F array by sorting
    F = sorted(bwt)

    #Getting the occurance table and rank array
    occ_table = build_occ_table(bwt, ALPHABET_SIZE, STARTING_CHARACTER)
    rank_array = build_rank_array(occ_table, bwt, ALPHABET_SIZE)

    return bwt, F, rank_array, occ_table

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
