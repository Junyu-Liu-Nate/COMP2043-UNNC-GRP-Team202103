from tokenize import Double
from node import Node
from overlapNode import OverlapNode
from collections import Counter

class OverlapNode2(OverlapNode):
    """
    The OverlapNode class stands for a collection of overlapped nodes in pattern 1
    """
    def __init__(self, name, pattern):
        """
        Initialize the OverlapNode2 class
        :param name: a string which stands for the name of the overlapNode2
        :param pattern: a number which stands for which display pattern to be used
        """
        OverlapNode.__init__(self, name, pattern)
        self.__pattern = pattern

        self.__overlapPart = Node("", pattern)

        self.__remainList = []
        self.separateOverlapPart1()

        self.__radiusList = []

        self.calOverlapName()

    def separateOverlapPart1(self):
        """
        Separate overlapped part with remaining node lists
        :return: no return
        """
        nodeList = self.getNodesContain()

        tempNodeName1 = nodeList[0].getName()
        tempNodeName2 = nodeList[1].getName()
        # tempStr1 = Counter(tempNodeName1)
        # tempStr2 = Counter(tempNodeName2)
        # tempStr3 = tempStr1 & tempStr2
        # overlapPartName = "".join(tempStr3.keys())
        # self.__overlapPart = Node(overlapPartName, self.__pattern)

        i = 0
        overlapPartName = ''
        while tempNodeName1[i] == tempNodeName2[i]:
            overlapPartName += tempNodeName1[i]
            i += 1
        if tempNodeName1[i].isdigit() or tempNodeName2[i].isdigit():
            overlapPartName =  overlapPartName[:-1]
        self.__overlapPart = Node(overlapPartName, self.__pattern)

        for node in nodeList:
            nodeName = node.getName()
            overlapLength = len(overlapPartName)
            remainName = nodeName[overlapLength:]
            #remainName = nodeName.strip(overlapPartName)
            self.__remainList.append(Node(remainName, self.__pattern))

    #--- Getters ---#
    def getRemainList(self):
        """
        Get the list of nodes in the remain node list
        :return: a list of node objects which stands for the list of nodes in the remain node list
        """
        return self.__remainList

    def getOverlapPart(self):
        """
        Get the overlap part of this overlapNode2
        :return: an node object of this overlapNode2
        """
        return self.__overlapPart

    def getRadiusList(self):
        """
        Get the list of radius of this overlapNode2
        :return: a list of numbers which stands for the list of radius of this overlapNode2
        """
        return self.__radiusList

    def getRotateAngleList(self):
        """
        Get the list of rotate angel of this overlapNode2
        :return: a list of numbers which stands for the list of rotate angel of this overlapNode2
        """
        return self.__rotateAngleList

    #--- Setters ---#
    def setRadiusList(self, value):
        """
        Set the radius list of this overlapNode2
        :param value: a list of numbers which stands for the radius list of this overlapNode2
        :return: no return
        """
        self.__radiusList = value

    def findSubRemainNode(self, nodeName):
        """
        Find a node name in the remain node list of this overlapNode2 object
        :param nodeName: a string which indicates a node name in the remain node list of this overlapNode2 object
        :return: no return
        """
        length = len(self.__remainList)
        for i in range(0, length):
            tempNode = self.__remainList[i]

            if isinstance(tempNode, Node):
                if tempNode.getName().find(nodeName) != -1:
                    return tempNode
                else:
                    continue

    def removeRemainNode(self, nodeName):
        """
        Remove a node from the list of remain node
        :param nodeName: a string which stands for the name of the to-be-removed node
        :return: no return
        """
        for node in self.__remainList:
            if node.getName() == nodeName:
                self.__remainList.remove(node)
    
    def calOverlapName(self):
        """
        Calculate the overlapName
        :return: no return
        """
        remianNodeList = self.__remainList
        for node in remianNodeList:
            node.setOverlapName(self.getName())