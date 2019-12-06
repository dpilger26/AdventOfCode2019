"""
Universal Orbit map
"""
import os
import math
import pathlib
from typing import Dict, List, Union

INPUT_FILE = os.path.join(pathlib.Path(__file__).parent, 'input.txt')


def countTotalOrbits():
    """
    Counts the total orbits in the orbital map
    """
    orbitalMap = readInput()

    if 'COM' not in orbitalMap:
        raise RuntimeError('COM not found in orbital map')

    orbitalTree = makeOrbitalTree(orbitalMap=orbitalMap)

    levels = [node.level for node in orbitalTree]
    totalOrbits = math.fsum(levels)
    print(f'Total Orbits = {totalOrbits}')

    return orbitalTree


def orbitalTransfer():
    """
    Counts the number of orbital transfers from YOU to SAN
    """
    orbitalMap = readInput()

    if 'COM' not in orbitalMap:
        raise RuntimeError('COM not found in orbital map')

    orbitalTree = makeOrbitalTree(orbitalMap=orbitalMap)

    # for node in orbitalTree:
    #     print(node)

    parentNodeYOU = getParentNodeByChildName(orbitalTree=orbitalTree, childName='YOU')
    parentNodeSAN = getParentNodeByChildName(orbitalTree=orbitalTree, childName='SAN')

    ancestorsYou = [parentNodeYOU.id]
    ancestorsSan = [parentNodeSAN.id]
    while True:
        ancestorNodeYou = getNodeById(orbitalTree=orbitalTree, nodeId=ancestorsYou[-1])
        ancestorNodeSan = getNodeById(orbitalTree=orbitalTree, nodeId=ancestorsSan[-1])

        if ancestorNodeYou.id in ancestorsSan:
            commonId = ancestorNodeYou.id
            break
        elif ancestorNodeSan.id in ancestorsYou:
            commonId = ancestorNodeSan.id
            break
        else:
            ancestorsYou.append(ancestorNodeYou.parentId)
            ancestorsSan.append(ancestorNodeSan.parentId)

    if commonId is None:
        raise RuntimeError('Unable to find a common id')

    youToCommonSteps = stepsToAncestor(orbitalTree=orbitalTree, node=parentNodeYOU, ancestorId=commonId)
    sanToCommonSteps = stepsToAncestor(orbitalTree=orbitalTree, node=parentNodeSAN, ancestorId=commonId)

    print(f'Number of orbital transfers from YOU to SAN = {youToCommonSteps + sanToCommonSteps}')


class Node:
    """
    Simple Tree Node
    """
    def __init__(self, nodeId: int,
                 parentId: Union[int, None],
                 children: List[str],
                 level: int):
        """
        Constructor
        """
        self.id = nodeId
        self.level = level
        self.parentId = parentId
        self.children = children

    def __str__(self):
        return f'Node(id={self.id}, level={self.level}, parentId={self.parentId}, children={self.children})'

    def __repr__(self):
        return self.__str__()


def makeOrbitalTree(orbitalMap: dict) -> List[Node]:
    """
    Turns the orbital map into a tree
    """
    tree = list()
    tree.append(Node(nodeId=0,
                     parentId=None,
                     children=orbitalMap['COM'],
                     level=0))

    nodeId = 1
    for node in tree:
        if node.children is not None:
            for child in node.children:
                if child in orbitalMap:
                    grandChildren = orbitalMap[child]
                else:
                    grandChildren = None

                tree.append(Node(nodeId=nodeId,
                                 parentId=node.id,
                                 children=grandChildren,
                                 level=node.level + 1))
                nodeId += 1

    return tree


def getParentNodeByChildName(orbitalTree: List[Node], childName: str) -> Node:
    """
    finds the parent node by a child name
    """
    for node in orbitalTree:
        if node.children is not None and childName in node.children:
            return node

    raise RuntimeError(f'Unable to find the {childName} parent.')


def getNodeById(orbitalTree: List[Node], nodeId: int) -> Union[Node, None]:
    """
    finds the node in the tree for the input node id
    """
    for node in orbitalTree:
        if node.id == nodeId:
            return node

    return None


def stepsToAncestor(orbitalTree: List[Node], node: Node, ancestorId: int) -> int:
    """
    Counts the steps from a node to an ancestor id
    """
    steps = 1
    parentNode = getNodeById(orbitalTree=orbitalTree, nodeId=node.parentId)
    while parentNode.parentId != ancestorId:
        parentNode = getNodeById(orbitalTree=orbitalTree, nodeId=parentNode.parentId)
        steps += 1

    return steps + 1


def readInput() -> Dict:
    """
    Reads in the orbital map input file
    """
    with open(INPUT_FILE) as f:
        data = f.read()

    pairs = data.split('\n')

    orbitalMap = dict()
    for pair in pairs:
        host, satellite = pair.split(')')
        if host not in orbitalMap:
            orbitalMap[host] = list()

        orbitalMap[host].append(satellite)

    return orbitalMap


if __name__ == '__main__':
    countTotalOrbits()
    orbitalTransfer()
