# -*- coding: UTF-8 -*-
class Node:

    def __init__(self, name):
        self.__name = name
        # 定位点坐标
        self.__xAnchor = 0
        self.__yAnchor = 0
        self.__angle = 0

    def getName(self):
        return self.__name

    # The length of the node equals to the number of letter in the name
    def getLen(self):
        length = 0
        for literal in self.__name:
            if literal.isalpha():
                length = length + 1

        return length

    def getXAnchor(self):
        return self.__xAnchor

    def getYAnchor(self):
        return self.__yAnchor

    def setAngle(self, value):
        self.__angle = value
    
    def getAngle(self):
        return self.__angle

    def adjustX(self, value):
        self.__xAnchor = self.__xAnchor + value

    def adjustY(self, value):
        self.__yAnchor = self.__yAnchor + value

    #################
    # 计算长方体长宽的方法能不能放在这
    # 然后能不能写一个计算长方体四个角的坐标的方法

    def getLiteralsLength(self):
        literalslength = (self.getLen() - 1) * 0.18 * 4
        return literalslength

    def getNodeWidth(self):
        # For design pattern 1
        # nodeWidth = (self.getLen() - 1) * 0.18 * 4 + 0.5
        # For design pattern 2
        nodeWidth = (self.getLen() - 1) * 0.18 * 4 + 2
        return nodeWidth

    def getNodeHeight(self):
        nodeHeight = 0.5
        return nodeHeight
