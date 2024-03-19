
scoreSigns = "J23456789TQKA"
twelvePowerOfFive = 13 * 13 * 13 * 13 * 13
twelvePowerOfFour = 13 * 13 * 13 * 13
twelvePowerOfThree = 13 * 13 * 13
twelvePowerOfTwo = 13 * 13
twelvePowerOfOne = 13
twelvePowerOfZero = 1


def evaluate(hand):
   buckets = []
   for i in range(13):
      buckets.append(0)
   for i in range(5):
      buckets[scoreSigns.find(hand[i])] += 1
   isFiveOfKind = False
   isFourOfKind = False
   isFullHouse = False
   isThreeOfKind = False
   isTwoPair = False
   isPair = False
   for i in range(1, 13):
      if buckets[i] == 5:
         isFiveOfKind = True
         break
      elif buckets[i] == 4:
         print(" " + str(i) + " ")
         isFourOfKind = True
         break
      elif buckets[i] == 3:
         if isPair:
            isFullHouse = True
            break
         else:
            isThreeOfKind = True
      elif buckets[i] == 2:
         if isPair:
            isTwoPair = True
            break
         elif isThreeOfKind:
            isFullHouse = True
            break
         else:
            isPair = True
   for i in range(buckets[0]):
      if isFourOfKind:
         # print(" isFourOfKind -> isFiveOfKind")
         isFourOfKind = False
         isFiveOfKind = True
      elif isFullHouse:
         # print(" isFullHouse -> isFiveOfKind")
         isFullHouse = False
         isFiveOfKind = True
      elif isThreeOfKind:
         # print(" isThreeOfKind -> isFourOfKind")
         isThreeOfKind = False
         isFourOfKind = True
      elif isTwoPair:
         # print(" isTwoPair -> isFullHouse")
         isTwoPair = False
         isFullHouse = True
      elif isPair:
         # print(" isPair -> isThreeOfKind")
         isPair = False
         isThreeOfKind = True
      else:
         # print(" isNone -> isPair")
         isPair = True

   value = 0
   if isFiveOfKind:
      print(" isFiveOfKind ", end='')
      value = twelvePowerOfFive * 6
   elif isFourOfKind:
      print(" isFourOfKind ", end='')
      value = twelvePowerOfFive * 5
   elif isFullHouse:
      print(" isFullHouse ", end='')
      value = twelvePowerOfFive * 4
   elif isThreeOfKind:
      print(" isThreeOfKind ", end='')
      value = twelvePowerOfFive * 3
   elif isTwoPair:
      print(" isTwoPair ", end='')
      value = twelvePowerOfFive * 2
   elif isPair:
      print(" isPair ", end='')
      value = twelvePowerOfFive * 1
   else:
      print(" is none ", end='')
      value = twelvePowerOfFive * 0
   value += scoreSigns.find(hand[0]) * twelvePowerOfFour + scoreSigns.find(hand[1]) * twelvePowerOfThree + scoreSigns.find(hand[2]
                                                                                                                           ) * twelvePowerOfTwo + scoreSigns.find(hand[3]) * twelvePowerOfOne + scoreSigns.find(hand[4]) * twelvePowerOfZero
   return value


inputFile = open("input.txt", "r")
Lines = inputFile.readlines()
sum = 0
scores = []
bids = []
hands = []
for line in Lines:
   content = line.split(" ")
   hand = content[0].strip()
   print(hand, end='')
   bid = int(content[1].strip())
   value = evaluate(hand)
   print(str(value))
   scores.append(value)
   bids.append(bid)
   hands.append(hand)
scores, bids, hands = zip(*sorted(zip(scores, bids, hands)))
for i in range(0, len(bids)):
   sum += bids[i] * (i + 1)
   print(hands[i] + " " + str(i + 1) + " * " + str(bids[i]) + " = " + str(bids[i] * (i + 1)) + " " + str(sum))
print(sum)
inputFile.close()
