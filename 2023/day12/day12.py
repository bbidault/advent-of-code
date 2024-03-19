
# def match(candidate, nums):
#     idx = -1
#     result = []
#     prev = candidate[0]
#     if candidate[0] == "#":
#         result.append(1)
#         idx = 0
#     for i in range(1,len(candidate)):
#         if candidate[i-1] == "#" and candidate[i] == "#":
#             result[idx] += 1
#         elif candidate[i-1] == "." and candidate[i] == "#":
#             result.append(1)
#             idx += 1
#     return result == nums

# # print("#.##.##.#.#.....#### " + str(match("#.##.##.#.#.....####", [1,2,2,1,1,4])))
# # print("#.##.##.#.#.#### " + str(match("#.##.##.#.#.####", [1,2,2,1,1,4])))
# # print(".#..##.##.#.#....####. " + str(match(".#..##.##.#.#....####.", [1,2,2,1,1,4])))
# # print(".#..##.##.#.#....###. " + str(match(".#..##.##.#.#....###.", [1,2,2,1,1,4])))
# # print(".#..##.##.#....###. " + str(match(".#..##.##.#.#....###.", [1,2,2,1,1,4])))

import functools


@functools.lru_cache(maxsize=None)
def findpatterns(pattern, size, splits):
   count = 0
   patternMaxStart = size - sum(splits[1:]) - len(splits[1:]) - splits[0] + 1
   for i in range(patternMaxStart):
      if all(pattern[j] in "#?" for j in range(i, i + splits[0])):
         if len(splits) == 1:
            if all(pattern[j] in ".?" for j in range(i + splits[0], len(pattern))):
               count += 1
         elif pattern[i + splits[0]] in '.?':
            count += findpatterns(pattern[i + splits[0] + 1:], len(pattern[i + splits[0] + 1:]), splits[1:])
      if pattern[i] not in '.?':
         break
   return count


inputFile = open("input.txt", "r")
Lines = inputFile.readlines()
solution = 0
for line in Lines:
   content = line.split(" ")
   chars = content[0]
   splits = tuple(map(int, content[1].split(','))) * 5
   pattern = chars + "?" + chars + "?" + chars + "?" + chars + "?" + chars
#    splits = tuple(map(int, content[1].split(',')))
#    pattern = chars
   solution += findpatterns(pattern, len(pattern), splits)
print(solution)
inputFile.close()
