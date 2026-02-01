# https://adventofcode.com/2025/day/11

from functools import lru_cache


## Use depth first search to count the number of paths from the given root to the "out" node.
#
# @param inputFilePath: the input file
# @param root: the root node.
# @param dacfft: whether we should ignore the dac and fft node requirement or not.
# @return the number of paths from root to "out".
#
def compute(inputFilePath: str, root: str, dacfft: bool) -> tuple:
    inputFile = open(inputFilePath, "r")
    lines = inputFile.readlines()

    nodes = {}
    for line in lines:
        source, targets = line.split(": ")
        nodes[source] = targets.split()

    ## Depth First Search.
    #
    # @param node: the current node.
    # @param dac: whether a dac node as been traversed or not.
    # @param fft: whether a fft node as been traversed or not.
    # @return the number of path from node to "out".
    #
    @lru_cache(maxsize=None)
    def dfs(node: str, dac: bool, fft: bool) -> int:
        if node == "out" and dac and fft:
            return 1
        count = 0
        for child in nodes.get(node, []):
            count += dfs(child, (dac or node == "dac"), (fft or node == "fft"))
        return count

    return dfs(root, dacfft, dacfft)


# for part 1, the root node is "you" and we can ignore dac and fft nodes.
print("Part 1 test:", compute("test_input_1.txt", "you", True))
print("Part 1 solution:", compute("input.txt", "you", True))

# for part 2, the root node is "svr" and we should travel through a dac and a fft nodes.
print("Part 2 test:", compute("test_input_2.txt", "svr", False))
print("Part 2 solution:", compute("input.txt", "svr", False))
