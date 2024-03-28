# https://adventofcode.com/2023/day/1

import sys


## Compute the sum of numbers made from the first and last instance of keyword numbers in the given input
#
# @param inputFilePath: the input file
# @param keywords: The keyword to search within the input words
# @return the sum of numbers made from the first and last instance of keyword numbers in the given input
#
def compute(inputFilePath: str, keywords: list) -> int:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   sum = 0
   tens = 0
   ones = 0
   for line in lines:
      firstNumPos = sys.maxsize
      lastNumPos = -1
      for idx in range(len(keywords)):
         pos = line.strip().find(keywords[idx])
         if pos < firstNumPos and pos != -1:
            firstNumPos = pos
            tens = idx % 10
         rpos = line.strip().rfind(keywords[idx])
         if rpos > lastNumPos and rpos != -1:
            lastNumPos = rpos
            ones = idx % 10
      sum += tens * 10 + ones
   return sum


numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

print("Part 1 test:", compute("part1_test_input.txt", numbers))
print("Part 1 solution:", compute("input.txt", numbers))
print("Part 2 test:", compute("part2_test_input.txt", numbers + words))
print("Part 2 solution:", compute("input.txt", numbers + words))
