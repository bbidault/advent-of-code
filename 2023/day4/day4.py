# https://adventofcode.com/2023/day/4


##
# Parse the input and return a list of winning and matching numbers
#
# @param inputLine: a single input line
# @return: a list of winning and matching numbers
#
def parseInput(inputLine: str) -> tuple:
   content = inputLine.split(":")[1].strip().split("|")
   wNum = content[0].strip().split(" ")
   wNum = list(filter(None, wNum))
   mNum = content[1].strip().split(" ")
   mNum = list(filter(None, mNum))
   return (wNum, mNum)


##
# Calculate the total score using the rule that the first matching pair gives 1 point and each following matching number doubles the points
#
# @param inputFilePath: the input file
# @return: the total score using the rule that the first matching pair gives 1 point and each following matching number doubles the points
#
def part1(inputFilePath: str) -> int:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   sum = 0
   for line in lines:
      wNum, mNum = parseInput(line)  # winning number and matching numbers
      score = 0
      for num in mNum:
         if num in wNum:
            if score == 0:
               score = 1
            else:
               score = score * 2
      sum += score
   return sum


##
# Calculate the total number of won cards using the rule that each cards gives one of each next n card for n matching numbers
#
# @param inputFilePath: the input file
# @return: the total number of won cards using the rule that each cards gives one of each next n card for n matching numbers
#
def part2(inputFilePath: str) -> int:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   sum = 0
   # initialize the list of cards with one of each
   cards = []
   for idx in range(len(lines)):
      cards.append(1)
   # for each line/card
   for idx in range(len(lines)):
      wNum, mNum = parseInput(lines[idx])  # winning number and matching numbers
      score = 0  # the score of the card / the sum of matching numbers
      for num in mNum:
         if num in wNum:
            score += 1
      # update the list of cards with the newly won cards
      for jdx in range(1, score + 1):
         if idx + jdx < len(cards):
            cards[idx + jdx] += cards[idx]
   # sum the total of cards
   for idx in range(len(lines)):
      sum += cards[idx]
   return sum


print("Part 1 test:", part1("test_input.txt"))
print("Part 1 solution:", part1("input.txt"))
print("Part 2 test:", part2("test_input.txt"))
print("Part 2 solution:", part2("input.txt"))
