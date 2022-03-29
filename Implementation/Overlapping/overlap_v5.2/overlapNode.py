# -*- coding: UTF-8 -*-
# from asyncio.windows_events import NULL
from tokenize import Double
from xml.dom.minicompat import NodeList
from node import Node
from collections import Counter

# 一个OverlapNode中包含一组Node，他们因为相互Overlap所以视为一组（一个大Node）方便操作
# 这一组Node存放在__nodesContain中
# 在读入txt后，首先对OverlapNode中小Node的位置进行计算
# __nodesContain中的第一个Node作为定位Node，位置为（0，0）角度0，然后其他Node的位置和角度都作为这个定位Node的相对值
# 然后再使用LayOut Algorithm计算每个Node的位置
# 然后再通过一个function可视化出来
# （一个设想，不知道可不可行）


class OverlapNode:

    def __init__(self, name, pattern):
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

        #
        self.__isPaired = False
        self.__pairedNode = self.__nodesContain[0]

        #
        self.__radius = 0
        self.calRadius()

        #
        self.__overlapPattern = 1

        #
        self.__overlapPartName = ""
        self.calOverlapPartName()
        


    #--- Getters ---#
    def getName(self):
        return self.__name

    def getNodeNum(self):
        return len(self.__nodesContain)

    def getNodesContain(self):
        return self.__nodesContain

    def getCenter(self):
        return [self.__xCenter, self.__yCenter]

    def checkIsPaired(self):
        return self.__isPaired

    def getPairedNode(self):
        return self.__pairedNode

    def checkIsCalculated(self):
        return self.__isCalculated

    def getRadius(self):
        return self.__radius

    def getOverlapPattern(self):
        return self.__overlapPattern

    def getOverlapPartName(self):
        return self.__overlapPartName

    # def getXAnchor(self):
    #     return self.__nodesContain[0].getXAnchor()

    # def getYAnchor(self):
    #     return self.__nodesContain[0].getYAnchor()

    #--- Setters - Pay attention to updating every attributes !!! ---#
    def setxCenter(self, value):
        self.__xCenter = value

    def setyCenter(self, value):
        self.__yCenter = value

    def setIsPaired(self, value):
        self.__isPaired = value

    def setPairedNode(self, value):
        self.__pairedNode = value

    def setIsCalculated(self, value):
        self.__isCalculated = value

    def setOverlapPattern(self, value):
        self.__overlapPattern = value

    def setOverlapName(self):
        nodeList = self.getNodesContain()
        for node in nodeList:
            node.setOverlapName(self.getName())

    def calRadius(self):
        nodeList = self.getNodesContain()
        nodeWidthList = []
        for node in nodeList:
            nodeWidthList.append(node.getNodeWidth())
        self.__radius = max(nodeWidthList)


    def findSubNode(self, nodeName):
        length = len(self.__nodesContain)
        for i in range(0, length):
            tempNode = self.__nodesContain[i]

            if isinstance(tempNode, Node):
                if tempNode.getName().find(nodeName) != -1:
                    return tempNode
                else:
                    continue

    def calOverlapPartName(self):
        nodeList = self.getNodesContain()

        tempNodeName1 = nodeList[0].getName()
        tempNodeName2 = nodeList[1].getName()
        tempStr1 = Counter(tempNodeName1)
        tempStr2 = Counter(tempNodeName2)
        tempStr3 = tempStr1 & tempStr2
        overlapPartName = "".join(tempStr3.keys())

        self.__overlapPartName = overlapPartName


    # Move all the nodes as a group
    def adjustX(self, value):
        for node in self.__nodesContain:
            node.adjustX(value)

    def adjustY(self, value):
        for node in self.__nodesContain:
            node.adjustY(value)

    def removeNode(self, value):
        for node in self.__nodesContain:
            if node.getName() == value:
                self.__nodesContain.remove(node)
