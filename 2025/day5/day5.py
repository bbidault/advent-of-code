# https://adventofcode.com/2025/day/5


## Compute and return the number of fresh ingredients in the given list
#  and the number of fresh ingredients in total.
#
# @param inputFilePath: the input file.
# @return the number of fresh ingredients in the given list
#         and the number of fresh ingredients in total.
#
def compute(inputFilePath: str) -> tuple:
    inputFile = open(inputFilePath, "r")
    lines = inputFile.readlines()
    inputFile.close()
    part1 = 0
    readRanges = True  # start by reading the ranges of fresh ingredients
    ranges = []
    for line in lines:
        if line.strip():
            if readRanges:  # ingest the input ingredient ranges
                bounds = line.split("-")
                ranges.append((int(bounds[0]), int(bounds[1])))
            else:  # part 1, identify if the ingredient of interest is fresh
                ingredient = int(line)
                for r in ranges:
                    if ingredient >= r[0] and ingredient <= r[1]:
                        part1 += 1
                        break
        else:
            # once we reach an empty line, stop reading ranges and start
            # reading ingredients
            readRanges = False
    # part 2, calculate the number of fresh ingredients in total
    part2 = 0
    freshes = sorted(ranges)
    currentIngredientOfInterest = freshes[0][0]
    for freshIdx in range(len(freshes)):  # for each range of fresh ingredients
        if currentIngredientOfInterest < freshes[freshIdx][0]:
            currentIngredientOfInterest = freshes[freshIdx][0]
        if currentIngredientOfInterest <= freshes[freshIdx][1]:
            # add the number of ingredients from the current to the end of the range
            part2 += freshes[freshIdx][1] - currentIngredientOfInterest + 1
            currentIngredientOfInterest = freshes[freshIdx][1] + 1
    return (part1, part2)


part1Test, part2Test = compute("test_input.txt")
part1, part2 = compute("input.txt")
print("Part 1 test:", part1Test)
print("Part 1 solution:", part1)
print("Part 2 test:", part2Test)
print("Part 2 solution:", part2)
