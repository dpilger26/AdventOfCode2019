"""
A simple Incode Computer
"""
import os
import pathlib
from typing import Tuple

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
    OP_STOP = 99

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

    def execute(self) -> int:
        """
        Executes the program
        """
        self.getOpcodeAndMode()

        while self.opcode != self.OP_STOP:
            if self.opcode == self.OP_1:
                self.opcode1()
            elif self.opcode == self.OP_2:
                self.opcode2()
            elif self.opcode == self.OP_3:
                self.opcode3()
            elif self.opcode == self.OP_4:
                self.opcode4()
            elif self.opcode == self.OP_5:
                self.opcode5()
            elif self.opcode == self.OP_6:
                self.opcode6()
            elif self.opcode == self.OP_7:
                self.opcode7()
            elif self.opcode == self.OP_8:
                self.opcode8()
            else:
                raise RuntimeError(f'Encountered illigal opcode {self.opcode}')

            self.getOpcodeAndMode()

        return self.program[self.PROGRAM_RESULT_PTR]

    def getOpcodeAndMode(self):
        """
        Gets the instructions opcode and modes
        """
        self.instruction = str(self.program[self.sp]).zfill(self.OP_CODE_LENGTH + 3)
        if self.verboseOutput:
            print(f'Instruction = {self.instruction}')

        self.opcode = int(self.instruction[-self.OP_CODE_LENGTH:])
        self.firstParameterMode = int(self.instruction[2])
        self.secondParameterMode = int(self.instruction[1])
        self.thirdParameterMode = int(self.instruction[0])

    def opcode1(self):
        """
        Performs the add opcode
        """
        value1, value2 = self.getOpValues()
        storagePtr = self.program[self.sp + 3]

        if self.verboseOutput:
            print(f'Adding {value1} and {value2} and storing in {storagePtr}')

        self.program[storagePtr] = value1 + value2
        self.sp += self.OP_LENGTH_4

    def opcode2(self):
        """
        Performs the multiply opcode
        """
        value1, value2 = self.getOpValues()
        storagePtr = self.program[self.sp + 3]

        if self.verboseOutput:
            print(f'Muliplying {value1} and {value2} and storing in {storagePtr}')

        self.program[storagePtr] = value1 * value2
        self.sp += self.OP_LENGTH_4

    def opcode3(self):
        """
        Opcode 3 takes a single integer as input and saves it to the address given by its only parameter
        """
        storagePtr = self.program[self.sp + 1]
        value = int(input('Enter Process Input: '))

        if self.verboseOutput:
            print(f'Storing {value} in {storagePtr}')

        self.program[storagePtr] = value
        self.sp += self.OP_LENGTH_2

    def opcode4(self):
        """
        Opcode 4 outputs the value of its only parameter
        """
        storagePtr = self.program[self.sp + 1]
        print(f'opcode4 output = {self.program[storagePtr]}')
        self.sp += self.OP_LENGTH_2

    def opcode5(self):
        """
        Opcode 5 jump-if-true
        """
        value1, value2 = self.getOpValues()
        if value1 != 0:
            self.sp = value2

            if self.verboseOutput:
                print(f'Jumping to {value2}')
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
                print(f'Jumping to {value2}')
        else:
            self.sp += self.OP_LENGTH_3

    def opcode7(self):
        """
        Opcode 7 less than
        """
        value1, value2 = self.getOpValues()
        storagePtr = self.program[self.sp + 3]
        if value1 < value2:
            self.program[storagePtr] = 1
        else:
            self.program[storagePtr] = 0

        if self.verboseOutput:
            print(f'Opcode 7 storing {1 if value1 < value2 else 0} to {storagePtr}')

        self.sp += self.OP_LENGTH_4

    def opcode8(self):
        """
        Opcode 8 equals
        """
        value1, value2 = self.getOpValues()
        storagePtr = self.program[self.sp + 3]
        if value1 == value2:
            self.program[storagePtr] = 1
        else:
            self.program[storagePtr] = 0

        if self.verboseOutput:
            print(f'Opcode 8 storing {1 if value1 == value2 else 0} to {storagePtr}')

        self.sp += self.OP_LENGTH_4

    def getOpValues(self) -> Tuple[int, int]:
        """
        Gets the add or multiply op values
        """
        if self.firstParameterMode == 0:
            valuePtr = self.program[self.sp + 1]
            value1 = self.program[valuePtr]
        elif self.firstParameterMode == 1:
            value1 = self.program[self.sp + 1]
        else:
            raise RuntimeError(f'Unrecognized first parameter mode {self.firstParameterMode}')

        if self.secondParameterMode == 0:
            valuePtr = self.program[self.sp + 2]
            value2 = self.program[valuePtr]
        elif self.secondParameterMode == 1:
            value2 = self.program[self.sp + 2]
        else:
            raise RuntimeError(f'Unrecognized second parameter mode {self.secondParameterMode}')

        return value1, value2

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


def runTEST():
    """
    Runs the TEST program
    """
    comp = IntcodeComputer(inputFile=INPUT_FILE, verboseOuput=False)
    comp.execute()


if __name__ == '__main__':
    runTEST()
