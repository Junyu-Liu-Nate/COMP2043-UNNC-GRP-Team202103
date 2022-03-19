import math

class Node:

    def __init__(self, name):
        self.__name = name
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


    #--- Getters ---#
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

    def getAngle(self):
        return self.__angle

    def getConnectPoint1(self):
        return self.__connectPoint1

    def getConnectPoint2(self):
        return self.__connectPoint2

    def getEnd1Coordinate(self):
        return self.__End1Coordinate

    def getEnd2Coordinate(self):
        return self.__End2Coordinate

    def checkIsConnected(self):
        return self.__isConnected

    #--- Setters - Pay attention to updating every attributes !!! ---#
    def setName(self, value):
        self.__name = value

    def setAngle(self, value):
        self.__angle = value
        # self.calEndCoordinate()

    def adjustX(self, value):
        self.__xAnchor = self.__xAnchor + value

        self.__End1Coordinate[0] = self.__End1Coordinate[0] + value
        self.__End2Coordinate[0] = self.__End2Coordinate[0] + value
        self.__connectPoint1[0] = self.__connectPoint1[0] + value
        self.__connectPoint2[0] = self.__connectPoint2[0] + value

    def adjustY(self, value):
        self.__yAnchor = self.__yAnchor + value

        self.__End1Coordinate[1] = self.__End1Coordinate[1] + value
        self.__End2Coordinate[1] = self.__End2Coordinate[1] + value
        self.__connectPoint1[1] = self.__connectPoint1[1] + value
        self.__connectPoint2[1] = self.__connectPoint2[1] + value

    def setConnectPonit1(self, value):
        self.__connectPoint1[0] = value[0]
        self.__connectPoint1[1] = value[1]

    def setConnectPonit2(self, value):
        self.__connectPoint2[0] = value[0]
        self.__connectPoint2[1] = value[1]

    def setIsConnected(self, value):
        self.__isConnected = value

    def calEndCoordinate(self):
        halfLiteralsLength = self.getLiteralsLength() / 2 
        self.__End1Coordinate[0] = self.__xAnchor - halfLiteralsLength * math.cos(math.radians(self.__angle))
        self.__End1Coordinate[1] = self.__xAnchor - halfLiteralsLength * math.sin(math.radians(self.__angle))
        self.__End2Coordinate[0] = self.__xAnchor + halfLiteralsLength * math.cos(math.radians(self.__angle))
        self.__End2Coordinate[1] = self.__xAnchor + halfLiteralsLength * math.sin(math.radians(self.__angle))

    # Calculate the length between 1st letter to last letter
    def getLiteralsLength(self):
        literalslength = (self.getLen() - 1) * 0.18 * 4
        return literalslength

    # Calculate the width of the rectangle
    def getNodeWidth(self):
        # For design pattern 1
        nodeWidth = (self.getLen() - 1) * 0.18 * 4 + 0.5
        # For design pattern 2
        # nodeWidth = (self.getLen() - 1) * 0.18 * 4 + 2
        return nodeWidth

    # Calculate the height of the rectangle
    def getNodeHeight(self):
        nodeHeight = 0.5
        return nodeHeight

    
