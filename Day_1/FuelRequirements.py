"""
Calculates the sum total of Santa's fuel requirements
based on the input file
"""
import math
import pandas as pd

INPUT_FILE = r'./input.txt'
COLUMN_NAME = 'Mass'


def calculateFuelRequirements() -> int:
    """
    Calculates the sum total of Santa's fuel requirements
    based on the input file
    :return: total fuel requirements
    """
    data = readInput()
    fuels = [calculateFuelByMass(mass=mass) for mass in data[COLUMN_NAME]]

    initialSummation = int(math.fsum(fuels))
    print(f'initial summation = {initialSummation}')

    # now add to the fuel requirements the fuel needed for the fuel
    additionalFuels = [calculateFuelForFuel(mass=mass) for mass in fuels]

    additionalSummation = int(math.fsum(additionalFuels))
    print(f'additional summation = {additionalSummation}')

    totalSummation = initialSummation + additionalSummation
    print(f'total summation = {totalSummation}')

    return totalSummation


def calculateFuelByMass(mass: int) -> int:
    """
    Calculates the fuel required by mass
    :param mass:
    :return: fuel:
    """
    return math.floor(mass / 3) - 2


def calculateFuelForFuel(mass: int) -> int:
    """
    Calculates the total amount of extra fuel need to lift the fuel
    :param mass: the mass of the fuel
    :return: additional needed fuel:
    """
    totalAdditionalFuel = 0
    additionalFuel = calculateFuelByMass(mass)
    while additionalFuel > 0:
        totalAdditionalFuel += additionalFuel
        additionalFuel = calculateFuelByMass(additionalFuel)

    return totalAdditionalFuel


def readInput() -> pd.DataFrame:
    """
    reads the input file and returns the values
    :return: pandas DataFrame of the input data file
    """
    return pd.read_csv(INPUT_FILE, sep='\n', names=[COLUMN_NAME])


if __name__ == '__main__':
    calculateFuelRequirements()
