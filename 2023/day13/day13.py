
import math

inputFile = open("input.txt", "r")
Lines = inputFile.readlines()
answer = 0
table = []
count = 0
for line in Lines:
   if line.strip():
      subtable = []
      for char in line:
         if char in ".#":
            subtable.append(char)
      table.append(subtable)
   else:
      # print(table)

      vertical = -1
      horizontal = -1
      decFromBin = []
      for i in range(len(table)):
         decFromBin.append(0)
         for j in range(len(table[i])):
            # print(str(table[i][j]) + " ", end='')
            if table[i][j] == "#":
               # print("sum: " + str(decFromBin[i]), end='' )
               decFromBin[i] += math.pow(2, j)
               # print(" j: " + str(j) + " sum: " + str(decFromBin[i]) + ", ", end='')
      # print(decFromBin)
      for i in range(len(decFromBin) - 1):
         symmetry = True
         idx = 0
         while i - idx >= 0 and i + 1 + idx < len(decFromBin):
            if decFromBin[i - idx] != decFromBin[i + 1 + idx]:
               symmetry = False
               break
            idx += 1
         if symmetry:
            # print("table " + str(count) + " horizontal symmetry at " + str(i + 1))
            horizontal = i + 1
      decFromBin = []
      for i in range(len(table[0])):
         decFromBin.append(0)
         for j in range(len(table)):
            if table[j][i] == "#":
               decFromBin[i] += math.pow(2, j)
      # print(decFromBin)
      for i in range(len(decFromBin) - 1):
         symmetry = True
         idx = 0
         while i - idx >= 0 and i + 1 + idx < len(decFromBin):
            if decFromBin[i - idx] != decFromBin[i + 1 + idx]:
               symmetry = False
               break
            idx += 1
         if symmetry:
            # print("table " + str(count) + " vertical symmetry at " + str(i + 1))
            vertical = i + 1

      for k in range(len(table)):
         for l in range(len(table[0])):
            table[k][l] = "." if table[k][l] == "#" else "#"
            decFromBin = []
            for i in range(len(table)):
               decFromBin.append(0)
               for j in range(len(table[i])):
                  # print(str(table[i][j]) + " ", end='')
                  if table[i][j] == "#":
                     # print("sum: " + str(decFromBin[i]), end='' )
                     decFromBin[i] += math.pow(2, j)
                     # print(" j: " + str(j) + " sum: " + str(decFromBin[i]) + ", ", end='')
            # print(decFromBin)
            for i in range(len(decFromBin) - 1):
               symmetry = True
               idx = 0
               while i - idx >= 0 and i + 1 + idx < len(decFromBin):
                  if decFromBin[i - idx] != decFromBin[i + 1 + idx]:
                     symmetry = False
                     break
                  idx += 1
               if symmetry:
                  if horizontal != i + 1:
                     print("table " + str(count) + " horizontal symmetry at " + str(i + 1))
                     answer += (i + 1) * 100
            decFromBin = []
            for i in range(len(table[0])):
               decFromBin.append(0)
               for j in range(len(table)):
                  if table[j][i] == "#":
                     decFromBin[i] += math.pow(2, j)
            # print(decFromBin)
            for i in range(len(decFromBin) - 1):
               symmetry = True
               idx = 0
               while i - idx >= 0 and i + 1 + idx < len(decFromBin):
                  if decFromBin[i - idx] != decFromBin[i + 1 + idx]:
                     symmetry = False
                     break
                  idx += 1
               if symmetry:
                  if vertical != i + 1:
                     print("table " + str(count) + " vertical symmetry at " + str(i + 1))
                     answer += (i + 1)

            # if vertical > 0 or horizontal > 0:
            #     for i in range(len(table)):
            #         if horizontal == i:
            #             for j in range(len(table[0])):
            #                 print("-", end="")
            #             print()
            #         for j in range(len(table[0])):
            #             if vertical == j:
            #                 print("|", end="")
            #             print(table[i][j], end="")
            #         print()
            #     print()
            table[k][l] = "." if table[k][l] == "#" else "#"

      table = []
      count += 1

print(answer)
inputFile.close()
