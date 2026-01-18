# https://adventofcode.com/2025/day/7


## Move the beams and return the number of times the beams split.
#  Also update the number of overlapping beams.
#
# @param row: the row to update.
# @param space: the total space with beams and splitters.
# @return The number of times the beams split.
#
def moveBeams(row: int, space: list) -> int:
    splits = 0
    for col in range(len(space[row])):
        # if there is a beam above.
        if isinstance(space[row - 1][col], int) and space[row - 1][col] > 0:
            if space[row][col] == "^":
                splits += 1
                space[row][col - 1] += space[row - 1][col]
                space[row][col + 1] += space[row - 1][col]
            else:
                space[row][col] += space[row - 1][col]
    return splits


## Compute the number of times the beams split and the number of
#  overlapping beams at the bottom of the fixture.
#
# @param inputFilePath: the input file
# @return The number of times the beams split and the number of
#         overlapping beams at the bottom of the fixture.
#
def compute(inputFilePath: str) -> tuple:
    inputFile = open(inputFilePath, "r")
    lines = inputFile.readlines()
    inputFile.close()
    part1 = 0
    part2 = 0
    space = []
    for line in lines:
        row = []
        for character in line:
            if character == ".":
                row.append(0)
            elif character == "S":  # starting beam.
                # beams are represented by numbers superior to 0.
                row.append(1)
            elif character == "^":
                row.append("^")
        space.append(row)
    for row in range(1, len(space), 1):
        # move the beams row after row.
        part1 += moveBeams(row, space)
    for beams in space[-1]:
        # sum the total number of overlapping beams at the bottom of the fixture.
        part2 += beams
    return (part1, part2)


part1Test, part2Test = compute("test_input.txt")
part1, part2 = compute("input.txt")
print("Part 1 test:", part1Test)
print("Part 1 solution:", part1)
print("Part 2 test:", part2Test)
print("Part 2 solution:", part2)
