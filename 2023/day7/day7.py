# https://adventofcode.com/2023/day/7

import math


# Evaluates the given hand
#
# @param hand: the hand to evaluate
# @param part1: whether we should evaluate the hand with the rules of part 1 (True) or part 2 (False)
# @return: The score of the hand
#
def evaluate(hand: list, part1: bool) -> int:
   scoreSigns = "J23456789TQKA"
   if part1:
      scoreSigns = "23456789TJQKA"

   # one bucket per type of card, count the number of times each card appears
   buckets = []
   for idx in range(13):
      buckets.append(0)
   for card in hand:
      buckets[scoreSigns.find(card)] += 1

   # evaluate the type of the hand
   isFiveOfKind = False
   isFourOfKind = False
   isFullHouse = False
   isThreeOfKind = False
   isTwoPair = False
   isPair = False
   isHighCard = part1 or buckets[0] > 0  # cannot have a high card case if we are using part 2 rules and there is a joker (bucket[0])

   # evaluate high card case (every cards label are distinct)
   if isHighCard:
      for bucket in buckets:
         if bucket > 1:
            isHighCard = False
            break

   # evaluate case where two or more cards are not distinct
   if not isHighCard:
      rangeBegin = 0 if part1 else 1
      for idx in range(rangeBegin, 13):
         if buckets[idx] == 5:
            isFiveOfKind = True
            break
         elif buckets[idx] == 4:
            isFourOfKind = True
            break
         elif buckets[idx] == 3:
            if isPair:
               isFullHouse = True
               break
            else:
               isThreeOfKind = True
         elif buckets[idx] == 2:
            if isPair:
               isTwoPair = True
               break
            elif isThreeOfKind:
               isFullHouse = True
               break
            else:
               isPair = True

   # consider jockers (buckets[0]) in part 2
   if not part1:
      for idx in range(buckets[0]):
         if isFourOfKind:
            isFourOfKind = False
            isFiveOfKind = True
         elif isFullHouse:
            isFullHouse = False
            isFiveOfKind = True
         elif isThreeOfKind:
            isThreeOfKind = False
            isFourOfKind = True
         elif isTwoPair:
            isTwoPair = False
            isFullHouse = True
         elif isPair:
            isPair = False
            isThreeOfKind = True
         else:
            isPair = True

   # calculate the final score of the hand, since each card can take 13 values,
   # we multiply each evaluation step score by a decreasing powers of 13
   score = 0
   if isFiveOfKind:
      score = 7
   elif isFourOfKind:
      score = 6
   elif isFullHouse:
      score = 5
   elif isThreeOfKind:
      score = 4
   elif isTwoPair:
      score = 3
   elif isPair:
      score = 2
   elif isHighCard:
      score = 1

   score *= math.pow(13, 5)
   score += (scoreSigns.find(hand[0]) * math.pow(13, 4) + scoreSigns.find(hand[1]) * math.pow(13, 3) +
             scoreSigns.find(hand[2]) * math.pow(13, 2) + scoreSigns.find(hand[3]) * math.pow(13, 1) +
             scoreSigns.find(hand[4]))

   return score


# Sum the bid time ranking of each hands
#
# @param inputFilePath: the input file
# @param part1: whether we should evaluate the hand with the rules of part 1 (True) or part 2 (False)
# @return: the sum of the bids time the ranking of each hands
#
def solve(inputFilePath: str, part1: bool) -> int:
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   sum = 0
   scores = []
   bids = []
   hands = []
   for line in lines:
      content = line.split(" ")
      hand = content[0].strip()
      bid = int(content[1].strip())
      score = evaluate(hand, part1)
      scores.append(score)
      bids.append(bid)
      hands.append(hand)
   scores, bids, hands = zip(*sorted(zip(scores, bids, hands)))
   for idx in range(len(bids)):
      sum += bids[idx] * (idx + 1)
   return sum


print("Part 1 test:", solve("test_input.txt", True))
print("Part 1 solution:", solve("input.txt", True))
print("Part 2 test:", solve("test_input.txt", False))
print("Part 2 solution:", solve("input.txt", False))
