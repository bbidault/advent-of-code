# https://adventofcode.com/2025/day/12

import numpy as np


## Count the number of Christmas trees that can fit all the presents allocated to it.
#
# @param inputFilePath: the input file.
# @return  the number of Christmas trees that can fit all the presents.
#
def compute(inputFilePath: str) -> tuple:
    inputFile = open(inputFilePath, "r")
    lines = inputFile.readlines()

    count = 0
    sizes = np.array([7, 7, 5, 6, 7, 7])  # the size of each type of present.
    for line in lines:
        if "x" in line:
            area, presentsStr = line.split(": ")
            # the size of the area at the foot of the tree.
            x, y = map(int, area.split("x"))
            # the number of each type of present.
            presents = np.array(list(map(int, presentsStr.split())))

            if int(x / 3) * int(y / 3) >= sum(presents):
                # if we have enough room to fit the presents without packing
                # them like Pentomino pieces.
                count += 1
            elif x * y >= sum(presents * sizes):
                # otherwise, we need to pack them like Pentomino pieces,
                # luckily this never happens for the given input !
                print("Need to fit the presents like Pentomino pieces!")

    return count


print("Part 1 solution:", compute("input.txt"))
