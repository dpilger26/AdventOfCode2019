"""
The N-Body problem
"""
from copy import deepcopy
import re
import os
import pathlib
from typing import List

INPUT_FILE = os.path.join(pathlib.Path(__file__).parent, 'input.txt')


class Vec3:
    """
    Simple Vec3 class
    """
    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        """
        String method
        """
        return f'Vec3(x={self.x}, y={self.y}, z={self.z})'

    def __repr__(self):
        """
        repr method
        """
        return self.__str__()

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

        return self

    def energy(self) -> int:
        """
        Returns the potential energy of the position vector, or
        the kinetic energy of the velocity vector
        """
        return abs(self.x) + abs(self.y) + abs(self.z)

    def right(self) -> None:
        """
        incraments (+x)
        """
        self.x += 1

    def left(self) -> None:
        """
        incraments (-x)
        """
        self.x -= 1

    def up(self) -> None:
        """
        incraments (+y)
        """
        self.y += 1

    def down(self) -> None:
        """
        incraments (-y)
        """
        self.y -= 1

    def forward(self) -> None:
        """
        incraments (+z)
        """
        self.z += 1

    def back(self) -> None:
        """
        incraments (-z)
        """
        self.z -= 1


class Body:
    """
    Simple body class
    """
    def __init__(self, position: Vec3 = Vec3(), velocity: Vec3 = Vec3()):
        self.position = position
        self.velocity = velocity

    def __str__(self):
        """
        String method
        """
        return f'Body(position={self.position}, velocity={self.velocity})'

    def __repr__(self):
        """
        repr method
        """
        return self.__str__()

    def potentialEnergy(self) -> int:
        """
        The potential energy of the body
        """
        return self.position.energy()

    def kineticEnergy(self) -> int:
        """
        The kinetic energy of the body
        """
        return self.velocity.energy()

    def totalEnergy(self) -> int:
        """
        The total energy of the body
        """
        return self.potentialEnergy() * self.kineticEnergy()

    def updateVelocity(self, other: 'Body') -> None:
        """
        Updates the velocity based of the simple gravity model
        """
        if self.position.x < other.position.x:
            print('updating +x')
            self.velocity.right()
            other.velocity.left()
        elif self.position.x > other.position.x:
            print('updating -x')
            self.velocity.left()
            other.velocity.right()

        if self.position.y < other.position.y:
            print('updating +y')
            self.velocity.up()
            other.velocity.down()
        elif self.position.y > other.position.y:
            print('updating -y')
            self.velocity.down()
            other.velocity.up()

        if self.position.z < other.position.z:
            print('updating +z')
            self.velocity.forward()
            other.velocity.back()
        elif self.position.z > other.position.z:
            print('updating -z')
            self.velocity.back()
            other.velocity.forward()

        print(f'\t\t{self}')
        print(f'\t\t{other}')

    def updatePosition(self) -> None:
        """
        Updates the position of the body
        """
        self.position += self.velocity


def calcTotalEnergy(numSteps: int, verboseOutput: bool = False) -> None:
    """
    Calculates the total energy of the moons after input steps
    """
    moons = readInput()

    if verboseOutput:
        print(f'After 0 steps')
        for moon in moons:
            print(moon)

    for step in range(numSteps):
        for idx1 in range(len(moons) - 1):
            for idx2 in range(idx1 + 1, len(moons)):
                moons[idx1].updateVelocity(moons[idx2])
                print(f'\t{moons[idx1]}')
                print(f'\t{moons[idx2]}')

        for moon in moons:
            print(moon)
            moon.updatePosition()
            print(moon)

        if verboseOutput:
            print(f'After {step + 1} steps')
            for moon in moons:
                print(moon)

    totalEnergy = 0
    for moon in moons:
        totalEnergy += moon.totalEnergy()

    print(f'Total Energy = {totalEnergy}')


# def calcStepsToHistory(verboseOutput: bool = False) -> None:
#     """
#     Calculates the number of steps before the moons return to a position
#     they have already been in before
#     """
#     moonCoordinates = readInput()
#     moonVelocities = [Vec3() for _ in range(len(moonCoordinates))]
#
#     if verboseOutput:
#         print(f'After 0 steps')
#         for idx, moonCoordinate in enumerate(moonCoordinates):
#             print(f'pos={moonCoordinate},\tvel={moonVelocities[idx]}')
#
#     positionHistory = list()
#     positionHistory.append(deepcopy(moonCoordinates))
#
#     velocityHistory = list()
#     velocityHistory.append(deepcopy(moonVelocities))
#
#     numSteps = 1
#     while True:
#         print(f'Step {numSteps}')
#         for idx1 in range(len(moonCoordinates) - 1):
#             for idx2 in range(idx1 + 1, len(moonCoordinates)):
#                 if moonCoordinates[idx1].x < moonCoordinates[idx2].x:
#                     moonVelocities[idx1].x += 1
#                     moonVelocities[idx2].x -= 1
#                 elif moonCoordinates[idx1].x > moonCoordinates[idx2].x:
#                     moonVelocities[idx1].x -= 1
#                     moonVelocities[idx2].x += 1
#
#                 if moonCoordinates[idx1].y < moonCoordinates[idx2].y:
#                     moonVelocities[idx1].y += 1
#                     moonVelocities[idx2].y -= 1
#                 elif moonCoordinates[idx1].y > moonCoordinates[idx2].y:
#                     moonVelocities[idx1].y -= 1
#                     moonVelocities[idx2].y += 1
#
#                 if moonCoordinates[idx1].z < moonCoordinates[idx2].z:
#                     moonVelocities[idx1].z += 1
#                     moonVelocities[idx2].z -= 1
#                 elif moonCoordinates[idx1].z > moonCoordinates[idx2].z:
#                     moonVelocities[idx1].z -= 1
#                     moonVelocities[idx2].z += 1
#
#         for idx, moonCoordinate in enumerate(moonCoordinates):
#             moonCoordinate += moonVelocities[idx]
#
#         if verboseOutput:
#             print(f'After {numSteps + 1} steps')
#             for idx, moonCoordinate in enumerate(moonCoordinates):
#                 print(f'pos={moonCoordinate},\tvel={moonVelocities[idx]}')
#
#         if moonCoordinates in positionHistory:
#             idx = positionHistory.index(moonCoordinates)
#             if moonVelocities == velocityHistory[idx]:
#                 break
#
#         positionHistory.append(deepcopy(moonCoordinates))
#         velocityHistory.append(deepcopy(moonVelocities))
#         numSteps += 1
#
#     print(f'Number of steps to history = {numSteps}')


def readInput() -> List[Body]:
    """
    Reads the input file
    """
    tokenizer = re.compile('<x=(.+), y=(.+), z=(.+)>')

    bodies = list()
    with open(INPUT_FILE) as f:
        line = f.readline()
        while line != '':
            x, y, z = tokenizer.findall(line)[0]
            bodies.append(Body(position=Vec3(x=int(x), y=int(y), z=int(z))))
            line = f.readline()

    return bodies


if __name__ == '__main__':
    calcTotalEnergy(numSteps=1000, verboseOutput=True)
    # calcStepsToHistory(verboseOutput=False)
