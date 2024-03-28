# https://adventofcode.com/2023/day/3


## Parse the input file data into a table
#
# @param inputFilePath: the input file
# @return: the input data in a table
#
def parseInput(inputFilePath: str) -> list:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()

   table = []
   for line in lines:
      subtable = []
      for char in line.strip():
         subtable.append(char)
      table.append(subtable)
   return table


## Identify whether the specific table cell is surounded by a part sign or not
#
# @param table: the table representing the parts schematics
# @param row: the row number of the cell of interest
# @param col: the column number of the cell of interest
# @return: whether the specific table cell is surounded by a part sign or not
#
def isPart(table, row, col) -> bool:
   for idx in range(-1, 2, 1):
      for jdx in range(-1, 2, 1):
         if ((0 <= row + idx < len(table)) and
             (0 <= col + jdx < len(table[row + idx])) and
                 (table[row + idx][col + jdx] != ".") and
                 (table[row + idx][col + jdx].isnumeric() == False)):
            return True
   return False


## Get a full part number given the one of the table cell the number
#
# @param table: the table representing the parts schematics
# @param row: the row number of the cell of interest
# @param col: the column number of the cell of interest
# @return: the full part number given the one of the table cell the number
#
def getNum(table, row, col) -> int:
   units = int(table[row][col])
   tens = 0
   hundreds = 0
   if 0 <= col - 1 and table[row][col - 1].isnumeric():
      tens = int(table[row][col - 1])
      if 0 <= col - 2 and table[row][col - 2].isnumeric():
         hundreds = int(table[row][col - 2])
   if col + 1 < len(table) and table[row][col + 1].isnumeric():
      hundreds = tens
      tens = units
      units = int(table[row][col + 1])
      if col + 2 < len(table) and table[row][col + 2].isnumeric():
         hundreds = tens
         tens = units
         units = int(table[row][col + 2])
   return hundreds * 100 + tens * 10 + units


## Calculates and returns the sum of the parts number in the input file
#
# @param inputFilePath: the input file
# @return: the sum of the parts number in the input file
#
def part1(inputFilePath: str) -> int:
   table = parseInput(inputFilePath)

   sum = 0
   for row in range(len(table)):
      added = False
      for col in range(len(table[row])):
         if (False == added) and table[row][col].isnumeric() and isPart(table, row, col):
            sum += getNum(table, row, col)
            added = True
         elif (False == table[row][col].isnumeric()):
            added = False
   return sum


## Calculates and returns the sum of the gear ratios of all gears (*) in the input file
#
# @param inputFilePath: the input file
# @return: the sum of the gear ratios of all gears (*) in the input file
#
def part2(inputFilePath: str) -> int:
   table = parseInput(inputFilePath)

   sum = 0
   for row in range(1, len(table) - 1):
      for col in range(1, len(table[row]) - 1):
         if table[row][col] == "*":
            num = []
            if table[row - 1][col - 1].isnumeric() and table[row - 1][col] == ".":
               num.append(getNum(table, row - 1, col - 1))
            if table[row - 1][col].isnumeric():
               num.append(getNum(table, row - 1, col))
            if table[row - 1][col + 1].isnumeric() and table[row - 1][col] == ".":
               num.append(getNum(table, row - 1, col + 1))
            if table[row][col - 1].isnumeric():
               num.append(getNum(table, row, col - 1))
            if table[row][col + 1].isnumeric():
               num.append(getNum(table, row, col + 1))
            if table[row + 1][col - 1].isnumeric() and table[row + 1][col] == ".":
               num.append(getNum(table, row + 1, col - 1))
            if table[row + 1][col].isnumeric():
               num.append(getNum(table, row + 1, col))
            if table[row + 1][col + 1].isnumeric() and table[row + 1][col] == ".":
               num.append(getNum(table, row + 1, col + 1))
            if len(num) == 2:
               sum += num[0] * num[1]
   return sum


print("Part 1 test:", part1("test_input.txt"))
print("Part 1 solution:", part1("input.txt"))
print("Part 2 test:", part2("test_input.txt"))
print("Part 2 solution:", part2("input.txt"))
