# https://adventofcode.com/2023/day/8


# Read the input file and return its content as a tuple of directions (string) and dictionary mapping source to target locations
#
# @param inputFilePath: the input file
# @return: The content of the input file in a data structure
#
def ingestInput(inputFilePath: str):
   inputFile = open(inputFilePath, "r")
   lines = inputFile.readlines()
   inputFile.close()
   directions = lines[0].strip()
   map = {}
   for line in lines[2:]:
      source, targets = line.strip().split(" = ")
      map[source] = [targets[1:4], targets[6:9]]
   return (directions, map)


# Calculate the number of steps to travel through a given graph from a source location AAA to a target location ZZZ by following given directions
#
# @param inputFilePath: the input file
# @return: The number of steps to travel
#
def part1(inputFilePath: str) -> int:
   directions, map = ingestInput(inputFilePath)
   location = "AAA"
   count = 0
   idx = 0
   while True:
      count += 1
      if directions[idx] == "L":
         location = map[location][0]
      else:
         location = map[location][1]
      if location == "ZZZ":
         break
      idx += 1
      if idx == len(directions):
         idx = 0
   return count


# Calculate and return the smallest divisor of the given number
#
# @param num: the number to find the smallest divisor for
# @return: smallest divisor
#
def smallestDivisor(num: int) -> int:
   # if divisible by 2
   if (num % 2 == 0):
      return 2
   # iterate from 3 to sqrt(num)
   candidate = 3
   while (candidate * candidate <= num):
      if (num % candidate == 0):
         return candidate
      candidate += 2
   return num


# Calculate and return the number of steps that will have to be traveled through each **A to **Z cycle before all walks are on step **Z simultaneously
#
# @param inputFilePath: the input file
# @return: the number of steps that will have to be traveled through each **A to **Z cycle before all walks are on step **Z simultaneously
#
def part2(inputFilePath: str) -> int:
   directions, map = ingestInput(inputFilePath)
   locations = []
   for key in map:
      if key[2] == "A":
         locations.append(key)
   sDs = []  # smallest divisors
   lDs = 0  # largest divisors, we know from experimentation that each of the cycles share the same common largest divisor
   for location in locations:
      count = 0
      idx = 0
      while True:
         count += 1
         if directions[idx] == "L":
            location = map[location][0]
         else:
            location = map[location][1]
         if location[2] == "Z":
            break
         idx += 1
         if idx == (len(directions)):
            idx = 0
      sD = smallestDivisor(count)
      sDs.append(sD)
      lDs = count / sD
   answer = lDs
   for divisor in sDs:
      answer *= divisor
   return answer


print("Part 1 test 1:", part1("test_input_1_part_1.txt"))
print("Part 1 test 2:", part1("test_input_2_part_1.txt"))
print("Part 1 solution:", part1("input.txt"))
print("Part 2 test:", part2("test_input_part_2.txt"))
print("Part 2 solution:", part2("input.txt"))
