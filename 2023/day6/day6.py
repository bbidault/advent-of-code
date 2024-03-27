# https://adventofcode.com/2023/day/6

import math


##
# Solve returns the solution(s) of a quadratic equation written as a * x^2 + b * x + c = 0
#
# @param a: second degree coefficient
# @param b: first degree coefficient
# @param c: constant coefficient
# @return: the solution(s) of the equation
#
def solve(a: int, b: int, c: int) -> list:
   solutions = []
   delta = b * b - 4 * a * c
   if delta == 0:
      solutions.add(-b / (2 * a))
   elif delta > 0:
      solutions.append((-b + math.sqrt(delta)) / (2 * a))
      solutions.append((-b - math.sqrt(delta)) / (2 * a))
   # assume that the given input cannot lead to complex solutions (delta < 0)
   return solutions


##
# Computes the product of the numbers of valid solutions to win each race,
# the "solutions" are the the number of seconds to press the "speed" buton before releasing
#
# @param inputs: the race details
# @return: the product of the numbers of valid solutions to win each race
#
def compute(inputs: list) -> int:
   answer = 1
   for input in inputs:
      solutions = solve(-1, input[0], -input[1])
      ceil = 0  # the max number of seconds pressed to win
      floor = 0  # the min number of seconds pressed to win
      if max(solutions) == int(max(solutions)):
         ceil = max(solutions) - 1  # exclude case that would lead to a tie
      else:
         ceil = math.floor(max(solutions))
      if min(solutions) == int(min(solutions)):
         floor = min(solutions) + 1  # exclude case that would lead to a tie
      else:
         floor = math.ceil(min(solutions))
      answer *= ceil - floor + 1  # + 1 to include both the ceil and floor
   return answer


# directly paste the input in a set of structures for simplicity
test_input_part_1 = [(7, 9), (15, 40), (30, 200)]
input_part_1 = [(49, 356), (87, 1378), (78, 1502), (95, 1882)]
test_input_part_2 = [(71530, 940200)]
input_part_2 = [(49877895, 356137815021882)]

print("Part 1 test:", compute(test_input_part_1))
print("Part 1 solution:", compute(input_part_1))
print("Part 2 test:", compute(test_input_part_2))
print("Part 2 solution:", compute(input_part_2))
