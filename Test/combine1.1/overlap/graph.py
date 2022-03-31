# -*- coding: UTF-8 -*-
from node import Node
from overlapNode import OverlapNode
from overlapNode2 import OverlapNode2

class Graph:

    def __init__(self):
        # In the form like: [AB, BC_BH_BF, KL], all Node or OverlapNode objects
        # AB, KL stands for separate nodes, while BC_BH_BF stands for a group of overlapped nodes
        # AB, KL are Node types, while BC_BH_BF is OverlapNode type which is the subtype of Node
        self.__nodeList = []
        self.__edgeList = []

    def readInput(self, fileName, patternNum):
        with open(fileName, "r") as fileHandler:
            # Read nodes
            tempTxt = fileHandler.readline()
            # Split the line using space
            tempNodeList = tempTxt.split()
            for tempNode in tempNodeList:
                # Initialise the overlapped node
                if '_' in tempNode:
                    if patternNum == 1:
                        self.__nodeList.append(OverlapNode(tempNode, patternNum))
                    else:
                        self.__nodeList.append(OverlapNode2(tempNode, patternNum))
                else:
                    self.__nodeList.append(Node(tempNode, patternNum))

            # Read edges
            for edge in fileHandler.readlines():
                self.__edgeList.append(edge.split())

    # Find and return Node instance through name
    def findNode(self, nodeName):
        length = len(self.__nodeList)
        for i in range(0, length):
            tempNode = self.__nodeList[i]

            if isinstance(tempNode, Node):
                if tempNode.getName().find(nodeName) != -1:
                    return tempNode
                else:
                    continue

            if isinstance(tempNode, OverlapNode):
                if tempNode.getName().find(nodeName) != -1:
                    return tempNode.findSubNode(nodeName)
                else:
                    continue

    # Get the number of supernodes
    def getNodeNumber(self):
        return len(self.__nodeList)

    def getNodeList(self):
        return self.__nodeList

    def getEdgeList(self):
        return self.__edgeList