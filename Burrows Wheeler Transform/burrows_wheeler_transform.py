def suffix_array_to_bwt(text, suffix_array):
    """
    Computes BWT of the input text using the provided suffix array.

    Args:
        text (str): The original string from which BWT will be computed.
        suffix_array (list): The suffix array of the original string.

    Returns:
        str: The BWT of the input text.
    """

    # append a unique terminator to the text to handle BWT properly
    extended_text = text + "$"
    bwt = ""
    
    # iterate over each index in the suffix array
    for i in suffix_array:
         # if the suffix starts at the beginning, append the last character
        if i == 0:
            bwt += extended_text[-1]
        
        # else, append the character just before the start of the suffix
        else:
            bwt += extended_text[i - 1]
    
    return bwt

if __name__ == "__main__":
    text = "banana"
    suffix_array = [6, 5, 3, 1, 0, 4, 2]

    print(suffix_array_to_bwt(text, suffix_array))