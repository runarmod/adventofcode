import math


def is_prime(n):
    return all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))


print(sum(not is_prime(b) for b in range(107900, 124900 + 1, 17)))
