# https://adventofcode.com/2023/day/16

import sys
sys.setrecursionlimit(10000)


# A box of the focus beam defined by a list of labels and and focals
#
class contraption:
   # Constructor given an input file
   #
   # @param inputFilePath: the input file path
   #
   def __init__(self, inputFilePath: str):
      inputFile = open(inputFilePath, "r")
      lines = inputFile.readlines()
      inputFile.close()
      self.table = []
      self.visited = []
      for line in lines:
         if line.strip():
            subtable = []
            subvisited = []
            for char in line:
               if char in ".-|\\/":
                  subtable.append(char)
                  subvisited.append([])
            self.table.append(subtable)
            self.visited.append(subvisited)

   # Recursive function that generates the path of the laser beam through the contraption
   #
   # @param row: the row of interest
   # @param col: the column of interest
   # @param origin: where the laser beam is coming from in reference in reference to the location of interest
   #
   def visit(self, row, col, origin):
      if row >= 0 and col >= 0 and row < len(self.table) and col < len(self.table[0]) and origin not in self.visited[row][col]:
         self.visited[row][col].append(origin)
         if self.table[row][col] == ".":
            if origin == "N":
               self.visit(row + 1, col, "N")
            elif origin == "S":
               self.visit(row - 1, col, "S")
            elif origin == "W":
               self.visit(row, col + 1, "W")
            elif origin == "E":
               self.visit(row, col - 1, "E")
         elif self.table[row][col] == "-":
            if origin == "N" or origin == "S":
               self.visit(row, col + 1, "W")
               self.visit(row, col - 1, "E")
            elif origin == "W":
               self.visit(row, col + 1, "W")
            elif origin == "E":
               self.visit(row, col - 1, "E")
         elif self.table[row][col] == "|":
            if origin == "N":
               self.visit(row + 1, col, "N")
            elif origin == "S":
               self.visit(row - 1, col, "S")
            elif origin == "W" or origin == "E":
               self.visit(row + 1, col, "N")
               self.visit(row - 1, col, "S")
         elif self.table[row][col] == "\\":
            if origin == "N":
               self.visit(row, col + 1, "W")
            elif origin == "S":
               self.visit(row, col - 1, "E")
            elif origin == "W":
               self.visit(row + 1, col, "N")
            elif origin == "E":
               self.visit(row - 1, col, "S")
         elif self.table[row][col] == "/":
            if origin == "N":
               self.visit(row, col - 1, "E")
            elif origin == "S":
               self.visit(row, col + 1, "W")
            elif origin == "W":
               self.visit(row - 1, col, "S")
            elif origin == "E":
               self.visit(row + 1, col, "N")

   # Sum the number of visited cells
   #
   # @return: the number of visited cells
   #
   def countVisited(self):
      count = 0
      for row in range(len(self.visited)):
         for col in range(len(self.visited[row])):
            if self.visited[row][col]:
               count += 1
            self.visited[row][col] = []
      return count


# Count and return the sum of visited cell if the laser beam start from 0, 0 going westward
#
# @param inputFilePath: the input file
# @return: the sum of visited cell if the laser beam start from 0, 0 going westward
#
def part1(inputFilePath: str) -> int:
   cntrptn = contraption(inputFilePath)
   cntrptn.visit(0, 0, "W")
   return cntrptn.countVisited()


# Count and return the maximum sum of visited cell for any laser beam start position and direction
#
# @param inputFilePath: the input file
# @return: the maximum sum of visited cell for any laser beam start position and direction
#
def part2(inputFilePath: str) -> int:

   cntrptn = contraption(inputFilePath)

   candidates = []
   for k in range(len(cntrptn.table)):
      cntrptn.visit(k, 0, "W")
      candidates.append(cntrptn.countVisited())
      cntrptn.visit(k, len(cntrptn.table) - 1, "E")
      candidates.append(cntrptn.countVisited())

   for k in range(len(cntrptn.table[0])):
      cntrptn.visit(0, k, "N")
      candidates.append(cntrptn.countVisited())
      cntrptn.visit(len(cntrptn.table) - 1, k, "S")
      candidates.append(cntrptn.countVisited())

   return max(candidates)


print("Part 1 test:", part1("test_input.txt"))
print("Part 1 solution:", part1("input.txt"))
print("Part 2 test:", part2("test_input.txt"))
print("Part 2 solution:", part2("input.txt"))
