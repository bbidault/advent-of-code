# https://adventofcode.com/2023/day/17

from heapq import heappush, heappop


# The city class defines a city with a table of travelling costs
#
class city:
   # Constructor from an input file path
   #
   # @param inputFilePath: input file path
   #
   def __init__(self, inputFilePath: str):
      inputFile = open(inputFilePath, "r")
      lines = inputFile.readlines()
      inputFile.close()
      self.table = []
      for line in lines:
         if line.strip():
            subtable = []
            for char in line:
               if char in "0123456789":
                  subtable.append(int(char))
            self.table.append(subtable)

   #  Add a given cell to the given queue if it is a valid cell
   #
   # @param queue: queue of cells to visit for DFS
   # @param cost: cost of the cell
   # @param row: row of the cell
   # @param col: column of the cell
   # @param steps: number of steps travelled by the crucible in a straight line since the last turn
   # @param origin: origin of the crucible in regard to the cell (North, South, East, West)
   #
   def add(self, queue, cost, row, col, steps, origin):
      if row >= 0 and row < len(self.table) and col >= 0 and col < len(self.table[0]):
         heappush(queue, (cost + self.table[row][col], row, col, steps, origin))

   # Depth first search algorithm to find the path with the lowest cost from the top left
   # to the bottom right cells following the min and max steps constraints
   #
   # @param maxSteps: the maximum number of steps allowed going straight before turning
   # @param minSteps: the minimum number of steps allowed going straight before turning
   # @return: the cost of the cheapest path
   #
   def solve(self, maxSteps: int, minSteps=0) -> int:
      visited = set()
      queue = [(0, 0, 0, 0, "O")]

      while queue:
         cost, row, col, steps, origin = heappop(queue)

         if row == len(self.table) - 1 and col == len(self.table[row]) - 1:
            return cost

         if (row, col, steps, origin) in visited:
            continue

         visited.add((row, col, steps, origin))

         if origin == "N":
            if steps >= minSteps:
               self.add(queue, cost, row, col - 1, 1, "E")
               self.add(queue, cost, row, col + 1, 1, "W")
            if steps < maxSteps:
               self.add(queue, cost, row + 1, col, steps + 1, "N")
         elif origin == "S":
            if steps >= minSteps:
               self.add(queue, cost, row, col - 1, 1, "E")
               self.add(queue, cost, row, col + 1, 1, "W")
            if steps < maxSteps:
               self.add(queue, cost, row - 1, col, steps + 1, "S")
         elif origin == "E":
            if steps >= minSteps:
               self.add(queue, cost, row + 1, col, 1, "N")
               self.add(queue, cost, row - 1, col, 1, "S")
            if steps < maxSteps:
               self.add(queue, cost, row, col - 1, steps + 1, "E")
         elif origin == "W":
            if steps >= minSteps:
               self.add(queue, cost, row + 1, col, 1, "N")
               self.add(queue, cost, row - 1, col, 1, "S")
            if steps < maxSteps:
               self.add(queue, cost, row, col + 1, steps + 1, "W")
         else:
            self.add(queue, 0, row + 1, col, 1, "N")
            self.add(queue, 0, row, col + 1, 1, "W")


# Find the cheapeast path through the input map given the constraint of travelling a maximum of 3 cells straight before turning
#
# @param inputFilePath: the input file
# @return: the cheapeast path through the input map
#
def part1(inputFilePath: str) -> int:
   lavaTown = city(inputFilePath)
   return lavaTown.solve(3)


# Find the cheapeast path through the input map given the constraints of travelling
# a minimum of 4 cells and a maximum of 10 cells straight before turning
#
# @param inputFilePath: the input file
# @return: the cheapeast path through the input map
#
def part2(inputFilePath: str) -> int:
   lavaTown = city(inputFilePath)
   return lavaTown.solve(10, 4)


print("Part 1 test:", part1("test_input.txt"))
print("Part 1 solution:", part1("input.txt"))
print("Part 2 test:", part2("test_input.txt"))
print("Part 2 solution:", part2("input.txt"))
