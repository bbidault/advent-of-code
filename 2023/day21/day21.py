# https://adventofcode.com/2023/day/21


# Ingest the given input into a table representing the gardens (maxSteps + 1) and rocks (-1)
# The output table captures 5 * 5 the input to enables walks of up to 327 steps for part 2
#
# @param inputFilePath: the input file
# @param maxSteps: the max number of steps this table will be used for
# @return: a table representing 5 * 5 input tables with numbers
#
def ingest(inputFilePath: str, maxSteps: int) -> list:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   lenInputTable = len(lines)
   table = [[-1] * lenInputTable * 5 for _ in range(lenInputTable * 5)]  # create a large table that includes 5 * 5 input tables
   for i in range(lenInputTable * 5):
      for j in range(lenInputTable * 5):
         if lines[i % lenInputTable][j % lenInputTable] in ".S":
            table[i][j] = maxSteps + 1
   return table


# Calculate and return the number of garden cells that can be reached from the given location
# with the number of steps walked and the total number of steps to walk as constraints.
#
# @param loc: the location in the map
# @param steps: the number of walked steps
# @param maxSteps: the total number of steps for this walk
# @param table: the map of gardens and rocks
# @return: the number of garden cells that can be reached from the given location
#
def recurse(loc: tuple, steps: int, maxSteps: int, table: list) -> int:
   sum = 0
   row, col = loc
   if ((steps <= maxSteps) and (row < len(table)) and (row >= 0) and (col < len(table[0])) and (col >= 0) and (table[row][col] > steps)):
      if table[row][col] == (maxSteps + 1) and (row + col) % 2 == (maxSteps % 2):
         sum = 1
      table[row][col] = steps
      sum += recurse((row + 1, col), steps + 1, maxSteps, table)
      sum += recurse((row - 1, col), steps + 1, maxSteps, table)
      sum += recurse((row, col + 1), steps + 1, maxSteps, table)
      sum += recurse((row, col - 1), steps + 1, maxSteps, table)
   return sum


# Calculate and return the number of garden cells that can be reached in 64 steps
#
# @param inputFilePath: the input file
# @return: the number of garden cells that can be reached in 64 steps
#
def part1(inputFilePath: str) -> int:
   return recurse((327, 327), 0, 64, ingest(inputFilePath, 64))


# Calculate and return the number of garden cells that can be reached in 26501365 steps by using Lagrange interpolation
#
# @param inputFilePath: the input file
# @return: the number of garden cells that can be reached in 26501365 steps
#
def part2(inputFilePath: str) -> int:
   # using Lagrange interpolation with
   x0 = 65
   y0 = recurse((327, 327), 0, x0, ingest(inputFilePath, x0))
   x1 = 196
   y1 = recurse((327, 327), 0, x1, ingest(inputFilePath, x1))
   x2 = 327
   y2 = recurse((327, 327), 0, x2, ingest(inputFilePath, x2))
   x = 26501365

   return (((x - x1) * (x - x2) / ((x0 - x1) * (x0 - x2))) * y0 +
           ((x - x0) * (x - x2) / ((x1 - x0) * (x1 - x2))) * y1 +
           ((x - x0) * (x - x1) / ((x2 - x0) * (x2 - x1))) * y2)


print("Part 1 solution:", part1("input.txt"))
print("Part 2 solution:", part2("input.txt"))
