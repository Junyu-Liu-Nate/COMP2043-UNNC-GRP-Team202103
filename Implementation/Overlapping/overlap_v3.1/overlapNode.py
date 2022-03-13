# -*- coding: UTF-8 -*-
from tokenize import Double
from node import Node

# 一个OverlapNode中包含一组Node，他们因为相互Overlap所以视为一组（一个大Node）方便操作
# 这一组Node存放在__nodesContain中
# 在读入txt后，首先对OverlapNode中小Node的位置进行计算
# __nodesContain中的第一个Node作为定位Node，位置为（0，0）角度0，然后其他Node的位置和角度都作为这个定位Node的相对值
# 然后再使用LayOut Algorithm计算每个Node的位置
# 然后再通过一个function可视化出来
# （一个设想，不知道可不可行）


class OverlapNode:

    def __init__(self, name):
        self.__name = name

        # Coordinates of the rotate center
        self.__xCenter = 0
        self.__yCenter = 0

        # A list of all the containing nodes
        self.__nodesContain = []

        # Generate the containing nodes list
        tempNodesContain = name.split("_")
        for node in tempNodesContain:
            self.__nodesContain.append(Node(node))

    def getName(self):
        return self.__name

    def getNodeNum(self):
        return len(self.__nodesContain)

    def getNodesContain(self):
        return self.__nodesContain

    def getCenter(self):
        return [self.__xCenter, self.__yCenter]

    # def getXAnchor(self):
    #     return self.__nodesContain[0].getXAnchor()

    # def getYAnchor(self):
    #     return self.__nodesContain[0].getYAnchor()

    def setxCenter(self, value):
        self.__xCenter = value

    def setyCenter(self, value):
        self.__yCenter = value

    def findSubNode(self, nodeName):
        length = len(self.__nodesContain)
        for i in range(0, length):
            tempNode = self.__nodesContain[i]

            if isinstance(tempNode, Node):
                if tempNode.getName().find(nodeName) != -1:
                    return tempNode
                else:
                    continue

    # Move all the nodes as a group
    def adjustX(self, value):
        for node in self.__nodesContain:
            node.adjustX(value)

    def adjustY(self, value):
        for node in self.__nodesContain:
            node.adjustY(value)
