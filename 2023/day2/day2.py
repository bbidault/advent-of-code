# https://adventofcode.com/2023/day/2


## Calculates and returns the sum of ids of game that respects the rule of maximum 12 red, 13 green and 13 blue cubes
#
# @param inputFilePath: the input file
# @return the sum of ids of game that respects the rule of maximum 12 red, 13 green and 13 blue cubes
#
def part1(inputFilePath: str) -> int:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   sum = 0
   for jdx in range(len(lines)):
      words = lines[jdx].replace(",", "").replace(";", "").split(" ")
      validGame = True
      for idx in range(len(words)):
         if (((words[idx].strip() == "red") and (int(words[idx - 1].strip()) > 12)) or
            ((words[idx].strip() == "green") and (int(words[idx - 1].strip()) > 13)) or
            ((words[idx].strip() == "blue") and (int(words[idx - 1].strip()) > 14))):
            validGame = False
            break
      if validGame:
         sum += jdx + 1
   return sum


## Calculates and returns the sum of the products of minimum required red, green and blue cubes for the game to be valid
#
# @param inputFilePath: the input file
# @return: the sum of the products of minimum required red, green and blue cubes for the game to be valid
#
def part2(inputFilePath: str) -> int:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   sum = 0
   for line in lines:
      maxRed = 0
      maxGreen = 0
      maxBlue = 0
      words = line.replace(",", "").replace(";", "").split(" ")
      for idx in range(len(words)):
         if (words[idx].strip() == "red") and (int(words[idx - 1].strip()) > maxRed):
            maxRed = int(words[idx - 1].strip())
         elif (words[idx].strip() == "green") and (int(words[idx - 1].strip()) > maxGreen):
            maxGreen = int(words[idx - 1].strip())
         elif (words[idx].strip() == "blue") and (int(words[idx - 1].strip()) > maxBlue):
            maxBlue = int(words[idx - 1].strip())
      sum += maxRed * maxGreen * maxBlue
   return sum


print("Part 1 test:", part1("test_input.txt"))
print("Part 1 solution:", part1("input.txt"))
print("Part 2 test:", part2("test_input.txt"))
print("Part 2 solution:", part2("input.txt"))
