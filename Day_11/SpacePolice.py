"""
Emergency Hull Paining Robot
"""
from enum import Enum
import os
import pathlib
from typing import Union, List, Tuple

import numpy as np
import matplotlib.pyplot as plt

INPUT_FILE = os.path.join(pathlib.Path(__file__).parent, 'input.txt')


class IntcodeComputer:
    """
    Simple Intcode computer
    """
    OP_LENGTH_2 = 2
    OP_LENGTH_3 = 3
    OP_LENGTH_4 = 4
    OP_CODE_LENGTH = 2

    OP_1 = 1
    OP_2 = 2
    OP_3 = 3
    OP_4 = 4
    OP_5 = 5
    OP_6 = 6
    OP_7 = 7
    OP_8 = 8
    OP_9 = 9
    OP_STOP = 99

    MODE_POSITION = 0
    MODE_IMMEDIATE = 1
    MODE_RELATIVE = 2

    MEMORY_INITIAL_VALUE = 0

    PROGRAM_RESULT_PTR = 0

    def __init__(self, inputFile: str, verboseOuput: bool = False):
        self.inputFile = inputFile
        self.program = None
        self.sp = 0
        self.instruction = None
        self.opcode = None
        self.firstParameterMode = 0
        self.secondParameterMode = 0
        self.thirdParameterMode = 0
        self.inputs = None
        self.inputCounter = 0
        self.relativeBase = 0

        self.verboseOutput = verboseOuput

        self.reset()

    def initialize(self, value1: int, value2: int):
        """
        Initializes the program for execution
        """
        if self.verboseOutput:
            print(f'Initializing with {value1} and {value2}')

        self.program[1] = value1
        self.program[2] = value2

    def setInputs(self, inputs: List[int]):
        """
        Sets the program inputs
        """
        self.inputs = inputs

    def appendInput(self, value: int):
        """
        Appends an input value to the list of inputs
        """
        if self.inputs is None:
            self.inputs = list()
        self.inputs.append(value)

    def execute(self) -> Union[int, None]:
        """
        Executes the program
        """
        self.getOpcodeAndMode()

        output = None
        while self.opcode != self.OP_STOP:
            if self.opcode == self.OP_1:
                self.opcode1()
            elif self.opcode == self.OP_2:
                self.opcode2()
            elif self.opcode == self.OP_3:
                if self.inputs is not None:
                    if self.inputCounter == len(self.inputs):
                        value = self.inputs[-1]
                    else:
                        value = self.inputs[self.inputCounter]
                        self.inputCounter += 1
                    self.opcode3(value=value)
                else:
                    self.opcode3(value=None)
            elif self.opcode == self.OP_4:
                return self.opcode4()
            elif self.opcode == self.OP_5:
                self.opcode5()
            elif self.opcode == self.OP_6:
                self.opcode6()
            elif self.opcode == self.OP_7:
                self.opcode7()
            elif self.opcode == self.OP_8:
                self.opcode8()
            elif self.opcode == self.OP_9:
                self.opcode9()
            else:
                raise RuntimeError(f'Encountered illigal opcode {self.opcode}')

            self.getOpcodeAndMode()
        else:
            if self.verboseOutput:
                print(f'Received Opcode {self.OP_STOP} and stopping')

        return output

    def storeValue(self, value: int, ptr: int, relativePtr: bool):
        """
        Stores the value at the address pointer
        """
        if relativePtr:
            storePtr = self.relativeBase + ptr
        else:
            storePtr = ptr

        if storePtr > len(self.program) - 1:
            newProgram = [0] * (storePtr + 1)
            newProgram[:len(self.program)] = self.program

            if self.verboseOutput:
                print(f'\tIncreasing memory size from {len(self.program)} to {len(newProgram)}')

            self.program = newProgram

        if self.verboseOutput:
            print(f'\tStoring {value} in {storePtr}')

        self.program[storePtr] = value

    def resume(self) -> Union[int, None]:
        """
        Resumes the execution
        """
        return self.execute()

    def getOpcodeAndMode(self):
        """
        Gets the instructions opcode and modes
        """
        self.instruction = str(self.program[self.sp]).zfill(self.OP_CODE_LENGTH + 3)
        self.opcode = int(self.instruction[-self.OP_CODE_LENGTH:])
        self.firstParameterMode = int(self.instruction[2])
        self.secondParameterMode = int(self.instruction[1])
        self.thirdParameterMode = int(self.instruction[0])

        if self.verboseOutput:
            print(f'Instruction = {self.instruction}: {self.firstParameterMode} {self.secondParameterMode} {self.thirdParameterMode}')

    def opcode1(self):
        """
        Performs the add opcode
        """
        value1, value2 = self.getOpValues()
        storagePtr = self.program[self.sp + 3]

        if self.verboseOutput:
            print(f'\tAdding {value1} and {value2} and storing in {storagePtr}')

        self.storeValue(value=value1 + value2,
                        ptr=storagePtr,
                        relativePtr=True if self.thirdParameterMode == self.MODE_RELATIVE else False)
        self.sp += self.OP_LENGTH_4

    def opcode2(self):
        """
        Performs the multiply opcode
        """
        value1, value2 = self.getOpValues()
        storagePtr = self.program[self.sp + 3]

        if self.verboseOutput:
            print(f'\tMuliplying {value1} and {value2} and storing in {storagePtr}')

        self.storeValue(value=value1 * value2,
                        ptr=storagePtr,
                        relativePtr=True if self.thirdParameterMode == self.MODE_RELATIVE else False)
        self.sp += self.OP_LENGTH_4

    def opcode3(self, value: Union[int, None] = None):
        """
        Opcode 3 takes a single integer as input and saves it to the address given by its only parameter
        """
        storagePtr = self.program[self.sp + 1]

        if value is None:
            value = int(input('\tEnter Process Input: '))

        self.storeValue(value=value,
                        ptr=storagePtr,
                        relativePtr=True if self.firstParameterMode == self.MODE_RELATIVE else False)
        self.sp += self.OP_LENGTH_2

    def opcode4(self) -> int:
        """
        Opcode 4 outputs the value of its only parameter
        """
        storagePtr = self.program[self.sp + 1]

        if self.firstParameterMode == self.MODE_POSITION:
            ptr = storagePtr
        elif self.firstParameterMode == self.MODE_IMMEDIATE:
            ptr = self.sp + 1
        elif self.firstParameterMode == self.MODE_RELATIVE:
            ptr = self.relativeBase + storagePtr
        else:
            raise RuntimeError(f'Unknown output mode {self.firstParameterMode}')

        output = self.program[ptr]
        # print(f'\topcode4 output = {output}')

        self.sp += self.OP_LENGTH_2
        return output

    def opcode5(self):
        """
        Opcode 5 jump-if-true
        """
        value1, value2 = self.getOpValues()
        if value1 != 0:
            self.sp = value2

            if self.verboseOutput:
                print(f'\tJumping to {value2}')
        else:
            self.sp += self.OP_LENGTH_3

    def opcode6(self):
        """
        Opcode 6 jump-if-false
        """
        value1, value2 = self.getOpValues()
        if value1 == 0:
            self.sp = value2

            if self.verboseOutput:
                print(f'\tJumping to {value2}')
        else:
            self.sp += self.OP_LENGTH_3

    def opcode7(self):
        """
        Opcode 7 less than
        """
        value1, value2 = self.getOpValues()
        storagePtr = self.program[self.sp + 3]
        if value1 < value2:
            self.storeValue(value=1,
                            ptr=storagePtr,
                            relativePtr=True if self.thirdParameterMode == self.MODE_RELATIVE else False)
        else:
            self.storeValue(value=0,
                            ptr=storagePtr,
                            relativePtr=True if self.thirdParameterMode == self.MODE_RELATIVE else False)

        if self.verboseOutput:
            print(f'\tOpcode 7 value1 = {value1} and value2 = {value2}; storing {1 if value1 < value2 else 0} to {storagePtr}')

        self.sp += self.OP_LENGTH_4

    def opcode8(self):
        """
        Opcode 8 equals
        """
        value1, value2 = self.getOpValues()
        storagePtr = self.program[self.sp + 3]
        if value1 == value2:
            self.storeValue(value=1,
                            ptr=storagePtr,
                            relativePtr=True if self.thirdParameterMode == self.MODE_RELATIVE else False)
        else:
            self.storeValue(value=0,
                            ptr=storagePtr,
                            relativePtr=True if self.thirdParameterMode == self.MODE_RELATIVE else False)

        if self.verboseOutput:
            print(f'\tOpcode 8 value1 = {value1} and value2 = {value2}; storing {1 if value1 == value2 else 0} to {storagePtr}')

        self.sp += self.OP_LENGTH_4

    def opcode9(self):
        """
        Opcode 9 relative base adjust
        """
        value = self.getOpValueSingle()
        self.relativeBase += value
        if self.verboseOutput:
            print(f'\tOpcode 9 adjusting relative base by {value} to {self.relativeBase}')

        self.sp += self.OP_LENGTH_2

    def getOpValues(self) -> Tuple[int, int]:
        """
        Gets the op values for two value ops
        """
        if self.firstParameterMode == self.MODE_POSITION:
            valuePtr = self.program[self.sp + 1]
            if valuePtr > len(self.program) - 1:
                value1 = self.MEMORY_INITIAL_VALUE
            else:
                value1 = self.program[valuePtr]
        elif self.firstParameterMode == self.MODE_IMMEDIATE:
            value1 = self.program[self.sp + 1]
        elif self.firstParameterMode == self.MODE_RELATIVE:
            valuePtr = self.program[self.sp + 1]
            if self.relativeBase + valuePtr > len(self.program) - 1:
                value1 = self.MEMORY_INITIAL_VALUE
            else:
                value1 = self.program[self.relativeBase + valuePtr]
        else:
            raise RuntimeError(f'Unrecognized first parameter mode {self.firstParameterMode}')

        if self.secondParameterMode == self.MODE_POSITION:
            valuePtr = self.program[self.sp + 2]
            if valuePtr > len(self.program) - 1:
                value2 = self.MEMORY_INITIAL_VALUE
            else:
                value2 = self.program[valuePtr]
        elif self.secondParameterMode == self.MODE_IMMEDIATE:
            value2 = self.program[self.sp + 2]
        elif self.secondParameterMode == self.MODE_RELATIVE:
            valuePtr = self.program[self.sp + 2]
            if self.relativeBase + valuePtr > len(self.program) - 1:
                value2 = self.MEMORY_INITIAL_VALUE
            else:
                value2 = self.program[self.relativeBase + valuePtr]
        else:
            raise RuntimeError(f'Unrecognized second parameter mode {self.secondParameterMode}')

        return value1, value2

    def getOpValueSingle(self) -> Tuple[int, int]:
        """
        Gets the op value for single value ops
        """
        if self.firstParameterMode == self.MODE_POSITION:
            valuePtr = self.program[self.sp + 1]
            if valuePtr > len(self.program) - 1:
                value1 = self.MEMORY_INITIAL_VALUE
            else:
                value1 = self.program[valuePtr]
        elif self.firstParameterMode == self.MODE_IMMEDIATE:
            value1 = self.program[self.sp + 1]
        elif self.firstParameterMode == self.MODE_RELATIVE:
            valuePtr = self.program[self.sp + 1]
            if self.relativeBase + valuePtr > len(self.program) - 1:
                value1 = self.MEMORY_INITIAL_VALUE
            else:
                value1 = self.program[self.relativeBase + valuePtr]
        else:
            raise RuntimeError(f'Unrecognized first parameter mode {self.firstParameterMode}')

        return value1

    def reset(self):
        """
        reads the input file
        """
        with open(self.inputFile) as f:
            self.program = [int(value) for value in f.readline().split(sep=',')]

        self.sp = 0
        self.instruction = None
        self.opcode = None
        self.firstParameterMode = 0
        self.secondParameterMode = 0
        self.thirdParameterMode = 0
        self.inputs = None
        self.inputCounter = 0
        self.relativeBase = 0


