from tokenize import Double
from node import Node
from overlapNode import OverlapNode
from collections import Counter

class OverlapNode2(OverlapNode):
    def __init__(self, name, pattern):
        OverlapNode.__init__(self, name, pattern)
        self.__pattern = pattern
        
        # Used for overlapPattern2
        self.__overlapPart = Node("", pattern)

        self.__remainList = []
        self.separateOverlapPart1()

        self.__radiusList = []

        self.calOverlapName()

    # Separate overlapped part with remaining node lists
    def separateOverlapPart1(self):
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
        #print(overlapPartName)
        self.__overlapPart = Node(overlapPartName, self.__pattern)

        for node in nodeList:
            nodeName = node.getName()
            overlapLength = len(overlapPartName)
            remainName = nodeName[overlapLength:]
            #remainName = nodeName.strip(overlapPartName)
            self.__remainList.append(Node(remainName, self.__pattern))

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

    def findSubRemainNode(self, nodeName):
        length = len(self.__remainList)
        for i in range(0, length):
            tempNode = self.__remainList[i]

            if isinstance(tempNode, Node):
                if tempNode.getName().find(nodeName) != -1:
                    return tempNode
                else:
                    continue

    def removeRemainNode(self, nodeName):
        for node in self.__remainList:
            if node.getName() == nodeName:
                self.__remainList.remove(node)
    
    def calOverlapName(self):
        remianNodeList = self.__remainList
        for node in remianNodeList:
            node.setOverlapName(self.getName())