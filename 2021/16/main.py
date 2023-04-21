import functools


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        bins = [bin(int(c, 16))[2:].zfill(4) for c in open(filename).read().rstrip()]
        self.data = "".join(bins)

        self.rip = 0
        self.return_pointer = 0
        self.sum_version_numbers = 0
        self.total_value = self.find_value(self.data, 0)[0]

    def get_3_bits_value(self, packet, rip):
        _id = packet[rip : rip + 3]
        rip += 3
        return int(_id, 2), rip

    def find_value(self, packet, rip):
        packet_version, rip = self.get_3_bits_value(packet, rip)
        type_id, rip = self.get_3_bits_value(packet, rip)
        self.sum_version_numbers += packet_version

        if type_id == 4:
            packet_value = ""
            _break = False
            while not _break:
                if packet[rip] == "0":
                    _break = True
                rip += 1
                packet_value += packet[rip : rip + 4]
                rip += 4
            packet_value = int(packet_value, 2)
            return packet_value, rip

        length_type_id = int(packet[rip])
        rip += 1

        packets = []
        if length_type_id == 0:  # 15 bits
            total_length = int(packet[rip : rip + 15], 2)
            rip += 15
            start_rip = rip
            while rip < start_rip + total_length:
                value, rip = self.find_value(packet, rip)
                packets.append(value)
        else:
            total_packets = int(packet[rip : rip + 11], 2)
            rip += 11
            for _ in range(total_packets):
                value, rip = self.find_value(packet, rip)
                packets.append(value)

        match type_id:
            case 0:
                return sum(packets), rip
            case 1:
                return functools.reduce(lambda x, y: x * y, packets), rip
            case 2:
                return min(packets), rip
            case 3:
                return max(packets), rip
            case 5:
                return int(packets[0] > packets[1]), rip
            case 6:
                return int(packets[0] < packets[1]), rip
            case 7:
                return int(packets[0] == packets[1]), rip
        raise RuntimeError("Should not reach here")

    def part1(self):
        return self.sum_version_numbers

    def part2(self):
        return self.total_value


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
