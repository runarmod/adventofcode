groups = [groups for groups in open("../input.txt").read().split("\n\n")]
for i in range(len(groups)):
    groups[i] = groups[i].split("\n")

numQuestions = 0

for group in groups:
    questionsAllSaidYes = list(group[0])
    toBeRemoved = []
    for person in group:
        for question in questionsAllSaidYes:
            if question not in person:
                toBeRemoved.append(question)
    # print(toBeRemoved)
    toBeRemoved = list(set(toBeRemoved))
    for remove in toBeRemoved:
        # print(remove)
        questionsAllSaidYes.remove(remove)
    # print(questionsAllSaidYes)
    numQuestions += len(questionsAllSaidYes)

print(numQuestions)