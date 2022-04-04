# -*- coding: UTF-8 -*-
from tokenize import Double
from xml.dom.minicompat import NodeList
from node import Node
from collections import Counter

class OverlapNode:
    """
    The OverlapNode class stands for a collection of overlapped nodes in pattern 1
    """
    def __init__(self, name, pattern):
        """
        Initialize the OverlapNode class
        :param name: a string which stands for the name of the overlapNode
        :param pattern: a number which stands for which display pattern to be used
        """
        self.__name = name
        self.__pattern = pattern

        # Coordinates of the rotate center
        self.__xCenter = 0
        self.__yCenter = 0

        # A list of all the containing nodes
        self.__nodesContain = []

        # Generate the containing nodes list
        tempNodesContain = name.split("_")
        for node in tempNodesContain:
            self.__nodesContain.append(Node(node, pattern))
        self.setOverlapName()

        # Used to indicate whether this overlapNode is connected
        self.__isPaired = False
        self.__pairedNode = self.__nodesContain[0]

        self.__radius = 0
        self.calRadius()

        self.__overlapPattern = 1

        self.__overlapPartName = ""
        self.calOverlapPartName()

    #--- Getters ---#
    def getName(self):
        """
        Get the name of the overlapNode
        :return: a string which stands for the name of the overlapNode
        """
        return self.__name

    def getNodeNum(self):
        """
        Get the number of nodes of this overlapNode
        :return: a number which stands for the number of nodes of this overlapNode
        """
        return len(self.__nodesContain)

    def getNodesContain(self):
        """
        Get the nodes contained in this overlapNode
        :return: a list of node which stands for the nodes contained in this overlapNode
        """
        return self.__nodesContain

    def getCenter(self):
        """
        Get the center position of this overlapNode
        :return: a coordinate which stands for the center position of this overlapNode
        """
        return [self.__xCenter, self.__yCenter]

    def checkIsPaired(self):
        """
        Check whether this overlapNode is paired with another overlapNode
        :return: a boolean which stands for whether this overlapNode is paired with another overlapNode
        """
        return self.__isPaired

    def getPairedNode(self):
        """
        Get the paired overlapNode if this overlapNode is paired with another overlapNode
        :return: an overlapNode object which stands for the paired overlapNode if this overlapNode is paired with another overlapNode
        """
        return self.__pairedNode

    def checkIsCalculated(self):
        """
        Check whether this overlapNode is calculated in clustering
        :return: a boolean which stands for whether this overlapNode is calculated in clustering
        """
        return self.__isCalculated

    def getRadius(self):
        """
        Get the radius of this overlapNode
        :return: a number which stands for the radius of this overlapNode
        """
        return self.__radius

    def getOverlapPattern(self):
        """
        Get the overlap pattern number
        :return: a number which stands for the overlap pattern number
        """
        return self.__overlapPattern

    def getOverlapPartName(self):
        """
        Get the name of the overlap part
        :return: a string which stands for the name of the overlap part
        """
        return self.__overlapPartName

    #--- Setters ---#
    def setxCenter(self, value):
        """
        Set the x coordinate of this overlapNode center
        :param value: a number which stands for the x coordinate of this overlapNode center
        :return: no return
        """
        self.__xCenter = value

    def setyCenter(self, value):
        """
        Set the y coordinate of this overlapNode center
        :param value: a number which stands for the y coordinate of this overlapNode center
        :return: no return
        """
        self.__yCenter = value

    def setIsPaired(self, value):
        """
        Set whether this overlapNode is paired
        :param value: a boolean which stands for whether this overlapNode is paired
        :return: no return
        """
        self.__isPaired = value

    def setPairedNode(self, value):
        """
        Set the paired overlapNode
        :param value: an overlapNode object which stands for the paired overlapNode
        :return: no return
        """
        self.__pairedNode = value

    def setIsCalculated(self, value):
        """
        Set whether this overlapNod is calculated when clustering
        :param value: a boolean which stands for whether this overlapNod is calculated when clustering
        :return: no return
        """
        self.__isCalculated = value

    def setOverlapPattern(self, value):
        """
        Set the number of overlap pattern
        :param value: a number which stands for the number of overlap pattern
        :return: no return
        """
        self.__overlapPattern = value

    def setOverlapName(self):
        """
        Set the name of the overlap part
        :return: no return
        """
        nodeList = self.getNodesContain()
        for node in nodeList:
            node.setOverlapName(self.getName())

    def calRadius(self):
        """
        Calculate the radius of this overlapNode
        :return: no return
        """
        nodeList = self.getNodesContain()
        nodeWidthList = []
        for node in nodeList:
            nodeWidthList.append(node.getNodeWidth())
        self.__radius = max(nodeWidthList)


    def findSubNode(self, nodeName):
        """
        Find a sub-node inside this overlapNode with a given name
        :param nodeName: a string which stands for the name of a sub-node
        :return: no return
        """
        length = len(self.__nodesContain)
        for i in range(0, length):
            tempNode = self.__nodesContain[i]

            if isinstance(tempNode, Node):
                if tempNode.getName().find(nodeName) != -1:
                    return tempNode
                else:
                    continue

    def calOverlapPartName(self):
        """
        Calculate the overlap part name of this overlapNode
        :return: no return
        """
        nodeList = self.getNodesContain()

        tempNodeName1 = nodeList[0].getName()
        tempNodeName2 = nodeList[1].getName()
        tempStr1 = Counter(tempNodeName1)
        tempStr2 = Counter(tempNodeName2)
        tempStr3 = tempStr1 & tempStr2
        overlapPartName = "".join(tempStr3.keys())

        self.__overlapPartName = overlapPartName

    def adjustX(self, value):
        """
        Move all the nodes as a group along x coordinate
        :param value: a number which stands for the value of movement along x coordinate
        :return: no return
        """
        for node in self.__nodesContain:
            node.adjustX(value)

    def adjustY(self, value):
        """
        Move all the nodes as a group along y coordinate
        :param value: a number which stands for the value of movement along y coordinate
        :return: no return
        """
        for node in self.__nodesContain:
            node.adjustY(value)

    def removeNode(self, value):
        """
        Remove a node from the node list of this overlapNode
        :param value: a node object
        :return: no return
        """
        for node in self.__nodesContain:
            if node.getName() == value:
                self.__nodesContain.remove(node)