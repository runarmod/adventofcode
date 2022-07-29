groups = [groups for groups in open("../input.txt").read().split("\n\n")]
for i in range(len(groups)):
    groups[i] = groups[i].split("\n")

numAnswers = 0

for group in groups:
    answers = []
    for person in group:
        for answer in person:
            if answer not in answers:
                answers.append(answer)
    numAnswers += len(answers)

print(numAnswers)