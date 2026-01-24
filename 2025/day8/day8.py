# https://adventofcode.com/2025/day/8


## A juncton box.
#
class JunctionBox:

    ## JunctionBox constructor.
    #
    # @param self: the junction box.
    # @param aX: the x coordinate of the box.
    # @param aY: the y coordinate of the box.
    # @param aZ: the z coordinate of the box.
    #
    def __init__(self, aX: int, aY: int, aZ: int):
        self.x = aX
        self.y = aY
        self.z = aZ
        self.connections = []  # the list of boxes connected to this box.
        # whether this box has been visited in the circuit traversal or not.
        self.visited = False

    ## Calculate the distance between two given junction boxes.
    #
    # @param self: the junction box of interest.
    # @param otherBox: an other junction box.
    # @return the distance between the two given junction boxes.
    #
    def dist(self, otherBox) -> float:
        return (
            (self.x - otherBox.x) ** 2
            + (self.y - otherBox.y) ** 2
            + (self.z - otherBox.z) ** 2
        ) ** 0.5


## Visit a circuit and return the number of boxes in it.
#
# @param boxKey: the key of a specific box to visit in the circuit.
# @param boxes: a dictionary of boxes.
# @return the number of boxes in the circuit.
#
def visitCircuit(boxKey: int, boxes: dict) -> int:
    circuitSize = 0
    if False == boxes[boxKey].visited:
        circuitSize += 1
        boxes[boxKey].visited = True
        for key in boxes[boxKey].connections:
            circuitSize += visitCircuit(key, boxes)
    return circuitSize


## Compute the product of the size of the 3 largest circuits after connecting
#  the closest 10/1000 junctions boxes.
#
# @param inputFilePath: the input file
# @param test: whether this is a test or the real thing.
# @return the product of the size of the 3 largest circuits.
#
def compute(inputFilePath: str, test: bool) -> int:
    inputFile = open(inputFilePath, "r")
    lines = inputFile.readlines()
    inputFile.close()

    # read all the junction boxes.
    boxes = dict()
    idx = 0
    for line in lines:
        coor = [int(x) for x in line.split(",")]
        boxes[idx] = JunctionBox(coor[0], coor[1], coor[2])
        idx += 1

    # calculate the distances between each paires of junction boxes.
    distances = dict()
    for idx in range(len(boxes)):
        for jdx in range(idx + 1, len(boxes)):
            distances[(idx, jdx)] = boxes[idx].dist(boxes[jdx])
    # sort the paires of junction boxes by the distances seperating them.
    sortedDist = {
        key: value for key, value in sorted(distances.items(), key=lambda item: item[1])
    }

    # connect the junction boxes by proximity
    count = 0
    for key in sortedDist.keys():
        boxes[key[0]].connections.append(key[1])
        boxes[key[1]].connections.append(key[0])
        # 10 connections for the test, 1000 for the real thing.
        count += 1
        if count == 10 and test:
            break
        elif count == 1000:
            break

    # visit and measure the size of all the circuits.
    circuits = []
    for key, value in boxes.items():
        if False == value.visited:
            circuitSize = visitCircuit(key, boxes)
            circuits.append(circuitSize)

    # sort the circuits by size.
    circuits = sorted(circuits)

    # get the product of the 3 largest circuits size.
    part1 = circuits[-1] * circuits[-2] * circuits[-3]

    return part1


print("Part 1 test:", compute("test_input.txt", True))
print("Part 1 solution:", compute("input.txt", False))
