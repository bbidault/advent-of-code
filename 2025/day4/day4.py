# https://adventofcode.com/2025/day/4


## Ingest the input file and returns its content in a list of lists.
#
# @param inputFilePath: the input file path.
# @return The given input in the form of a list of lists.
#
def ingestInput(inputFilePath: str) -> list:
    inputFile = open(inputFilePath, "r")
    lines = inputFile.readlines()
    inputFile.close()
    floor = []
    for line in lines:
        row = []
        for space in line[0:-1]:
            row.append(space)
        floor.append(row)
    return floor


## Compute the number of movable rolls and remove them (@ becomes .).
#  A movable roll is a roll surrounded by less than 4 other rolls.
#
# @param floor: the input, a list of lists describing the position of rolls
#               and empty spaces on the floor.
# @return the number of movable rolls.
#
def findMovableRolls(floor: list) -> int:
    mRolls = 0
    for col in range(len(floor)):
        for row in range(len(floor[col])):
            if floor[col][row] == "@":  # does the space of interest contains a roll
                count = 0
                for idx in range(-1, 2):
                    for jdx in range(-1, 2):
                        if idx == 0 and jdx == 0:
                            continue  # ignore the space of interest
                        if (
                            (col + idx >= 0)
                            and (col + idx < len(floor))
                            and (row + jdx >= 0)
                            and (row + jdx < len(floor[col]))
                            and floor[col + idx][row + jdx] == "@"
                        ):
                            count += 1
                if count < 4:
                    mRolls += 1
                    floor[col][row] = "."  # "remove" the roll
    return mRolls


## Compute the number of movable rolls.
#
# @param inputFilePath: the input file
# @return the number of movable rolls
#
def part1(inputFilePath: str) -> int:
    floor = ingestInput(inputFilePath)
    return findMovableRolls(floor)


## Compute the total number of movable rolls.
#
# @param inputFilePath: the input file
# @return The total number of the movable rolls
#
def part2(inputFilePath: str) -> int:
    floor = ingestInput(inputFilePath)
    mRoll = 0
    oldMRoll = -1
    while oldMRoll != mRoll:  # as long as the number of movable rolls keeps changing
        oldMRoll = mRoll
        mRoll += findMovableRolls(floor)
    return mRoll


print("Part 1 test:", part1("test_input.txt"))
print("Part 1 solution:", part1("input.txt"))
print("Part 2 test:", part2("test_input.txt"))
print("Part 2 solution:", part2("input.txt"))
