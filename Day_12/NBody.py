"""
The N-Body problem
"""
from copy import deepcopy
from dataclasses import dataclass
import re
import os
import pathlib
from typing import List

INPUT_FILE = os.path.join(pathlib.Path(__file__).parent, 'input.txt')


@dataclass()
class Vec3:
    """
    Simple Vec3 class
    """
    x: int = 0
    y: int = 0
    z: int = 0

    def __eq__(self, other):
        """
        Equality operator
        """
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __iadd__(self, other):
        """
        addition assignment operator
        """
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def energy(self) -> int:
        """
        Returns the potential energy of the position vector, or
        the kinetic energy of the velocity vector
        """
        return abs(self.x) + abs(self.y) + abs(self.z)


def calcTotalEnergy(numSteps: int, verboseOutput: bool = False):
    """
    Calculates the total energy of the moons after input steps
    """
    moonCoordinates = readInput()
    moonVelocities = [Vec3() for _ in range(len(moonCoordinates))]

    if verboseOutput:
        print(f'After 0 steps')
        for idx, moonCoordinate in enumerate(moonCoordinates):
            print(f'pos={moonCoordinate},\tvel={moonVelocities[idx]}')

    for step in range(numSteps):
        for idx1 in range(len(moonCoordinates) - 1):
            for idx2 in range(idx1 + 1, len(moonCoordinates)):
                if moonCoordinates[idx1].x < moonCoordinates[idx2].x:
                    moonVelocities[idx1].x += 1
                    moonVelocities[idx2].x -= 1
                elif moonCoordinates[idx1].x > moonCoordinates[idx2].x:
                    moonVelocities[idx1].x -= 1
                    moonVelocities[idx2].x += 1

                if moonCoordinates[idx1].y < moonCoordinates[idx2].y:
                    moonVelocities[idx1].y += 1
                    moonVelocities[idx2].y -= 1
                elif moonCoordinates[idx1].y > moonCoordinates[idx2].y:
                    moonVelocities[idx1].y -= 1
                    moonVelocities[idx2].y += 1

                if moonCoordinates[idx1].z < moonCoordinates[idx2].z:
                    moonVelocities[idx1].z += 1
                    moonVelocities[idx2].z -= 1
                elif moonCoordinates[idx1].z > moonCoordinates[idx2].z:
                    moonVelocities[idx1].z -= 1
                    moonVelocities[idx2].z += 1

        for idx, moonCoordinate in enumerate(moonCoordinates):
            moonCoordinate += moonVelocities[idx]

        if verboseOutput:
            print(f'After {step + 1} steps')
            for idx, moonCoordinate in enumerate(moonCoordinates):
                print(f'pos={moonCoordinate},\tvel={moonVelocities[idx]}')

    totalEnergy = 0
    for idx, moonCoordinate in enumerate(moonCoordinates):
        totalEnergy += moonCoordinate.energy() * moonVelocities[idx].energy()

    print(f'Total Energy = {totalEnergy}')


def calcStepsToHistory(verboseOutput: bool = False):
    """
    Calculates the number of steps before the moons return to a position
    they have already been in before
    """
    moonCoordinates = readInput()
    moonVelocities = [Vec3() for _ in range(len(moonCoordinates))]

    if verboseOutput:
        print(f'After 0 steps')
        for idx, moonCoordinate in enumerate(moonCoordinates):
            print(f'pos={moonCoordinate},\tvel={moonVelocities[idx]}')

    positionHistory = list()
    positionHistory.append(deepcopy(moonCoordinates))

    velocityHistory = list()
    velocityHistory.append(deepcopy(moonVelocities))

    numSteps = 1
    while True:
        for idx1 in range(len(moonCoordinates) - 1):
            for idx2 in range(idx1 + 1, len(moonCoordinates)):
                if moonCoordinates[idx1].x < moonCoordinates[idx2].x:
                    moonVelocities[idx1].x += 1
                    moonVelocities[idx2].x -= 1
                elif moonCoordinates[idx1].x > moonCoordinates[idx2].x:
                    moonVelocities[idx1].x -= 1
                    moonVelocities[idx2].x += 1

                if moonCoordinates[idx1].y < moonCoordinates[idx2].y:
                    moonVelocities[idx1].y += 1
                    moonVelocities[idx2].y -= 1
                elif moonCoordinates[idx1].y > moonCoordinates[idx2].y:
                    moonVelocities[idx1].y -= 1
                    moonVelocities[idx2].y += 1

                if moonCoordinates[idx1].z < moonCoordinates[idx2].z:
                    moonVelocities[idx1].z += 1
                    moonVelocities[idx2].z -= 1
                elif moonCoordinates[idx1].z > moonCoordinates[idx2].z:
                    moonVelocities[idx1].z -= 1
                    moonVelocities[idx2].z += 1

        for idx, moonCoordinate in enumerate(moonCoordinates):
            moonCoordinate += moonVelocities[idx]

        if verboseOutput:
            print(f'After {numSteps + 1} steps')
            for idx, moonCoordinate in enumerate(moonCoordinates):
                print(f'pos={moonCoordinate},\tvel={moonVelocities[idx]}')

        if moonCoordinates in positionHistory:
            idx = positionHistory.index(moonCoordinates)
            if moonVelocities == velocityHistory[idx]:
                break

        positionHistory.append(deepcopy(moonCoordinates))
        velocityHistory.append(deepcopy(moonVelocities))
        numSteps += 1

    print(f'Number of steps to history = {numSteps}')


def readInput() -> List[Vec3]:
    """
    Reads the input file
    """
    tokenizer = re.compile('<x=(.+), y=(.+), z=(.+)>')

    coordinates = list()
    with open(INPUT_FILE) as f:
        line = f.readline()
        while line != '':
            x, y, z = tokenizer.findall(line)[0]
            coordinates.append(Vec3(x=int(x), y=int(y), z=int(z)))
            line = f.readline()

    return coordinates


if __name__ == '__main__':
    # calcTotalEnergy(numSteps=1000, verboseOutput=True)
    calcStepsToHistory(verboseOutput=False)
