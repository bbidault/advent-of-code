# https://adventofcode.com/2025/day/9

import shapely


## Calculate the area of the rectangle formed by two given tiles.
#
# @param tile: a tile.
# @param otherTile: an other tile.
# @return the area of the rectangle formed by two given tiles.
#
def area(tile: tuple, otherTile: tuple) -> float:
    return (max(tile[0], otherTile[0]) - min(tile[0], otherTile[0]) + 1) * (
        max(tile[1], otherTile[1]) - min(tile[1], otherTile[1]) + 1
    )


## Return a shapely box of the rectangle formed by two given tiles.
#
# @param tile: a tile.
# @param otherTile: an other tile.
# @return a shapely box of the rectangle formed by two given tiles.
#
def rect(tile: tuple, otherTile: tuple) -> shapely.box:
    return shapely.box(
        min(tile[0], otherTile[0]),  # x min
        min(tile[1], otherTile[1]),  # y min
        max(tile[0], otherTile[0]),  # x max
        max(tile[1], otherTile[1]),  # y max
    )


## Compute and returns the area of the largest rectangle formed by any two red
#  tiles and the area of the largest rectangle contained within the shape
#  drawn by the consecutive red tiles.
#
# @param inputFilePath: the input file
# @return the area of the largest rectangle formed by any two red tiles and
#         the area of the largest rectangle contained within the shape drawn
#         by the consecutive red tiles.
#
def compute(inputFilePath: str) -> tuple:
    inputFile = open(inputFilePath, "r")
    lines = inputFile.readlines()
    inputFile.close()

    # read all the tiles.
    tiles = []
    for line in lines:
        x, y = [int(coor) for coor in line.split(",")]
        tiles.append((x, y))

    # The shape drawn by the consecutive red tiles.
    polygon = shapely.Polygon(tiles)

    # calculate the area of the rectangle formed by each paires of tiles.
    part1 = 0
    part2 = 0
    for idx in range(len(tiles)):
        for jdx in range(idx + 1, len(tiles)):
            rArea = area(tiles[idx], tiles[jdx])
            rectangle = rect(tiles[idx], tiles[jdx])
            if part1 < rArea:
                part1 = rArea
            if part2 < rArea and polygon.contains(rectangle):
                part2 = rArea

    return (part1, part2)


part1Test, part2Test = compute("test_input.txt")
part1, part2 = compute("input.txt")
print("Part 1 test:", part1Test)
print("Part 1 solution:", part1)
print("Part 2 test:", part2Test)
print("Part 2 solution:", part2)
