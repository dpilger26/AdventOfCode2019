"""
Advent of code day 3
"""
from enum import Enum
import os
import pathlib
from typing import Tuple, List

import numpy as np

INPUT_FILE = os.path.join(pathlib.Path(__file__).parent, 'input.txt')


def closestIntersection():
    """

    :return:
    """
    wire1Path, wire2Path = readInput()

    wire1XY = createEdgeMap(wire1Path)
    wire2XY = createEdgeMap(wire2Path)

    if len(wire1XY) > len(wire2XY):
        manhattenDistances = findManhattenDistances(wire1XY, wire2XY)
    else:
        manhattenDistances = findManhattenDistances(wire2XY, wire1XY)

    print(f'min distance = {np.min(manhattenDistances)}')


def shortestIntersetion():
    """

    :return:
    """
    wire1Path, wire2Path = readInput()

    wire1XY = createEdgeMap(wire1Path)
    wire2XY = createEdgeMap(wire2Path)

    if len(wire1XY) > len(wire2XY):
        print('in if')
        length = len(wire2XY)
        theIdx = 0
        thePair = None
        for idx, xyPair in enumerate(wire2XY):
            print(f'idx = {idx} of {length}')
            if xyPair in wire1XY:
                theIdx = idx
                thePair = xyPair
                break

        steps2 = np.sum(np.abs(np.diff(wire2XY[:theIdx], axis=0)), axis=0).sum()

        for idx, xyPair in enumerate(wire1XY):
            if xyPair == thePair:
                theIdx = idx

        steps1 = np.sum(np.abs(np.diff(wire1XY[:theIdx], axis=0)), axis=0).sum()
        totalSteps = steps1 + steps2
    else:
        print('in else')
        length = len(wire1XY)
        theIdx = 0
        thePair = None
        for idx, xyPair in enumerate(wire1XY):
            print(f'idx = {idx} of {length}')
            if xyPair in wire2XY:
                theIdx = idx
                thePair = xyPair
                break
        steps1 = np.sum(np.abs(np.diff(wire1XY[:theIdx], axis=0)), axis=0).sum()

        for idx, xyPair in enumerate(wire2XY):
            if xyPair == thePair:
                theIdx = idx

        steps2 = np.sum(np.abs(np.diff(wire2XY[:theIdx], axis=0)), axis=0).sum()
        totalSteps = steps1 + steps2

    print(f'min steps = {totalSteps}')


class Point:
    """
    blah
    """
    def __init__(self, x: int, y: int):
        """
        blah
        """
        self.x = x
        self.y = y

    def __eq__(self, other):
        """
        blah
        """
        return self.x == other.x and self.y == other.y

    def manhattenDistance(self):
        """
        blah
        """
        return abs(self.x) + abs(self.y)


class Direction(Enum):
    """
    blah
    """
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class Edge:
    """
    blah
    """
    def __init__(self, direction: Direction, length: int):
        self.direction = direction
        self.length = length


def parsePathEdge(edge: str) -> Edge:
    """

    :param edge:
    :return:
    """
    if edge[0] == 'R':
        direction = Direction.RIGHT
    elif edge[0] == 'L':
        direction = Direction.LEFT
    elif edge[0] == 'U':
        direction = Direction.UP
    elif edge[0] == 'D':
        direction = Direction.DOWN
    else:
        raise RuntimeError(f'Unknown direction {edge[0]}')

    return Edge(direction, int(edge[1:]))


def readInput() -> Tuple[List[Edge], List[Edge]]:
    """

    :return:
    """
    with open(INPUT_FILE) as f:
        wire1Path = f.readline().strip()
        wire1Path = wire1Path.split(',')

        wire2Path = f.readline().strip()
        wire2Path = wire2Path.split(',')

    wire1Edges = [parsePathEdge(pathEdge) for pathEdge in wire1Path]
    wire2Edges = [parsePathEdge(pathEdge) for pathEdge in wire2Path]

    return wire1Edges, wire2Edges


def createEdgeMap(path: List[Edge]) -> List[Point]:
    """

    :param path:
    :return:
    """
    y = list()
    x = list()
    for edge in path:
        if edge.direction == Direction.UP:
            y.append(edge.length)
        elif edge.direction == Direction.DOWN:
            y.append(-edge.length)
        elif edge.direction == Direction.RIGHT:
            x.append(edge.length)
        elif edge.direction == Direction.LEFT:
            x.append(-edge.length)

    cumX = np.cumsum(x)
    cumY = np.cumsum(y)

    numRows = np.ptp(cumY) + 1
    numCols = np.ptp(cumX) + 1

    edgeMap = np.zeros([numRows, numCols])

    rowStart = np.abs(np.min(cumY)).item()
    colStart = np.abs(np.min(cumX)).item()

    row = rowStart
    col = colStart

    for edge in path:
        if edge.direction == Direction.UP:
            edgeMap[row:row + edge.length, col] = 1
            row += edge.length
        elif edge.direction == Direction.DOWN:
            edgeMap[row - edge.length:row, col] = 1
            row -= edge.length
        elif edge.direction == Direction.RIGHT:
            edgeMap[row, col:col + edge.length] = 1
            col += edge.length
        elif edge.direction == Direction.LEFT:
            edgeMap[row, col - edge.length:col] = 1
            col -= edge.length

    rows, cols = np.nonzero(edgeMap)
    rows -= rowStart
    cols -= colStart

    points = list()
    for idx in range(len(rows)):
        points.append(Point(cols[idx], rows[idx]))

    return points


def findManhattenDistances(listLarge: List[Point], listSmall: List[Point]) -> List[int]:
    """
    blah
    """
    manhattenDistances = list()
    length = len(listSmall)
    for idx, point in enumerate(listSmall):
        print(f'idx = {idx} of {length}')
        if point in listLarge:
            manhattenDistances.append(point.manhattenDistance())

    return manhattenDistances


if __name__ == '__main__':
    closestIntersection()
    # shortestIntersetion()
