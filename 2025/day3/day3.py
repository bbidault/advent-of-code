# https://adventofcode.com/2025/day/3


## Finds and return the largest digit and its position within a given number string.
#
# @param number: a string with numbers.
# @return The largest digit and its position.
#
def findLargestDigit(number: str) -> tuple:
    num = 0
    pos = 0
    for idx in range(len(number)):
        if int(number[idx]) > num:
            num = int(number[idx])
            pos = idx
    return (num, pos)


## Compute and return the sum of the largest n (given) digits numbers.
#
# @param inputFilePath: the input file.
# @param digits: the number of digits of the number to find.
# @return The sum of the largest n (given) digits numbers.
#
def compute(inputFilePath: str, digits: int) -> int:
    inputFile = open(inputFilePath, "r")
    lines = inputFile.readlines()
    inputFile.close()
    sum = 0
    for line in lines:
        numbers = []
        begin = 0
        # find the largest digit in a specified range for as many digits as necessary
        for idx in range(digits):
            end = len(line) - digits + idx
            subStr = line[begin:end]
            (num, pos) = findLargestDigit(subStr)
            begin += pos + 1
            numbers.append(num)
        # add the number to the total sum, the number is calculated from its digits
        # multiplied by the proper power of 10
        for idx in range(len(numbers)):
            sum += numbers[idx] * 10 ** (len(numbers) - idx - 1)
    return sum


print("Part 1 test:", compute("test_input.txt", 2))
print("Part 1 solution:", compute("input.txt", 2))
print("Part 2 test:", compute("test_input.txt", 12))
print("Part 2 solution:", compute("input.txt", 12))
