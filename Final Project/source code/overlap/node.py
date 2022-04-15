# -*- coding: UTF-8 -*-
import math
from numpy import inner

class Node:
    """
    The Node class stands for a node on the graph
    """
    def __init__(self, name, pattern):
        """
        Initialize the Node class
        :param name: a string which stands for the name of the node
        :param pattern: a number which stands for which display pattern to be used
        """
        self.__name = name
        self.__pattern = pattern

        # Anchor Points Coordinate
        self.__xAnchor = 0
        self.__yAnchor = 0

        # Rotate Angle
        self.__angle = 0

        # Coordinates of the 2 edge-connection points
        self.__connectPoint1 = [0,0]
        self.__connectPoint2 = [0,0]

        # Coordinates of the 2 ends
        self.__End1Coordinate = [0,0]
        self.__End2Coordinate = [0,0]
        self.calEndCoordinate()

        # Used to check whether this node is used to connect two overlapped nodes
        self.__isConnected = False

        # Used to get the overlapNode name
        self.__overlapName = ""


    #--- Getters ---#
    def getName(self):
        """
        Get the name of the node
        :return: a string which stands for the name of the node
        """
        return self.__name

    def getLen(self):
        """
        Get the length of the node equals to the number of letter in the name
        :return: a number which stands for the length of the node equals to the number of letter in the name
        """
        length = 0
        for literal in self.__name:
            if literal.isalpha():
                length = length + 1

        return length

    def getXAnchor(self):
        """
        Get the x coordinate of this node position
        :return: a number which stands for the x coordinate of this node position
        """
        return self.__xAnchor

    def getYAnchor(self):
        """
        Get the y coordinate of this node position
        :return: a number which stands for the y coordinate of this node position
        """
        return self.__yAnchor

    def getAngle(self):
        """
        Get the rotate angle of this node
        :return: a number which stands for the rotate angle of this node
        """
        return self.__angle

    def getConnectPoint1(self):
        """
        Get the first edge connection point of this node
        :return: a coordinate which stands for the first edge connection point of this node
        """
        return self.__connectPoint1

    def getConnectPoint2(self):
        """
        Get the second edge connection point of this node
        :return: a coordinate which stands for the second edge connection point of this node
        """
        return self.__connectPoint2

    def getEnd1Coordinate(self):
        """
        Get the point of the first end-literals of this node
        :return: a coordinate which stands for the first end-literals of this node
        """
        return self.__End1Coordinate

    def getEnd2Coordinate(self):
        """
        Get the point of the second end-literals of this node
        :return: a coordinate which stands for the second end-literals of this node
        """
        return self.__End2Coordinate

    def getOverlapName(self):
        """
        Get the overlapNode name if this node belongs to an overlapNode
        :return: a string which stands for the overlapNode name if this node belongs to an overlapNode
        """
        return self.__overlapName

    def checkIsConnected(self):
        """
        Check whether the node is connected in overlap pairs or groups
        :return: a boolean which stands for whether the node is connected in overlap pairs or groups
        """
        return self.__isConnected

    #--- Setters ---#
    def setName(self, value):
        """
        Set the name for this node
        :param value: s string which stands for the name of this node
        :return: no return
        """
        self.__name = value

    def setAngle(self, value):
        """
        Set the rotate angle of this node
        :param value: a number which indicates the rotate angle of this node
        :return: no return
        """
        self.__angle = value
        # self.calEndCoordinate()

    def adjustX(self, value):
        """
        Adjust the node position along x axis
        :param value: a number which stands for the value of movement along x axis
        :return: no return
        """
        self.__xAnchor = self.__xAnchor + value

        self.__End1Coordinate[0] = self.__End1Coordinate[0] + value
        self.__End2Coordinate[0] = self.__End2Coordinate[0] + value
        self.__connectPoint1[0] = self.__connectPoint1[0] + value
        self.__connectPoint2[0] = self.__connectPoint2[0] + value

    def adjustY(self, value):
        """
        Adjust the node position along y axis
        :param value: a number which stands for the value of movement along y axis
        :return: no return
        """
        self.__yAnchor = self.__yAnchor + value

        self.__End1Coordinate[1] = self.__End1Coordinate[1] + value
        self.__End2Coordinate[1] = self.__End2Coordinate[1] + value
        self.__connectPoint1[1] = self.__connectPoint1[1] + value
        self.__connectPoint2[1] = self.__connectPoint2[1] + value

    def setConnectPonit1(self, value):
        """
        Set the first edge connection point of this node
        :param value: a coordinate which stands for the first edge connection point of this node
        :return: no return
        """
        self.__connectPoint1[0] = value[0]
        self.__connectPoint1[1] = value[1]

    def setConnectPonit2(self, value):
        """
        Set the second edge connection point of this node
        :param value: a coordinate which stands for the second edge connection point of this node
        :return: no return
        """
        self.__connectPoint2[0] = value[0]
        self.__connectPoint2[1] = value[1]

    def setIsConnected(self, value):
        """
        Set whether this node is a connection node of an overlap pair or overlap group
        :param value: a boolean which stands for whether this node is a connection node of an overlap pair or overlap group
        :return: no return
        """
        self.__isConnected = value

    def setOverlapName(self, value):
        """
        Set the overlapNode name if this node belongs to an overlapNode
        :param value: a string which stands for the overlapNode name if this node belongs to an overlapNode
        :return: no return
        """
        self.__overlapName = value

    def setAngle(self, value):
        """
        Set the rotate angle of this node
        :param value: a number which stands for the rotate angle of this node
        :return: no return
        """
        self.__angle = value
        #self.calEndCoordinate()

    def calEndCoordinate(self):
        """
        Calculate the end coordinate of the two end-literal positions
        :return: no return
        """
        halfLiteralsLength = self.getLiteralsLength() / 2 
        self.__End1Coordinate[0] = self.__xAnchor - halfLiteralsLength * math.cos(math.radians(self.__angle))
        self.__End1Coordinate[1] = self.__xAnchor - halfLiteralsLength * math.sin(math.radians(self.__angle))
        self.__End2Coordinate[0] = self.__xAnchor + halfLiteralsLength * math.cos(math.radians(self.__angle))
        self.__End2Coordinate[1] = self.__xAnchor + halfLiteralsLength * math.sin(math.radians(self.__angle))

    def getLiteralsLength(self):
        """
        Calculate the length between 1st letter to last letter
        :return: a number which stands for the length between 1st letter to last letter
        """
        literalslength = (self.getLen() - 1) * 0.18 * 4
        return literalslength

    def getNodeWidth(self):
        """
        Calculate the width of the rectangle
        :return: a number which stands for the width of the rectangle
        """
        if self.__pattern == 1:
            nodeWidth = (self.getLen() - 1) * 0.18 * 4 + 0.5
        elif self.__pattern == 2:
            nodeWidth = (self.getLen() - 1) * 0.18 * 4 + 2
        else:
            print("Invalid pattern type.")

        return nodeWidth


    def getNodeHeight(self):
        """
        Calculate the height of the rectangle
        :return: a number which stands for the height of the rectangle
        """
        nodeHeight = 0.5
        return nodeHeight

    def getNodeCorners(self):
        """
        Calculate the positions of four corners of this node
        :return: a list of coordinates which stands for the positions of four corners of this node
        """
        nodeWidth = self.getNodeWidth()
        nodeHeight = self.getNodeHeight()
        nodeCenter = [self.getXAnchor(), self.getYAnchor()]
        rotateAngle = self.getAngle()

        innerAngle = math.degrees(math.atan(nodeHeight / nodeWidth))

        calAngle1 = rotateAngle + innerAngle
        calAngle2 = rotateAngle - innerAngle
        calLength = 0.5 * math.sqrt(nodeWidth * nodeWidth + nodeHeight * nodeHeight)

        pos3 = [nodeCenter[0] + calLength * math.cos(math.radians(calAngle1)), nodeCenter[1] + calLength * math.sin(math.radians(calAngle1))]
        pos2 = [nodeCenter[0] - calLength * math.cos(math.radians(calAngle1)), nodeCenter[1] - calLength * math.sin(math.radians(calAngle1))]
        pos4 = [nodeCenter[0] + calLength * math.cos(math.radians(calAngle2)), nodeCenter[1] + calLength * math.sin(math.radians(calAngle2))]
        pos1 = [nodeCenter[0] - calLength * math.cos(math.radians(calAngle2)), nodeCenter[1] - calLength * math.sin(math.radians(calAngle2))]

        return [pos1, pos2, pos3, pos4]