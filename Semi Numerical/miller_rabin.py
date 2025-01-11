import random
from modular_exponentiation import modular_exponentiation

def miller_rabin(n, k):
    """
    Perform the Miller-Rabin primality test on a number n.

    It determines if a number is likely prime or composite. It runs k iterations of the test, 
    where each iteration uses a different random base.

    Implementation based on pseudocode from Week 6 lecture notes.

    Parameters:
    n (int): The number to test for primality.
    k (int): The number of random bases to test with (higher k increases accuracy).

    Returns:
    bool: True if the number is probably prime, False if it is composite.
    """

    # handle small prime cases directly
    if n == 2 or n == 3:
        return True
    
    # even numbers greater than 2 are all composite
    if n % 2 == 0:
        return False
    
    # factor n - 1 as 2^s * t (find s and t)
    s = 0
    t = n - 1

    while t % 2 == 0:
        s = s + 1
        t = t // 2

    # perform k iterations of the test with random bases
    for _ in range(k):
        # choose a random base in the range [2, n - 2]
        a = random.randint(2, n - 2)

        # compute a^t % n
        current = modular_exponentiation(a, t, n)
        
        # if current == 1 or current == n - 1, it passes this round of testing
        if current == 1 or current == n - 1:
            continue
            
        # keep track of previous value as we square current
        for _ in range(s - 1):
            prev = current
            current = (prev ** 2) % n
            
            # if we find n - 1 at any point, this base passes
            if current == n - 1:
                break

            # if we find 1 and previous wasn't n - 1, definitely composite
            if current == 1 and prev != n - 1:
                return False
            
        else:
            # if we completed the loop without finding n - 1, check final value
            if current != n - 1:
                return False

    # probably prime
    return True

if __name__ == "__main__":
    example_numbers = [2, 3, 4, 17, 123, 561, 1023]
    # 561 is the smallest carmichael number (Fermat's liar, returns 1 but isn't a prime)

    for number in example_numbers: 
        if miller_rabin(number, 10):
            result = "prime"
        else:
            result = "composite"
        
        print(f"{number} is {result}")