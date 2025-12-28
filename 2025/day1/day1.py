# https://adventofcode.com/2025/day/1


## Compute for part 1 the number of times the dial of the safe points at 0
#  at the end of a movement and for part 2 the number of times the dial
#  points at 0 in total.
#
# @param inputFilePath: the input file describing the movements of the dial.
# @return the number of times the dial of the safe points at 0 at the end of
#         a movement for part 1 and the number of times the dial of the safe
#         points at 0 in total for part 2.
#
def compute(inputFilePath: str) -> tuple:
    inputFile = open(inputFilePath, "r")
    lines = inputFile.readlines()
    inputFile.close()
    part1 = 0
    part2 = 0
    position = 50  # starting position of the dial
    for line in lines:  # each line describes a movement
        direction = -1 if (line[0] == "L") else 1
        rotations = int(line[1:])
        while rotations > 0:  # simulate all clicks of the dial
            position += direction
            position %= 100  # dial with numbers from 0 to 99
            if position == 0:
                part2 += 1
            rotations -= 1
        if position == 0:
            part1 += 1
    return (part1, part2)


part1Test, part2Test = compute("test_input.txt")
part1, part2 = compute("input.txt")
print("Part 1 test:", part1Test)
print("Part 1 solution:", part1)
print("Part 2 test:", part2Test)
print("Part 2 solution:", part2)
