import itertools
import matplotlib.pyplot as plt
import numpy as np


class Printer:
    @staticmethod
    def show_sides(sides: dict[str, np.ndarray]):
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")

        size = len(sides["TOP"])
        for side, array in sides.items():
            for i, j in itertools.product(range(size), range(size)):
                x, y, z = 0, 0, 0
                match side:
                    case "TOP":
                        x, y, z = j, size - i, size + 1
                    case "BOTTOM":
                        x, y, z = j, i + 1, 0
                    case "LEFT":
                        x, y, z = -1, size - j, size - i
                    case "RIGHT":
                        x, y, z = size, j + 1, size - i
                    case "BACK":
                        x, y, z = size - j - 1, size + 1, size - i
                    case "FRONT":
                        x, y, z = j, 0, size - i
                value = array[i, j]
                # Red = "#", Green = path, Blue = empty
                color = (1, 0, 0) if value == "#" else (0, 0, 1) if value == "." else (0, 1, 0)
                ax.scatter(x, y, z, color=color, marker="s")

        ax.set_xlabel("X Label")
        ax.set_ylabel("Y Label")
        ax.set_zlabel("Z Label")

        plt.show()
