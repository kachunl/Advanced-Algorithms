def modular_exponentiation(a, b, n):
    """
    Perform modular exponentiation using repeated squaring.
    
    Implementation based on pseudocode from Week 6 lecture notes.

    Parameters:
    a (int): The base.
    b (int): The exponent.
    n (int): The modulus.

    Returns:
    int: The result of (a^b) % n.
    """
    
    # convert exponent to binary representation
    binary_representation = format(b, "b")
    result = 1

    # initialise base modulo n
    intermediate_result = a % n

    # loop through the binary representation from least significant bit
    for i in range(len(binary_representation) - 1, -1, -1):

        # if current bit is 1, multiply the result by the current base
        if binary_representation[i] == "1":
            result = (result * intermediate_result) % n

        # repeated squaring
        intermediate_result = (intermediate_result ** 2) % n

    return result

if __name__ == "__main__":
    print(modular_exponentiation(7, 560, 561))