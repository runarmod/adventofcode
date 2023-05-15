d = input + 365*7
while 1:
    a=d
    while a != 0:
        b = a % 2
        a //= 2
        print(b)


# Prints the binary representation of d repeating starting from lsb
# Habe to find the lowest number such that `number + 365*7`s binary
# representation is in the form 1010...10
