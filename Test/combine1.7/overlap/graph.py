# -*- coding: UTF-8 -*-
from node import Node
from overlapNode import OverlapNode
from overlapNode2 import OverlapNode2

class Graph:
    """
    The Graph class stands for the integration of all nodes
    """
    def __init__(self):
        """
        In the form like: [AB, BC_BH_BF, KL], all Node or OverlapNode objects
        AB, KL stands for separate nodes, while BC_BH_BF stands for a group of overlapped nodes
        AB, KL are Node types, while BC_BH_BF is OverlapNode type which is the subtype of Node
        """
        self.__nodeList = []
        self.__edgeList = []

    def readInput(self, fileName, patternNum):
        """
        Read input from file and create corresponding Node and OverlapNode objects
        :param fileName: a string which stands for the name of input file
        :param patternNum: a number which stands for which display pattern to be used
        :return: no return
        """
        with open(fileName, "r", encoding='utf-8') as fileHandler:
            # Read nodes
            next(fileHandler)
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

    def findNode(self, nodeName):
        """
        Find and return Node instance through name
        :param nodeName: a string which stands for the name of the node
        :return: no return
        """
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

    def getNodeNumber(self):
        """
        Get the number of supernodes
        :return: the number of supernodes
        """
        return len(self.__nodeList)

    def getNodeList(self):
        """
        Get the node list of this Graph object
        :return: the node list of this Graph object
        """
        return self.__nodeList

    def getEdgeList(self):
        """
        Get the edge list of this Graph object
        :return: the edge list of this Graph object
        """
        return self.__edgeList
