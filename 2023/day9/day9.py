# https://adventofcode.com/2023/day/9

# Calculate and return the sum of predicted numbers
#
# @param inputFilePath: the input file
# @param part1: whether we should predict the future (part 1, True) or the past (part 2, False)
# @return: the sum of predicted numbers
#
def solve(inputFilePath: str, part1: bool) -> int:
   sum = 0

   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   for line in lines:
      # ingest the input into a table of list of numbers
      numbers = line.split(" ")
      subtable = []
      if part1:
         for num in numbers:
            subtable.append(int(num))
      else:
         for jdx in range(len(numbers) - 1, -1, -1):  # prepare the initial list of numbers in reverse order for part 2
            subtable.append(int(numbers[jdx]))
      table = [subtable]

      # generate each consecutive history rows of the table until we have a row containing only zeros
      allZeros = False
      idx = 0
      while not allZeros:
         idx += 1
         subtable = []
         for jdx in range(len(table[idx - 1]) - 1):
            subtable.append(table[idx - 1][jdx + 1] - table[idx - 1][jdx])  # calculate the history for the current row
         table.append(subtable)
         allZeros = True
         for num in table[idx]:
            if num != 0:
               allZeros = False
               break

      # generate the prediction for each row
      for jdx in range(len(table) - 2, -1, -1):
         table[jdx].append(table[jdx][len(table[jdx]) - 1] + table[jdx + 1][len(table[jdx + 1]) - 1])

      sum += table[0][-1]
   return sum


print("Part 1 test:", solve("test_input.txt", True))
print("Part 1 solution:", solve("input.txt", True))
print("Part 2 test:", solve("test_input.txt", False))
print("Part 2 solution:", solve("input.txt", False))
