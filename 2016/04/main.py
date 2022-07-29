import string

class FirstPart:
    def __init__(self, filename):
        self.file = open(filename).read().splitlines()
        self.rooms = [str(line[:-10] + line[-7:]).replace("-","").replace("]","").split("[") for line in self.file]
        for i in range(len(self.file)):
            self.rooms[i].append(int(self.file[i][-10:-7]))

        self.id_sum = 0
        for room in self.rooms:
            letters = {}
            unique = list(set(room[0]))
            for c in unique:
                letters[c] = room[0].count(c)
            top_5 = self.get_top_5_letters(letters)
            if top_5 == room[1]:
                self.id_sum += room[2]

    def get_top_5_letters(self, d):
        popular = ""
        while True:
            if len(d) < 1:
                break
            maksCount = 0
            maksLetter = ""
            for key, value in d.items():
                if value == maksCount:
                    if ord(maksLetter) > ord(key):
                        maksCount = value
                        maksLetter = key
                elif value > maksCount:
                    maksCount = value
                    maksLetter = key
            popular += maksLetter
            d.pop(maksLetter)
        return popular[:5]


class SecondPart:
    def __init__(self, filename):
        self.file = open(filename).read().splitlines()
        self.rooms = [str(line[:-10] + line[-7:]).replace("-"," ").replace("]","").split("[") for line in self.file]
        for i in range(len(self.file)):
            self.rooms[i].append(int(self.file[i][-10:-7]))


    def caesar(self, plaintext, shift):
        shift %= 26
        alphabet = string.ascii_lowercase
        shifted_alphabet = alphabet[shift:] + alphabet[:shift]
        table = str.maketrans(alphabet, shifted_alphabet)
        return plaintext.translate(table)
        


part1 = FirstPart("in.txt")
print("Part 1:", part1.id_sum)

part2 = SecondPart("in.txt")
print("Part 2: ", end="")

for room in part2.rooms:
    name = part2.caesar(room[0], room[2])
    if name[:len("northpole object storage")] == "northpole object storage":
        print(room[2])