"""
Amplification Circuit
"""
from itertools import permutations
import os
import pathlib
from typing import Tuple, Union, List

INPUT_FILE = os.path.join(pathlib.Path(__file__).parent, 'input.txt')

NUM_AMPS = 5


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
        self.inputs = None
        self.inputCounter = 0

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
            else:
                raise RuntimeError(f'Encountered illigal opcode {self.opcode}')

            self.getOpcodeAndMode()

        return output

    def resume(self) -> Union[int, None]:
        """
        Resumes the execution
        """
        self.inputCounter = 0
        return self.execute()

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

    def opcode3(self, value: Union[int, None] = None):
        """
        Opcode 3 takes a single integer as input and saves it to the address given by its only parameter
        """
        storagePtr = self.program[self.sp + 1]

        if value is None:
            value = int(input('Enter Process Input: '))

        if self.verboseOutput:
            print(f'Storing {value} in {storagePtr}')

        self.program[storagePtr] = value
        self.sp += self.OP_LENGTH_2

    def opcode4(self) -> int:
        """
        Opcode 4 outputs the value of its only parameter
        """
        storagePtr = self.program[self.sp + 1]
        output = self.program[storagePtr]

        if self.verboseOutput:
            print(f'opcode4 output = {self.program[storagePtr]}')

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
        self.inputs = None
        self.inputCounter = 0


def determineSequenceForMaximumThrust():
    """
    Runs the TEST program
    """
    phases = list(range(NUM_AMPS))
    perms = list(permutations(phases))

    ampA = IntcodeComputer(inputFile=INPUT_FILE, verboseOuput=False)
    ampB = IntcodeComputer(inputFile=INPUT_FILE, verboseOuput=False)
    ampC = IntcodeComputer(inputFile=INPUT_FILE, verboseOuput=False)
    ampD = IntcodeComputer(inputFile=INPUT_FILE, verboseOuput=False)
    ampE = IntcodeComputer(inputFile=INPUT_FILE, verboseOuput=False)

    maxSignal = 0
    for perm in perms:
        # print('Running ampA')
        ampA.reset()
        ampA.setInputs(inputs=[perm[0], 0])
        outputA = ampA.execute()

        # print(f'Running ampB with input {outputA}')
        ampB.reset()
        ampB.setInputs(inputs=[perm[1], outputA])
        outputB = ampB.execute()

        # print(f'Running ampC with input {outputB}')
        ampC.reset()
        ampC.setInputs(inputs=[perm[2], outputB])
        outputC = ampC.execute()

        # print(f'Running ampD with input {outputC}')
        ampD.reset()
        ampD.setInputs(inputs=[perm[3], outputC])
        outputD = ampD.execute()

        # print(f'Running ampE with input {outputD}')
        ampE.reset()
        ampE.setInputs(inputs=[perm[4], outputD])
        signal = ampE.execute()

        maxSignal = max(maxSignal, signal)

    print(f'Maximum signal = {maxSignal}')


def determineSequenceForMaximumThrustWithFeedback():
    """
    Runs the TEST program
    """
    phases = list(range(5, 5 + NUM_AMPS))
    perms = list(permutations(phases))

    ampA = IntcodeComputer(inputFile=INPUT_FILE, verboseOuput=False)
    ampB = IntcodeComputer(inputFile=INPUT_FILE, verboseOuput=False)
    ampC = IntcodeComputer(inputFile=INPUT_FILE, verboseOuput=False)
    ampD = IntcodeComputer(inputFile=INPUT_FILE, verboseOuput=False)
    ampE = IntcodeComputer(inputFile=INPUT_FILE, verboseOuput=False)

    maxSignal = 0
    for perm in perms:
        ampA.reset()
        ampB.reset()
        ampC.reset()
        ampD.reset()
        ampE.reset()

        # print('Running ampA')
        ampA.setInputs(inputs=[perm[0], 0])
        outputA = ampA.execute()

        # print(f'Running ampB with input {outputA}')
        ampB.setInputs(inputs=[perm[1], outputA])
        outputB = ampB.execute()

        # print(f'Running ampC with input {outputB}')
        ampC.setInputs(inputs=[perm[2], outputB])
        outputC = ampC.execute()

        # print(f'Running ampD with input {outputC}')
        ampD.setInputs(inputs=[perm[3], outputC])
        outputD = ampD.execute()

        # print(f'Running ampE with input {outputD}')
        ampE.setInputs(inputs=[perm[4], outputD])
        outputE = ampE.execute()

        while True:
            # print(f'Running ampA with input {outputE}')
            ampA.setInputs(inputs=[outputE])
            outputA = ampA.resume()

            if outputA is None:
                signal = outputE
                break

            # print(f'Running ampB with input {outputA}')
            ampB.setInputs(inputs=[outputA])
            outputB = ampB.resume()

            if outputB is None:
                signal = outputA
                break

            # print(f'Running ampC with input {outputB}')
            ampC.setInputs(inputs=[outputB])
            outputC = ampC.resume()

            if outputC is None:
                signal = outputB
                break

            # print(f'Running ampD with input {outputC}')
            ampD.setInputs(inputs=[outputC])
            outputD = ampD.resume()

            if outputD is None:
                signal = outputC
                break

            # print(f'Running ampE with input {outputD}')
            ampE.setInputs(inputs=[outputD])
            outputE = ampE.resume()

            if outputE is None:
                signal = outputD
                break

        maxSignal = max(maxSignal, signal)

    print(f'Maximum signal with feedback = {maxSignal}')


if __name__ == '__main__':
    determineSequenceForMaximumThrust()
    determineSequenceForMaximumThrustWithFeedback()
