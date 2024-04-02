# https://adventofcode.com/2023/day/11


# Calculate and return the sum of distances between pairs of galaxies after expansion of the universe
#
# @param inputFilePath: the input file
# @param expansion: how much the universe expanded
# @return: the sum of distances between pairs of galaxies after expansion of the universe
#
def solve(inputFilePath: str, expansion: int) -> int:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()

   # ingest the input file into a table
   table = []
   for line in lines:
      subtable = []
      for char in line[:-1]:
         subtable.append(char)
      table.append(subtable)

   # populate a list of galaxies position
   galaxies = []
   for idx in range(len(table)):
      for jdx in range(len(table[idx])):
         if table[idx][jdx] == "#":
            galaxies.append([idx, jdx])

   # populate a list of empty rows
   emptyRows = []
   for idx in range(len(table)):
      isEmpty = True
      for char in table[idx]:
         if char == "#":
            isEmpty = False
            break
      if isEmpty:
         emptyRows.append(idx)

   # populate a list of empty columns
   emptyColumns = []
   for jdx in range(len(table[0])):
      isEmpty = True
      for idx in range(len(table)):
         if table[idx][jdx] == "#":
            isEmpty = False
            break
      if isEmpty:
         emptyColumns.append(jdx)

   # for each galaxy, update its position based on row expansion
   for galaxy in galaxies:
      add = 0
      for row in emptyRows:
         if galaxy[0] > row:
            add += expansion
      galaxy[0] += add

   # for each galaxy, update its position based on column expansion
   for galaxy in galaxies:
      add = 0
      for column in emptyColumns:
         if galaxy[1] > column:
            add += expansion
      galaxy[1] += add

   # sum the distances between each pair of galaxies
   sum = 0
   for source in galaxies:
      for target in galaxies:
         sum += abs(source[0] - target[0]) + abs(source[1] - target[1])

   return sum / 2  # divide by two since each distance will have been calculated twice (A to B and B to A)


print("Part 1 test:", solve("test_input.txt", 1))
print("Part 1 solution:", solve("input.txt", 1))
print("Part 2 test:", solve("test_input.txt", 99))
print("Part 2 solution:", solve("input.txt", 999999))
