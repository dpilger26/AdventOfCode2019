"""
The N-Body problem
"""
import copy
import re
import os
import pathlib
from typing import List

import numpy as np

INPUT_FILE = os.path.join(pathlib.Path(__file__).parent, 'input.txt')


class Vec3:
    """
    Simple Vec3 class
    """
    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        """
        Constructor
        """
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

    def __eq__(self, other: 'Vec3'):
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
    def __init__(self, position: Vec3, velocity: Vec3):
        """
        Constructor
        """
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

    def __eq__(self, other: 'Body'):
        """
        Equality operator
        """
        return self.position == other.position and self.velocity == other.velocity

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

    def updatePosition(self) -> 'Body':
        """
        Updates the position of the body
        """
        self.position += self.velocity

        return self


class NBody:
    """
    Simple Nbody class
    """
    def __init__(self):
        """
        Constructor
        """
        self.bodies = list()
        self.current = 0

    def __getitem__(self, index):
        """
        item at index
        """
        return self.bodies[index]

    def __len__(self):
        """
        len operator
        """
        return self.size()

    def __iter__(self):
        """
        iter
        """
        return self

    def __next__(self):
        """
        next
        """
        self.current += 1
        if self.current < self.size():
            return self.bodies[self.current]
        raise StopIteration

    def __str__(self):
        """
        String method
        """
        string = ''
        for body in self.bodies:
            string += f'{body}\n'

        return string

    def __repr__(self):
        """
        repr method
        """
        return self.__str__()

    def addBody(self, body: Body) -> None:
        """
        Adds a body to the system
        """
        self.bodies.append(body)

    def size(self) -> int:
        """
        size
        """
        return len(self.bodies)

    def updateVelocity(self, index1, index2) -> None:
        """
        Updates the velocity based of the simple gravity model
        """
        if self.bodies[index1].position.x < self.bodies[index2].position.x:
            self.bodies[index1].velocity.right()
            self.bodies[index2].velocity.left()
        elif self.bodies[index1].position.x > self.bodies[index2].position.x:
            self.bodies[index1].velocity.left()
            self.bodies[index2].velocity.right()

        if self.bodies[index1].position.y < self.bodies[index2].position.y:
            self.bodies[index1].velocity.up()
            self.bodies[index2].velocity.down()
        elif self.bodies[index1].position.y > self.bodies[index2].position.y:
            self.bodies[index1].velocity.down()
            self.bodies[index2].velocity.up()

        if self.bodies[index1].position.z < self.bodies[index2].position.z:
            self.bodies[index1].velocity.forward()
            self.bodies[index2].velocity.back()
        elif self.bodies[index1].position.z > self.bodies[index2].position.z:
            self.bodies[index1].velocity.back()
            self.bodies[index2].velocity.forward()

    def updateVelocities(self) -> None:
        """
        Updates all of the velocities
        """
        for idx1 in range(self.size() - 1):
            for idx2 in range(idx1 + 1, self.size()):
                self.updateVelocity(idx1, idx2)

    def updatePositions(self) -> None:
        """
        Updates all of the positions
        """
        for idx in range(self.size()):
            self.bodies[idx].updatePosition()

    def update(self):
        """
        Updates the velocities and positions
        """
        self.updateVelocities()
        self.updatePositions()

    def totalEnergy(self) -> int:
        """
        Returns the total energy of the system
        """
        totalEnergy = 0
        for body in self.bodies:
            totalEnergy += body.totalEnergy()

        return totalEnergy

    def xAxisEqual(self, otherBodies: List[Body]) -> bool:
        """
        checks if the bodies are equal for the x axis
        """
        if ([body.position.x for body in self.bodies] == [body.position.x for body in otherBodies] and
                not np.any([body.velocity.x for body in self.bodies])):
            return True

    def yAxisEqual(self, otherBodies: List[Body]) -> bool:
        """
        checks if the bodies are equal for the y axis
        """
        if ([body.position.y for body in self.bodies] == [body.position.y for body in otherBodies] and
                not np.any([body.velocity.y for body in self.bodies])):
            return True

    def zAxisEqual(self, otherBodies: List[Body]) -> bool:
        """
        checks if the bodies are equal for the z axis
        """
        if ([body.position.z for body in self.bodies] == [body.position.z for body in otherBodies] and
                not np.any([body.velocity.z for body in self.bodies])):
            return True


def calcTotalEnergy(numSteps: int, verboseOutput: bool = False) -> None:
    """
    Calculates the total energy of the moons after input steps
    """
    nBody = readInput()

    if verboseOutput:
        print(f'After 0 steps\n{nBody}')

    for step in range(numSteps):
        nBody.update()

        if verboseOutput:
            print(f'After {step + 1} steps\n{nBody}')

    print(f'Total Energy = {nBody.totalEnergy()}')


def calcStepsToHistory() -> None:
    """
    Calculates the number of steps before the moons return to a position
    they have already been in before
    """
    nBody = readInput()

    initial = copy.deepcopy(nBody.bodies)
    axisStops = [None, None, None]

    step = 0
    while not np.all(axisStops):
        nBody.update()
        step += 1

        if axisStops[0] is None and nBody.xAxisEqual(initial):
            axisStops[0] = step

        if axisStops[1] is None and nBody.yAxisEqual(initial):
            axisStops[1] = step

        if axisStops[2] is None and nBody.zAxisEqual(initial):
            axisStops[2] = step

    axisStops = np.array(axisStops, dtype=np.uint64)
    numSteps = np.lcm(np.lcm(axisStops[0], axisStops[1]), axisStops[2])
    print(f'Number of steps to history = {numSteps}')


def readInput() -> NBody:
    """
    Reads the input file
    """
    tokenizer = re.compile('<x=(.+), y=(.+), z=(.+)>')

    nBody = NBody()
    with open(INPUT_FILE) as f:
        line = f.readline()
        while line != '':
            x, y, z = tokenizer.findall(line)[0]
            nBody.addBody(Body(position=Vec3(x=int(x), y=int(y), z=int(z)),
                               velocity=Vec3(x=0, y=0, z=0)))
            line = f.readline()

    return nBody


if __name__ == '__main__':
    # calcTotalEnergy(numSteps=1000, verboseOutput=True)
    calcStepsToHistory()
