# https://adventofcode.com/2025/day/6


## Ingest the input and return it in the form of a list of lists.
#
# @param inputFilePath: the input file.
# @return the input in the form of a list of lists.
#
def ingestInput(inputFilePath: str) -> list:
    inputFile = open(inputFilePath, "r")
    lines = inputFile.readlines()
    inputFile.close()
    worksheet = []
    for line in lines:
        row = []
        for character in line:
            row.append(character)
        worksheet.append(row)
    return worksheet


## Compute and return the sum of the calculations described in the input.
#  For part 1 the numbers are written from left to right with the equation
#  operator at the bottom each blocks of numbers.
#
# @param worksheet: the worksheet, a list of lists of numbers and operators.
# @return The sum of all the calculations described in the worksheet.
#
def part1(worksheet: list) -> int:
    sum = 0
    numbers = []
    operators = []
    # read all the numbers and operators first.
    for row in worksheet:
        number = 0
        for character in row:
            if character == "+" or character == "*":
                operators.append(character)
            elif character.isdigit():
                number = number * 10 + int(character)
            elif number != 0:
                # if reading an empty space, the number is complete.
                numbers.append(number)
                number = 0
    # iterate through the operators and numbers and complete the calculations second.
    numbersPerOperation = int(len(numbers) / len(operators))
    for odx in range(len(operators)):
        if operators[odx] == "+":
            result = 0
            for idx in range(numbersPerOperation):
                result += numbers[odx + idx * len(operators)]
        else:
            result = 1
            for idx in range(numbersPerOperation):
                result *= numbers[odx + idx * len(operators)]
        sum += result
    return sum


## Compute and return the sum of the calculations described in the input.
#  For part 2 the numbers are written from top to bottom with the equation
#  operator at the bottom each blocks of numbers.
#
# @param worksheet: the worksheet, a list of lists of numbers and operators.
# @return The sum of all the calculations described in the worksheet.
#
def part2(worksheet: list) -> int:
    sum = 0
    numbers = []
    # read the worksheet from top to bottom and right to left to read the
    # equation operator after the numbers.
    for jdx in range(len(worksheet[0]) - 1, -1, -1):
        number = 0
        for idx in range(len(worksheet)):
            character = worksheet[idx][jdx]
            if character.isdigit():
                number = number * 10 + int(character)
            elif number != 0:
                # if reading an operator or and empty space, the number is complete.
                numbers.append(number)
                number = 0
            if character == "+":
                result = 0
                for number in numbers:
                    result += number
                sum += result
                numbers = []  # reset
            elif character == "*":
                result = 1
                for number in numbers:
                    result *= number
                sum += result
                numbers = []  # reset
    return sum


testWorksheet = ingestInput("test_input.txt")
worksheet = ingestInput("input.txt")
print("Part 1 test:", part1(testWorksheet))
print("Part 1 solution:", part1(worksheet))
print("Part 2 test:", part2(testWorksheet))
print("Part 2 solution:", part2(worksheet))
