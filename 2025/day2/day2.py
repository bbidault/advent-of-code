# https://adventofcode.com/2025/day/2


## Check if a given ID is invalid. An ID is invalid if it has the same pattern
#  repeated twice (E.g. 1212) for part 1. An ID is invalid if it has the same
#  pattern repeated twice or more (E.g. 121212) for part 2.
#
# @param id: The ID to check.
# @param part1: Whether we are checking validity for part 1 or 2.
# @return Whether the given ID is valid or not.
#
def isInvalid(id: str, part1: bool) -> bool:
    idLen = len(id)
    # an ID can have the same pattern twice and up to its length (E.g. 11111)
    for div in range(2, idLen + 1):
        if idLen % div == 0:
            subStr = id[0 : int(idLen / div)]  # get the potential pattern
            subStrLen = len(subStr)
            allEqual = True
            for idx in range(1, div):
                if subStr != id[idx * subStrLen : (idx + 1) * subStrLen]:
                    allEqual = False
                    break
            if allEqual:
                return True
        if part1:  # for part 1, check only if the pattern appears twice
            break
    return False


## Compute the number of invalid IDs within the given ranges of IDs.
#
# @param inputFilePath: the input file describing the ranges of IDs to check.
# @param part1: Whether we are checking validity for part 1 or 2.
# @return The number of invalid IDs within the given ranges of IDs.
#
def compute(inputFilePath: str, part1: bool) -> int:
    inputFile = open(inputFilePath, "r")
    lines = inputFile.readlines()
    inputFile.close()
    sum = 0  # sum of invalid IDs
    rangesStr = lines[0].split(",")
    for rangeStr in rangesStr:
        bounds = rangeStr.split("-")
        lowerBound = int(bounds[0])
        upperBound = int(bounds[1])
        for id in range(lowerBound, upperBound + 1):
            if isInvalid(str(id), part1):
                sum += id
    return sum


print("Part 1 test:", compute("test_input.txt", True))
print("Part 1 solution:", compute("input.txt", True))
print("Part 2 test:", compute("test_input.txt", False))
print("Part 2 solution:", compute("input.txt", False))
