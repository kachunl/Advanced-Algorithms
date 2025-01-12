def find_z_array(pattern):
    """
    Calculates the Z-array for the given pattern string.

    The Z-array is an array where the value at each index "i" represents the length of the longest substring starting from "pattern[i]" that matches the prefix of the pattern. 

    Implemented with the help of the references above

    Approach:
    1. The function initialises a Z-array of the same length as the input pattern.
    2. It iterates over the pattern starting from the second character.
    3. The Z-array is computed by comparing the substring starting at each index with the prefix of the pattern:
        
        - Case 1 (Naive Comparison): If the current index "k" is outside the Z-box (a region where a previous match was found), the function compares the pattern's characters 
                                     naively to determine the Z-value for that position.
        
        - Case 2 (Inside Z-box): If the current index "k" is within the Z-box:
            - Case 2a: If the Z-value at the corresponding position in the Z-box is less than the remaining distance to the right boundary, the Z-value is directly copied.
            - Case 2b: If the Z-value reaches or exceeds the right boundary, a new comparison is made to extend the Z-box.

    Args:
        pattern (str): Pattern to be used.

    Returns:
        list: A list of integers representing the Z-array. The value at each index "i" gives the length of the longest prefix of "pattern" starting from "pattern[i]". 
    """

    # initialise "empty" z-array
    z_arr = [0 for _ in range(len(pattern))]

    z_arr[0] = pat_length = len(pattern)

    left, right = 0, 0
    
    # iterating through the pattern from the second character
    for k in range(1, pat_length):

        # case 1: k > r (outside z-box [naive comparisons])
        if k > right:
            left = right = k

            # expanding z-box by comparing the substring starting a k with the prefix, increment if its a match or its an unknown character
            while right < pat_length and pattern[right - left] == pattern[right]:
                right += 1

            # store length of match in z-array
            z_arr[k] = right - left
            right -= 1

        # case 2: k <= r (k is inside z-box)
        else:
            # k1 is the index relative to the start of the z-box
            k1 = k - left

            # case 2a: if the z-value at k1 is less than the remaining distance to the right boundary
            if z_arr[k1] < right - k + 1:
                z_arr[k] = z_arr[k1]

            # case 2b: if the z-value at k1 reaches or exceeds right boundary 
            else: 
                # shift z-box to start from k
                left = k

                # expanding z-box by comparing the substring starting a k with the prefix, increment if its a match or its an unknown character
                while right < pat_length and pattern[right - left] == pattern[right]:
                    right += 1
                
                # store length of match in z-array
                z_arr[k] = right - left
                right -= 1

    return z_arr

if __name__ == "__main__":
    print(find_z_array("abcabcasc"))