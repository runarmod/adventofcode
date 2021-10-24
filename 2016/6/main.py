import collections

filename = "in.txt"

class Signals:
    def __init__(self, likelihood_index):
        self.input = open(filename).read().splitlines()
        self.likelihood_index = likelihood_index
        self.answer = self.findAnswer()
    
    def findAnswer(self):
        out = ""
        for i in range(len(self.input[0])):
            s = ""
            for j in range(len(self.input)):
                s += self.input[j][i]
            out += collections.Counter(s).most_common()[self.likelihood_index][0]
        return out

    
part1 = Signals(0)
print("Part 1:", part1.answer)

part2 = Signals(-1)
print("Part 2:", part2.answer)