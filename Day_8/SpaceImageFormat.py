"""
Space Image Format
"""
import os
import pathlib

import numpy as np
import matplotlib.pyplot as plt

NUM_ROWS = 6
NUM_COLS = 25
SIZE = NUM_ROWS * NUM_COLS

BLACK_PIXEL = 0
WHITE_PIXEL = 1
TRANSPARENT_PIXEL = 2
UNSET_PIXEL = 3

INPUT_FILE = os.path.join(pathlib.Path(__file__).parent, 'input.txt')


def checkImageCorruption():
    """
    Checks the input image for corruption
    """
    image = readInput()

    minCountZeros = NUM_ROWS * NUM_COLS
    minLayer = 0
    for layer in range(image.shape[0]):
        numZeros = np.count_nonzero(image[layer, :, :] == 0)
        if numZeros < minCountZeros:
            minCountZeros = numZeros
            minLayer = layer

    numOnes = np.count_nonzero(image[minLayer, :, :] == 1)
    numTwos = np.count_nonzero(image[minLayer, :, :] == 2)

    print(f'Corruption check output = {numOnes * numTwos}')


def decodeImage():
    """
    Decodes the input image
    """
    image = readInput()

    decodedImage = np.ones(SIZE) * UNSET_PIXEL
    for layer in range(image.shape[0]):
        layerImage = image[layer, :, :].flatten()
        indicesUnset = np.nonzero(decodedImage == UNSET_PIXEL)[0]

        indicesBlack = np.nonzero(layerImage == BLACK_PIXEL)[0]
        indicesBlack = np.intersect1d(indicesBlack, indicesUnset)
        decodedImage[indicesBlack] = BLACK_PIXEL

        indicesWhite = np.nonzero(layerImage == WHITE_PIXEL)[0]
        indicesWhite = np.intersect1d(indicesWhite, indicesUnset)
        decodedImage[indicesWhite] = WHITE_PIXEL

        if (np.count_nonzero(decodedImage == UNSET_PIXEL) == 0 and
                np.count_nonzero(decodedImage == TRANSPARENT_PIXEL) == 0):
            break

    plt.matshow(np.reshape(decodedImage, [NUM_ROWS, NUM_COLS]), cmap='gray')
    plt.show(block=True)


def readInput():
    """
    Reads the input file
    """
    with open(INPUT_FILE) as f:
        data = list(f.readline())

    data = [int(value) for value in data]

    numLayers = int(len(data) / NUM_ROWS / NUM_COLS)
    image = np.array(data).reshape(numLayers, NUM_ROWS, NUM_COLS)

    return image.astype(np.int)


if __name__ == '__main__':
    checkImageCorruption()
    decodeImage()
