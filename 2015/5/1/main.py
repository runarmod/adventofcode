with open("../input.txt", "r") as f:
    lines = f.readlines()

numberOfNiceWords = 0
vowels = "aeiou"
disgusting = ["ab", "cd", "pq", "xy"]




def checkAtleastThreeVowels(line):
    numberOfUniqueVowels = 0
    vowelsCopy = vowels
    for letter in line:
        if letter in vowelsCopy:
            numberOfUniqueVowels += 1
        if numberOfUniqueVowels >= 3:
            return True

    return False


def checkDoubleLetter(line):
    prevLetter = ""
    for letter in line:
        if letter == prevLetter:
            return True
        prevLetter = letter
    return False


def checkDisgustingSubString(line):
    for substring in disgusting:
        if substring in line:
            return True
    return False


for line in lines:
    atLeastThreeVowels = checkAtleastThreeVowels(line)
    doubleLetter = checkDoubleLetter(line)
    disgustingSubStrings = checkDisgustingSubString(line)
    
    if not atLeastThreeVowels:
        continue
    if not doubleLetter:
        continue
    if disgustingSubStrings:
        continue

    numberOfNiceWords += 1

print(numberOfNiceWords)