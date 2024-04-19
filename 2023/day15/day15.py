# https://adventofcode.com/2023/day/15


# Ingest the input file and return a list of command strings
#
# @param inputFilePath: the input file path
# @return: a list of command strings
#
def ingest(inputFilePath: str) -> list:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   input = [str(step.strip()) for step in lines[0].split(",")]
   return input


# A box of the focus beam defined by a list of labels and and focals
#
class box:
   # Constructor without parameters
   #
   def __init__(self):
      self.labels = []
      self.focals = []


# Get and return the HASH (Holiday ASCII String Helper) code of an input string
#
# @param input: an input string
# @return: the HASH code of the input string
#
def getHash(input: str) -> int:
   number = 0
   for char in input:
      number += ord(char)
      number *= 17
      number %= 256
   return number


# Return the sum of the HASH codes of the input file commands
#
# @param inputFilePath: the input file path
# @return: the sum of the HASH codes of the input file commands
#
def part1(inputFilePath: str) -> int:
   answer = 0
   inputs = ingest(inputFilePath)
   for input in inputs:
      answer += getHash(input)
   return answer


# Set the focals by following the HASHMAP (Holiday ASCII String Helper Manual Arrangement Procedure) and return the total focusing power
#
# @param inputFilePath: the input file
# @return: the total focusing power
#
def part2(inputFilePath: str) -> int:
   inputs = ingest(inputFilePath)

   boxes = []
   for i in range(256):
      boxes.append(box())

   # set the focals by following the input commands
   for input in inputs:
      length = len(input)
      label = ""
      sign = ""
      focal = 0
      if input[length - 1] == "-":
         label = input[0:length - 1]
         sign = "-"
      else:
         label = input[0:length - 2]
         sign = "="
         focal = int(input[length - 1])
      hash = getHash(label)
      if label in boxes[hash].labels:
         idx = boxes[hash].labels.index(label)
         if sign == "=":
            boxes[hash].focals[idx] = focal
         else:
            del boxes[hash].labels[idx]
            del boxes[hash].focals[idx]
      else:
         if sign == "=":
            boxes[hash].labels.append(label)
            boxes[hash].focals.append(focal)

   # calculate the total focusing power
   answer = 0
   for i in range(len(boxes)):
      for j in range(len(boxes[i].focals)):
         answer += (i + 1) * (j + 1) * boxes[i].focals[j]

   return answer


print("Part 1 test:", part1("test_input.txt"))
print("Part 1 solution:", part1("input.txt"))
print("Part 2 test:", part2("test_input.txt"))
print("Part 2 solution:", part2("input.txt"))
