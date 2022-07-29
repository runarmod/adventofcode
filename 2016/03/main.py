

class Triangle1:
    def __init__(self, file):
        self.lines = [[int(i) for i in list(filter(None, line.split(" ")))] for line in open(file).readlines()]

    def valid_triangle(self, triangle):
        sorted_triangle = sorted(triangle)
        valid = sorted_triangle[0] + sorted_triangle[1] > sorted_triangle[2]
        return 1 if valid else 0
    
    def get_valid_triangles(self):
        valid_triangles = 0
        for triangle in self.lines:
            valid_triangles += self.valid_triangle(triangle)
        return valid_triangles



class Triangle2:
    def __init__(self, file):
        self.lines = [[int(i) for i in list(filter(None, line.split(" ")))] for line in open(file).readlines()]
        self.columns = self.gather_tripples(self.get_columns(self.lines))

    def get_columns(self, inn):
        arr = []
        for i in range(len(inn[0])):
            for row in inn: 
                arr += [row[i]]
        return arr

    def gather_tripples(self, arr):
        new_arr = []
        for i in range(0, len(arr), 3):
            new_arr.append(arr[i:i+3])
        return new_arr

    def valid_triangle(self, triangle):
        s = sorted(triangle)
        valid = s[0] + s[1] > s[2]
        return 1 if valid else 0
    
    def get_valid_triangles(self):
        valid_triangles = 0
        for triangle in self.columns:
            valid_triangles += self.valid_triangle(triangle)
        return valid_triangles

part1 = Triangle1("in.txt")
print("Part 1:", part1.get_valid_triangles())


part2 = Triangle2("in.txt")
print("Part 2:", part2.get_valid_triangles())