class Direction(Enum):
    """
    Direction Enum
    """
    North = 0
    East = 1
    South = 2
    West = 3


def runHullPainterRobot(startingColor: int):
    """
    Estimates the number of tiles that will need painted
    """
    hullPainterRobot = IntcodeComputer(inputFile=INPUT_FILE, verboseOuput=False)

    hull = np.zeros([1000, 1000])
    hullCount = hull.copy()

    row = hull.shape[0] // 2
    col = hull.shape[1] // 2
    direction = Direction.North

    hull[row, col] = startingColor
    hullPainterRobot.appendInput(startingColor)

    while True:
        color = hullPainterRobot.execute()
        # print(f'Color = {color}')
        if color is None:
            break

        hull[row, col] = color
        hullCount[row, col] += 1

        turn = hullPainterRobot.execute()
        # print(f'Turn = {turn}')
        if turn is None:
            break

        if turn == 0:  # left
            if direction == Direction.North:
                direction = Direction.West
                col -= 1
            elif direction == Direction.East:
                direction = Direction.North
                row += 1
            elif direction == Direction.South:
                direction = Direction.East
                col += 1
            elif direction == Direction.West:
                direction = Direction.South
                row -= 1
        elif turn == 1:  # right
            if direction == Direction.North:
                direction = Direction.East
                col += 1
            elif direction == Direction.East:
                direction = Direction.South
                row -= 1
            elif direction == Direction.South:
                direction = Direction.West
                col -= 1
            elif direction == Direction.West:
                direction = Direction.North
                row += 1
        else:
            raise RuntimeError(f'Unknown turn direction {turn}')

        hullPainterRobot.appendInput(hull[row, col])

    tilesPainted = np.count_nonzero(hullCount)
    print(f'Number of tiles painted = {tilesPainted}')

    plt.imshow(hull)
    plt.gca().invert_yaxis()
    plt.show(block=False)


if __name__ == '__main__':
    runHullPainterRobot(startingColor=0)
    runHullPainterRobot(startingColor=1)
