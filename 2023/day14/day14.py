# https://adventofcode.com/2023/day/14


# Evaluates the load applied to the north support beam
# The load is the sum of the distances of rounded rocks (O) to the north side of the table
#
# @param table: a table representing the arrangement of the rocks
# @return: the load applied to the north support beam
#
def evaluate(table: list) -> int:
   load = 0
   for col in range(len(table[0])):
      for row in range(len(table)):
         if table[row][col] == "O":
            load += len(table) - row
   return load


# Move the rounded rocks (O) as far north as possible until they reach the edge of the table or a static rock (#)
#
# @param table: a table representing the arrangement of the rocks
# @return: the re-arranged table
#
def tiltNorth(table: list) -> list:
   newTable = [["."] * len(table[0]) for _ in range(len(table))]
   for col in range(len(table[0])):
      wall = 0
      for row in range(len(table)):
         if table[row][col] == "O":
            newTable[wall][col] = "O"
            wall += 1
         elif table[row][col] == "#":
            newTable[row][col] = "#"
            wall = row + 1
   return newTable


# Ingest the input file and return a table representing the arrangement of rocks (O and #)
#
# @param inputFilePath: the input file
# @return: a table representing the arrangement of rocks
#
def ingest(inputFilePath: str) -> list:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   table = []
   for line in lines:
      if line.strip():
         subtable = []
         for char in line:
            if char in ".#O":
               subtable.append(char)
         table.append(subtable)
   return table


# Calculate and return the load on the north support beam after tilting the platform toward the north
#
# @param inputFilePath: the input file
# @return: the load on the north support beam after tilting the platform toward the north
#
def part1(inputFilePath: str) -> int:
   table = ingest(inputFilePath)
   table = tiltNorth(table)
   return evaluate(table)


# Calculate and return the load on the north support beam after tilting the platform 1000000000 times in a north, west, south, east pattern
#
# @param inputFilePath: the input file
# @return: the load on the north support beam after tilting the platform 1000000000 times in a north, west, south, east pattern
#
def part2(inputFilePath: str) -> int:
   table = ingest(inputFilePath)
   seenGrids = []
   grids = []

   table = tiltNorth(table)
   tableStr = str.join("", [str.join("", k) for k in table])  # hashable type
   seenGrids.append(tableStr)
   grids.append(table)
   for cycle in range(1000000000):
      table = tiltNorth(table)
      table = list(zip(*table[::-1]))  # rotate
      table = tiltNorth(table)
      table = list(zip(*table[::-1]))  # rotate
      table = tiltNorth(table)
      table = list(zip(*table[::-1]))  # rotate
      table = tiltNorth(table)
      table = list(zip(*table[::-1]))  # rotate

      tableStr = str.join("", [str.join("", k) for k in table])
      if tableStr in seenGrids:
         break
      seenGrids.append(tableStr)
      grids.append(table)

   firstCycleGrid_idx = seenGrids.index(tableStr)
   finalGrid = grids[(1000000000 - firstCycleGrid_idx) % (cycle + 1 - firstCycleGrid_idx) + firstCycleGrid_idx]
   return evaluate(finalGrid)


print("Part 1 test:", part1("test_input.txt"))
print("Part 1 solution:", part1("input.txt"))
print("Part 2 test:", part2("test_input.txt"))
print("Part 2 solution:", part2("input.txt"))
