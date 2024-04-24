# https://adventofcode.com/2023/day/18

import copy


# Calculate and return the area of the given polygon using the shoelace formula
# The vertices of the polygon are given through a direction and a number.
# E.g. R 10 means the next vertex is 10 to the right of the current vertex.
#
# @param inputFilePath: the input file defining the polygon
# @param part2: whether we are solving part 2 or not
# @return: the area of the given polygon
#
def solve(inputFilePath: str, part2=False) -> int:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   area = 0
   perimeter = 0
   initLoc = [0, 0]
   for line in lines:
      dir, num, col = line.split(" ")
      if part2:
         dir = str(col[7])
         num = int(col[2:7], 16)
      nextLoc = copy.deepcopy(initLoc)
      if dir in "R0":  # Right
         nextLoc[1] += int(num)
      elif dir in "D1":  # Down
         nextLoc[0] += int(num)
      elif dir in "L2":  # Left
         nextLoc[1] -= int(num)
      elif dir in "U3":  # Up
         nextLoc[0] -= int(num)
      area -= (initLoc[0] * nextLoc[1] - initLoc[1] * nextLoc[0]) / 2
      perimeter += int(num)
      initLoc = copy.deepcopy(nextLoc)
   return area + perimeter / 2 + 1


print("Part 1 test:", solve("test_input.txt"))
print("Part 1 solution:", solve("input.txt"))
print("Part 2 test:", solve("test_input.txt", True))
print("Part 2 solution:", solve("input.txt", True))
