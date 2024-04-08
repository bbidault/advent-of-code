# https://adventofcode.com/2023/day/13


# Find the symmetry in a list of strings
#
# @param list: a list of strings
# @return: the index of the symmetry or 0 if none
#
def findSymmetryInList(list: list) -> tuple:
   for i in range(len(list) - 1):
      symmetry = True
      idx = 0
      while i - idx >= 0 and i + 1 + idx < len(list):
         if list[i - idx] != list[i + 1 + idx]:
            symmetry = False
            break
         idx += 1
      if symmetry:
         return (i + 1)
   return 0  # no symmetry


# Find the symmetry in a table of characters
#
# @param table: a table of characters
# @return: the indexes of the symmetries or zeros if there are none
#
def findSymmetryInTable(table: list) -> tuple:
   horizontal = findSymmetryInList([row for row in table])
   rotated = list(zip(*table[::-1]))  # rotate the table to read the columns as rows
   vertical = findSymmetryInList([col for col in rotated])
   return (horizontal, vertical)


# Calculate and return the sum of the locations of the symmetries
#
# @param inputFilePath: the input file
# @return: the sum of the locations of the symmetries (time 100 if horizontal)
#
def part1(inputFilePath: str) -> int:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   answer = 0
   table = []
   for line in lines:
      if line.strip():
         subtable = []
         for char in line:
            if char in ".#":
               subtable.append(char)
         table.append(subtable)
      else:
         horizontal, vertical = findSymmetryInTable(table)
         answer += horizontal * 100 + vertical
         table = []
   return answer


# Find a new symmetry in a list of strings
#
# @param list: a list of strings
# @param knownSymmetry: a known symmetry
# @return: the index of the symmetry or 0 if no new one
#
def findNewSymmetry(list: list, knownSymmetry: int) -> int:
   for i in range(len(list) - 1):
      symmetry = True
      idx = 0
      while i - idx >= 0 and i + 1 + idx < len(list):
         if list[i - idx] != list[i + 1 + idx]:
            symmetry = False
            break
         idx += 1
      if symmetry and knownSymmetry != i + 1:
         return (i + 1)
   return 0  # no symmetry


# Identify and return the location of the new symmetry after clearing the "smudge"
#
# @param table: a table of characters
# @return: the index of the new symmetry (time 100 if horizontal)
#
def findSmudge(table: list) -> int:  # rename
   horizontal, vertical = findSymmetryInTable(table)
   for i in range(len(table)):
      for j in range(len(table[0])):
         # for each cell in the table, switch its value
         table[i][j] = "." if table[i][j] == "#" else "#"

         rowAsString = [row for row in table]

         newHorizontal = findNewSymmetry(rowAsString, horizontal)

         rotated = list(zip(*table[::-1]))  # rotate the table to read the columns as rows
         colAsString = [col for col in rotated]

         newVertical = findNewSymmetry(colAsString, vertical)

         table[i][j] = "." if table[i][j] == "#" else "#"  # revert the change

         if newHorizontal != 0 or newVertical != 0:
            return newHorizontal * 100 + newVertical


# Calculate and return the sum of the locations of the new symmetries after clearing the "smudges"
#
# @param inputFilePath: the input file
# @return: the sum of the locations of the new symmetries (time 100 if horizontal)
#
def part2(inputFilePath: str) -> int:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   answer = 0
   table = []
   for line in lines:
      if line.strip():
         subtable = []
         for char in line:
            if char in ".#":
               subtable.append(char)
         table.append(subtable)
      else:
         answer += findSmudge(table)
         table = []

   return answer


print("Part 1 test:", part1("test_input.txt"))
print("Part 1 solution:", part1("input.txt"))
print("Part 2 test:", part2("test_input.txt"))
print("Part 2 solution:", part2("input.txt"))
