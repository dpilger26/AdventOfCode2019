"""
Advent of code day 3
"""
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

    manhattenDistances = list()
    if len(wire1XY) > len(wire2XY):
        length = len(wire2XY)
        for idx, xyPair in enumerate(wire2XY):
            print(f'idx = {idx} of {length}')
            if xyPair in wire1XY:
                manhattenDistances.append(np.sum(np.abs(xyPair)))
    else:
        length = len(wire1XY)
        for idx, xyPair in enumerate(wire1XY):
            print(f'idx = {idx} of {length}')
            if xyPair in wire2XY:
                manhattenDistances.append(np.sum(np.abs(xyPair)))

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


def createEdgeMap(path: List[str]) -> List[Tuple[int, int]]:
    """

    :param path:
    :return:
    """
    y = list()
    x = list()
    for edge in path:
        direction, length = parsePathEdge(edge=edge)

        if direction == 'U':
            y.append(length)
        elif direction == 'D':
            y.append(-length)
        elif direction == 'R':
            x.append(length)
        elif direction == 'L':
            x.append(-length)
        else:
            raise RuntimeError(f'Unknown direction {direction}')

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
        direction, length = parsePathEdge(edge=edge)

        if direction == 'U':
            edgeMap[row:row + length, col] = 1
            row += length
        elif direction == 'D':
            edgeMap[row - length:row, col] = 1
            row -= length
        elif direction == 'R':
            edgeMap[row, col:col + length] = 1
            col += length
        elif direction == 'L':
            edgeMap[row, col - length:col] = 1
            col -= length

    rows, cols = np.nonzero(edgeMap)
    rows -= rowStart
    cols -= colStart

    return np.vstack([rows, cols]).T.tolist()


def parsePathEdge(edge: str) -> Tuple[str, int]:
    """

    :param edge:
    :return:
    """
    return edge[0], int(edge[1:])


def readInput() -> Tuple[List[str], List[str]]:
    """

    :return:
    """
    with open(INPUT_FILE) as f:
        wire1 = f.readline().strip()
        wire1 = wire1.split(',')

        wire2 = f.readline().strip()
        wire2 = wire2.split(',')

    return wire1, wire2


if __name__ == '__main__':
    # closestIntersection()
    shortestIntersetion()
