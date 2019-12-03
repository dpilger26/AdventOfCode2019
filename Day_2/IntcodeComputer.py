"""
A simple Intcode Computer
"""
import os
import pathlib
from typing import List

INPUT_FILE = os.path.join(pathlib.Path(__file__).parent, 'input.txt')

OP_LENGTH = 4
OP_ADD = 1
OP_MULT = 2
OP_STOP = 99

PROGRAM_RESULT_PTR = 0

RESTORE_VALUE_1 = 12
RESTORE_VALUE_2 = 2

GRAVITY_ASSIST_OUTPUT = 19690720
MAX_NOUN = 100  # exclusive
MAX_VERB = 100  # exclusive


def restoreProgram():
    """
    Restores the program after 1202 error
    """
    program = readInput()
    program = initialize(program=program, value1=RESTORE_VALUE_1, value2=RESTORE_VALUE_2)
    program = execute(program=program, verboseOutput=False)

    print(f'Restore Program program[{PROGRAM_RESULT_PTR}] = {program[PROGRAM_RESULT_PTR]}')


def runGravityAssistProgram():
    """
    Runs the gravity assist program by brute force
    """
    program = readInput()

    solutionFound = False
    theNoun = 0
    theVerb = 0
    for noun in range(MAX_NOUN):
        for verb in range(MAX_VERB):
            programIteration = program[:]
            programIteration = initialize(program=programIteration, value1=noun, value2=verb)
            programIteration = execute(program=programIteration, verboseOutput=False)

            if programIteration[PROGRAM_RESULT_PTR] == GRAVITY_ASSIST_OUTPUT:
                theNoun = noun
                theVerb = verb
                solutionFound = True
                break

    if not solutionFound:
        raise RuntimeError('No solution found')

    print(f'Gravity Assist finalOutput = {finalOutput(noun=theNoun, verb=theVerb)}')


def initialize(program: List[int], value1: int, value2: int) -> List[int]:
    """
    Initializes the program for execution
    :param program:
    :param value1:
    :param value2:
    :return: initialized program
    """
    program[1] = value1
    program[2] = value2

    return program


def execute(program: List[int], verboseOutput: bool = False) -> List[int]:
    """
    Executes the program
    :param program:
    :param verboseOutput:
    :return: executed program
    """
    sp = 0
    opcode = program[sp]
    while opcode != OP_STOP:
        if verboseOutput:
            print(f'sp = {sp}')
            print(program[sp: sp + OP_LENGTH])

        if opcode == OP_ADD:
            program = opcodeAdd(program, sp)
        elif opcode == OP_MULT:
            program = opcodeMultiply(program, sp)
        else:
            raise RuntimeError(f'Encountered illigal opcode {opcode}')

        sp += OP_LENGTH
        opcode = program[sp]

    return program


def opcodeAdd(program: List[int], sp: int) -> List[int]:
    """
    Performs the add opcode
    :param program:
    :param sp: the current stack pointer
    :return: program:
    """
    valuePtr1 = program[sp + 1]
    valuePtr2 = program[sp + 2]
    storagePtr = program[sp + 3]

    program[storagePtr] = program[valuePtr1] + program[valuePtr2]

    return program


def opcodeMultiply(program: List[int], sp: int) -> List[int]:
    """
    Performs the multiply opcode
    :param program:
    :param sp: the current stack pointer
    :return: program:
    """
    valuePtr1 = program[sp + 1]
    valuePtr2 = program[sp + 2]
    storagePtr = program[sp + 3]

    program[storagePtr] = program[valuePtr1] * program[valuePtr2]

    return program


def finalOutput(noun: int, verb: int) -> int:
    """
    Calculates the final output from the Gravity Assist program
    :param noun:
    :param verb:
    :return: final output
    """
    return 100 * noun + verb


def readInput() -> List[int]:
    """
    reads the input file and returns the values
    :return: List[int] of the input data file
    """
    with open(INPUT_FILE) as f:
        return [int(value) for value in f.readline().split(sep=',')]


if __name__ == '__main__':
    restoreProgram()
    runGravityAssistProgram()
