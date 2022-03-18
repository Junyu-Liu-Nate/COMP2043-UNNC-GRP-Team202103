from tokenize import Double
from node import Node
from overlapNode import OverlapNode
from collections import Counter

class OverlapNode2(OverlapNode):
    def __init__(self, name):
        OverlapNode.__init__(self, name)
        
        # Used for overlapPattern2
        self.__overlapPart = Node("")
        #self.__overlapConnection = Node("")
        #self.__pariedOverlapPart = Node("")

        self.__remainList = []
        self.separateOverlapPart1()

        self.__radiusList = []

        self.__overlapPattern = 2

    # Separate overlapped part with remaining node lists
    def separateOverlapPart1(self):
        nodeList = self.getNodesContain()

        tempNodeName1 = nodeList[0].getName()
        tempNodeName2 = nodeList[1].getName()
        tempStr1 = Counter(tempNodeName1)
        tempStr2 = Counter(tempNodeName2)
        tempStr3 = tempStr1 & tempStr2
        overlapPartName = "".join(tempStr3.keys())
        self.__overlapPart = Node(overlapPartName)

        for node in nodeList:
            nodeName = node.getName()
            remainName = nodeName.strip(overlapPartName)
            self.__remainList.append(Node(remainName))

    #--- Getters ---#
    def getRemainList(self):
        return self.__remainList

    def getOverlapPart(self):
        return self.__overlapPart

    def getRadiusList(self):
        return self.__radiusList

    def getRotateAngleList(self):
        return self.__rotateAngleList

    #--- Setters ---#
    def setRadiusList(self, value):
        self.__radiusList = value

    # def setRotateAngleList(self, value):
    #     self.__rotateAngleList = value

    def findSubRemainNode(self, nodeName):
        length = len(self.__remainList)
        for i in range(0, length):
            tempNode = self.__remainList[i]

            if isinstance(tempNode, Node):
                if tempNode.getName().find(nodeName) != -1:
                    return tempNode
                else:
                    continue