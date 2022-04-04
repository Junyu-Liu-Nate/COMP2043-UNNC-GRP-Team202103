from tokenize import Double
from node import Node
import math
from overlapNode import OverlapNode
from overlapNode2 import OverlapNode2

class OverlapGroup:
    """
    The OverlapGroup class stands for a collection of connected overlapNodes
     """
    def __init__(self, overlapNodeList, overlapNodeName):
        """
        Initialize the OverlapGroup class
        :param overlapNodeList: a list of overlapNode
        :param overlapNodeName: a string which stands for the name of an overlapNode
        """
        self.__overlapNodeList = overlapNodeList
        self.__overlapNodeName = overlapNodeName

        self.__anchorCenter = [0,0]

    #--- Getters ---#
    def getOverlapNodeList(self):
        """
        Get a list of overlapNode
        :return: a list of overlapNode object which stands for a list of overlapNode
        """
        return self.__overlapNodeList

    def getAnchorCenter(self):
        """
        Get the anchor center of this overlapGroup
        :return: a coordinate which stands for the center of this overlapGroup
        """
        return self.__anchorCenter

    def getOverlapNodeName(self):
        """
        Get the name of the overlapNode
        :return: a string which stands for the name of the overlapNode
        """
        return self.__overlapNodeName

    #--- Setters ---#
    def adjustAnchorCenterX(self, value):
        """
        Adjust the x coordinate of the center
        :param value: a number which stands for the x coordinate of the center
        :return: no return
        """
        self.__anchorCenter = [self.__anchorCenter[0] + value, self.__anchorCenter[1]]

    def adjustAnchorCenterY(self, value):
        """
        Adjust the y coordinate of the center
        :param value: a number which stands for the y coordinate of the center
        :return: no return
        """
        self.__anchorCenter = [self.__anchorCenter[0], self.__anchorCenter[1] + value]

    def updateAll(self, value):
        """
        Update every nodes positions
        :param value: a number which stands for the coordinate of the center
        :return: no return
        """
        overlapNodeList = self.getOverlapNodeList()

    def calInitialPositions(self):
        """
        Calculate the initial position of this overlapGroup
        :return: no return
        """
        overlapNodeList = self.getOverlapNodeList()
        overlapNodeName = self.getOverlapNodeName()
        anchorCenter = self.__getAnchorCenter()

        if len(overlapNodeList == 2):
            overlapNode1 = overlapNodeList[0]
            overlapNode2 = overlapNodeList[1]
            overlapConnectNode1 = self.findConnectionNode(overlapNode1)
            overlapConnectNode2 = self.findConnectionNode(overlapNode2)

            connectionName = overlapConnectNode1.getName()
            connectionNameReverse = connectionName[::-1]
        else:
            overlapNode1 = overlapNodeList[0]
            overlapNode2 = overlapNodeList[1]
            overlapConnectNode1 = self.findConnectionNode(overlapNode1)
            overlapConnectNode2 = self.findConnectionNode(overlapNode2)

            connectionName = overlapConnectNode1.getName()
            center1 = overlapNode1.getCenter()
            angle1 = overlapConnectNode1.getAngle()

            for nextOverlapNode in overlapNodeList[2::]:
                nextOverlapConnectNode = self.findConnectionNode(nextOverlapNode)
                nextOverlapPartName = nextOverlapNode.getOverlapPartName()
                overlapPosition = connectionName.find(nextOverlapPartName)

                moveDistance = 0.18 * 2 * overlapPosition
                nextCenter = [center1[0] + moveDistance * math.cos(math.radians(angle1)), center1[1] + moveDistance * math.sin(math.radians(angle1))]
                nextOverlapNode.setxCenter(nextCenter[0])
                nextOverlapNode.setyCenter(nextCenter[1])

                nextOverlapNode.removeNode(nextOverlapConnectNode.getName())

                remainNodeNum = len(nextOverlapNode.getNodesContain())
                startAngle = 360 / remainNodeNum + angle1