data = tuple(map(int, open("input.txt").read().rstrip().split(" ")))


def parse_node(data):
    child_count, meta_count, data = *data[:2], data[2:]
    scores = []
    this_tot = 0

    for _ in range(child_count):
        data, score, child_tot = parse_node(data)
        this_tot += child_tot
        scores.append(score)

    meta_sum = sum(metadatas := data[:meta_count])

    return (
        (data[meta_count:], meta_sum, meta_sum)
        if child_count == 0
        else (
            data[meta_count:],
            sum(scores[index - 1] for index in metadatas if 0 < index <= child_count),
            meta_sum + this_tot,
        )
    )


print(parse_node(data)[1:][::-1])
