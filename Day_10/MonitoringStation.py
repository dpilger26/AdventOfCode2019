"""
blah
"""
from dataclasses import dataclass
import os
import pathlib
from typing import List

import numpy as np

INPUT_FILE = os.path.join(pathlib.Path(__file__).parent, 'input.txt')


@dataclass
class Astroid:
    """
    A simple astroid class
    """
    x: int
    y: int

    def __eq__(self, other):
        """
        Equality operator
        """
        return self.x == other.x and self.y == other.y

    def angle(self, other: 'Astroid') -> float:
        """
        Returns the angle between two astroids
        """
        x = other.x - self.x
        y = other.y - self.y
        return np.arctan2(y, x)

    def angleClockwiseFromTop(self, other: 'Astroid') -> float:
        """
        Returns the angle clock wise from the top
        """
        x = other.x - self.x
        y = other.y - self.y
        angle = np.arctan2(x, y)
        if angle < 0:
            angle += 2 * np.pi

        return angle

    def distance(self, other: 'Astroid') -> float:
        """
        Returns the distance
        """
        return np.hypot(other.x - self.x, other.y - self.y)

    def encode(self):
        """
        encodes the coordinate
        """
        return self.x * 100 + self.y


def findBestAstroid(verboseOutput: bool = False) -> Astroid:
    """
    Finds the number of other astroids the best astroid can see
    """
    astroids = readInput()

    if verboseOutput:
        print(f'Number of Astroids = {len(astroids)}')

    maxAstroids = 0
    bestAstroid = None
    for idx, astroid in enumerate(astroids):
        angles = list()
        for astroid2 in astroids:
            if astroid2 is astroid:
                continue
            angles.append(astroid.angle(astroid2))

        numVisibleAstroids = np.unique(angles).size
        if verboseOutput:
            print(f'Astroid {idx} numVisibleAstroids = {numVisibleAstroids}')

        if numVisibleAstroids > maxAstroids:
            maxAstroids = numVisibleAstroids
            bestAstroid = astroid

    print(f'Max number of astroids detected = {maxAstroids}')

    return bestAstroid


def vaporizeAstroids(verboseOutput: bool = False) -> None:
    """
    Vaporizes the astroids
    """
    astroids = readInput()

    bestAstroid = findBestAstroid(verboseOutput=False)

    if verboseOutput:
        print(f'Best Astroid = {bestAstroid}')

    # remove the best astroid from the astroids list
    removeIdx = None
    for idx, astroid in enumerate(astroids):
        if astroid == bestAstroid:
            removeIdx = idx

    del(astroids[removeIdx])

    angles = list()
    for astroid in astroids:
        angles.append(bestAstroid.angleClockwiseFromTop(astroid))

    angles = np.sort(np.unique(angles))
    lastAngle = angles[199]
    print(f'lastAngle = {np.degrees(lastAngle)}')

    astroidIdx = list()
    distances = list()
    for idx, astroid in enumerate(astroids):
        if bestAstroid.angleClockwiseFromTop(astroid) == lastAngle:
            distances.append(bestAstroid.distance(astroid))
            astroidIdx.append(idx)

    print(distances)
    sortedDistancesIdx = np.argsort(distances)
    print(sortedDistancesIdx)
    print(astroids[astroidIdx[sortedDistancesIdx[0]]])

    print(f'200th astroid = {astroids[astroidIdx[sortedDistancesIdx[0]]].encode()}')


def readInput() -> List[Astroid]:
    """
    Reads the input file
    """
    astroidMap = list()
    with open(INPUT_FILE) as f:
        line = f.readline().strip()
        while line != '':
            astroidMap.append([True if value == '#' else False for value in list(line)])
            line = f.readline().strip()

    astroidMap = np.array(astroidMap)
    astroidRows, astroidCols = np.nonzero(astroidMap)

    astroids = list()
    for i in range(len(astroidRows)):
        astroids.append(Astroid(x=astroidCols[i], y=-astroidRows[i]))

    return astroids


if __name__ == '__main__':
    # findBestAstroid(verboseOutput=False)
    vaporizeAstroids(verboseOutput=True)
