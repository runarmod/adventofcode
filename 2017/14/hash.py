import functools


def knothash(data: str) -> str:
    def round(
        index: int, skipsize: int, numbers: list[int], lengths: list[int]
    ) -> tuple[int, int, list[int]]:
        for length in lengths:
            _numbers = numbers[index:] + numbers[:index]
            rev = _numbers[:length][::-1]
            _numbers = rev + _numbers[length:]
            numbers = _numbers[-index:] + _numbers[:-index]
            index = (index + length + skipsize) % len(numbers)
            skipsize += 1
        return index, skipsize, numbers

    def hash(lst: list[int]) -> list[int]:
        return [
            functools.reduce(lambda x, y: x ^ y, lst[i : i + 16], 0) for i in range(0, len(lst), 16)
        ]

    ascii_data = list(map(ord, data))
    numbers = list(range(256))
    standard_suffix = [17, 31, 73, 47, 23]

    index = 0
    skipsize = 0
    numbers = numbers[:]
    length_seq = ascii_data + standard_suffix

    for _ in range(64):
        index, skipsize, numbers = round(index, skipsize, numbers, length_seq)
    dense_hash = hash(numbers)
    return "".join(hex(num)[2:].zfill(2) for num in dense_hash)


if __name__ == "__main__":
    print(knothash("a0c2017"))
