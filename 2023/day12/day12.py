# https://adventofcode.com/2023/day/12

import functools


# Recursive function that calculates and return the number of patterns matching the given parameters
#
# @param pattern: the incomplete pattern to match
# @param splits: the pattern defined as numbers of # seperated by .
# @return: the number of patterns matching the given parameters
#
@functools.lru_cache(maxsize=None)  # use memoization for performance
def findpatterns(pattern: list, splits: tuple) -> int:
   count = 0
   patternMaxStart = len(pattern) - sum(splits) - len(splits[1:])  # lenght of pattern - minimum length of pattern
   for idx in range(patternMaxStart + 1):  # + 1 buffer for range
      if all(char in "#?" for char in pattern[idx:idx + splits[0]]):  # if we can fit the full split (all can be #)
         if len(splits) == 1:  # if this is the last split to fit
            if all(char in ".?" for char in pattern[idx + splits[0]: len(pattern)]):  # if everything left in the pattern can be a .
               count += 1  # we have a matching pattern
         elif pattern[idx + splits[0]] in '.?':  # if we can have a . after the split
            count += findpatterns(pattern[idx + splits[0] + 1:], splits[1:])  # recurse on the remaining pattern and splits
      if pattern[idx] not in '.?':  # if we cannot fit the split in the pattern
         break  # we are done
   return count


# Calculate and returns the total number of valid patterns as defined by the given input
#
# @param inputFilePath: the input file
# @param multiplier: the number of times the pattern should be repeated
# @return: The total number of valid patterns
#
def solve(inputFilePath: str, multiplier: int) -> int:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   solution = 0
   for line in lines:
      content = line.split(" ")
      chars = content[0]
      splits = tuple(map(int, content[1].split(','))) * multiplier
      pattern = chars
      for _ in range(multiplier - 1):
         pattern += "?" + chars
      solution += findpatterns(pattern, splits)
   return solution


print("Part 1 test:", solve("test_input.txt", 1))
print("Part 1 solution:", solve("input.txt", 1))
print("Part 2 test:", solve("test_input.txt", 5))
print("Part 2 solution:", solve("input.txt", 5))
