
inputFile = open("input.txt", "r")
Lines = inputFile.readlines()
sum = 0
cards = []
for i in range(188):
   cards.append(1)
count = 0
for line in Lines:
   score = 0
   content = line.split("|")
   wNum = content[0].split(" ")
   mNum = content[1].split(" ")
   for num in mNum:
      if num.strip() in wNum:
         score += 1
   # print(str(score))
   for i in range(1, score + 1):
      if count + i < 188:
         cards[count + i] += cards[count]
   count += 1
for i in range(188):
   # print(cards[i])
   sum += cards[i]
print(sum)
inputFile.close()
