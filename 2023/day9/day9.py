
inputFile = open("input.txt", "r")
Lines = inputFile.readlines()
sum = 0
for line in Lines:
   table = []
   numbers = line.split(" ")
   subtable = []
   for i in range(len(numbers) - 1, -1, -1):
      subtable.append(int(numbers[i]))
   table.append(subtable)
   allZeros = False
   idx = 0
   while False == allZeros:
      idx += 1
      subtable = []
      for i in range(len(table[idx - 1]) - 1):
         subtable.append(table[idx - 1][i + 1] - table[idx - 1][i])
      table.append(subtable)
      allZeros = True
      for i in range(len(table[idx])):
         if table[idx][i] != 0:
            allZeros = False
            break
   for i in range(len(table) - 2, -1, -1):
      table[i].append(table[i][len(table[i]) - 1] + table[i + 1][len(table[i + 1]) - 1])
   print(str(table[0][len(table[0]) - 1]))
   sum += table[0][len(table[0]) - 1]
print(sum)
inputFile.close()
