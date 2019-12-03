"""
Advent of code day 3
"""
from enum import Enum
import os
import pathlib
from typing import Tuple, List

import numpy as np

INPUT_FILE = os.path.join(pathlib.Path(__file__).parent, 'input.txt')
# INPUT_FILE = os.path.join(pathlib.Path(__file__).parent, 'inputTest.txt')


def closestIntersection():
    """
    Finds the shortest manhatten distance of the intersections
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
    Finds the sortest full path of the intersections
    """
    wire1Path, wire2Path = readInput()

    wire1XY = createEdgeMap(wire1Path)
    wire2XY = createEdgeMap(wire2Path)

    if len(wire1XY) > len(wire2XY):
        totalSteps = findIntersectionPathLengths(wire1XY, wire2XY, wire1Path, wire2Path)
    else:
        totalSteps = findIntersectionPathLengths(wire2XY, wire1XY, wire1Path, wire2Path)

    print(f'min steps = {np.min(totalSteps)}')


class Point:
    """
    A simple point class
    """
    def __init__(self, x: int, y: int):
        """
        Constructor
        """
        self.x = x
        self.y = y

    def __eq__(self, other):
        """
        Equality operator
        """
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        """
        Less than operator
        """
        if self.x < other.x:
            return True
        elif self.x == other.x:
            if self.y < other.y:
                return True

        return False

    def __add__(self, other):
        """
        Addition operator
        """
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        subtraction operator
        """
        return Point(self.x - other.x, self.y - other.y)

    def __str__(self):
        """
        string operator
        """
        return f'Point({self.x}, {self.y})'

    def __repr__(self):
        """
        representation operator
        """
        return self.__str__()

    def manhattenDistance(self):
        """
        Finds the manhatten distance from (0,0)
        """
        return abs(self.x) + abs(self.y)


def absPoints(points: np.ndarray) -> List[Point]:
    """
    Takes the absolute value of a list of points
    """
    return [Point(abs(point.x), abs(point.y)) for point in points]


class Direction(Enum):
    """
    Directional Enum
    """
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class Edge:
    """
    Simple Class for holding an Edge
    """
    def __init__(self, direction: Direction, length: int):
        """
        Constructor
        """
        self.direction = direction
        self.length = length


def parsePathEdge(edge: str) -> Edge:
    """
    Parses the input file and forms Edge objects
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
    reads in and parses the input file
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
    Creates an List of Points of the input Edges
    """
    y = list()
    x = list()

    y.append(0)
    x.append(0)

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

    return sorted(points[1:])  # remove the origin


def findManhattenDistances(listLarge: List[Point], listSmall: List[Point]) -> List[int]:
    """
    Finds the manhatten distances of the path intersections
    """
    manhattenDistances = list()
    length = len(listSmall)
    for idx, point in enumerate(listSmall):
        print(f'idx = {idx} of {length}')
        if point in listLarge:
            manhattenDistances.append(point.manhattenDistance())

    return manhattenDistances


def findIntersectionPathLengths(listLarge: List[Point],
                                listSmall: List[Point],
                                wire1Path: List[Edge],
                                wire2Path: List[Edge]) -> List[int]:
    """
    Finds the total path length of the path intersections
    """
    intersections = list()
    length = len(listSmall)
    for idx, point in enumerate(listSmall):
        print(f'idx = {idx} of {length}')
        if point in listLarge:
            intersections.append(point)

    pathLengths = list()
    for point in intersections:
        pathLengths.append(getPathLengthToPoint(wire1Path, point) +
                           getPathLengthToPoint(wire2Path, point))

    return pathLengths


def getPathLengthToPoint(wirePath: List[Edge], point: Point):
    """
    Calculates the path length to a input point
    """
    x = 0
    y = 0
    length = 0
    for edge in wirePath:
        if edge.direction == Direction.UP:
            pointFound = False
            for step in range(edge.length):
                y += 1
                length += 1
                if x == point.x and y == point.y:
                    pointFound = True
                    break
            if pointFound:
                break
        elif edge.direction == Direction.DOWN:
            pointFound = False
            for step in range(edge.length):
                y -= 1
                length += 1
                if x == point.x and y == point.y:
                    pointFound = True
                    break
            if pointFound:
                break
        elif edge.direction == Direction.RIGHT:
            pointFound = False
            for step in range(edge.length):
                x += 1
                length += 1
                if x == point.x and y == point.y:
                    pointFound = True
                    break
            if pointFound:
                break
        elif edge.direction == Direction.LEFT:
            pointFound = False
            for step in range(edge.length):
                x -= 1
                length += 1
                if x == point.x and y == point.y:
                    pointFound = True
                    break
            if pointFound:
                break

    return length


if __name__ == '__main__':
    # closestIntersection()
    shortestIntersetion()
