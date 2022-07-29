# Part 1

with open('testinput.txt') as f:
    lines = [line.rstrip() for line in f]

def gamma_bin(i):
    zeroes = 0
    ones = 0
    for x in lines:
        if x[i] == '0':
            zeroes += 1
        else: ones += 1
    if zeroes > ones:
        return '0'
    else: return '1'

def epsilon_bin(i):
    zeroes = 0
    ones = 0
    for x in lines:
        if x[i] == '0':
            zeroes += 1
        else: ones += 1
    if zeroes < ones:
        return '0'
    else: return '1'

def rate(fun):
    rate_bin = ''
    i = 0
    while i < 12:
        rate_bin = rate_bin + fun(i)
        i += 1
    return rate_bin

gamma = int(rate(gamma_bin), 2)
epsilon = int(rate(epsilon_bin), 2)

print(gamma * epsilon)

# Part 2

def o2_bin(i, arr):
    zeroes = 0
    ones = 0
    for x in arr:
        if x[i] == '0':
            zeroes += 1
        else: ones += 1
    if zeroes > ones:
        return '0'
    else: return '1'

def co2_bin(i, arr):
    zeroes = 0
    ones = 0
    for x in arr:
        if x[i] == '0':
            zeroes += 1
        else: ones += 1
    if zeroes > ones:
        return '1'
    else: return '0'

def generator(fun):
    lines_gen = lines
    i = 0
    while i < 12:
        if len(lines_gen) == 1:
            break
        else: 
            bit_to_add = fun(i, lines_gen)
            lines_gen = list(filter(lambda x: x[i] == bit_to_add, lines_gen))
            i += 1
    return lines_gen[0]
        
o2 = int(generator(o2_bin), 2)
co2 = int(generator(co2_bin), 2)

print(o2 * co2)