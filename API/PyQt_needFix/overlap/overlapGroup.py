from tokenize import Double
from node import Node
import math
from overlapNode import OverlapNode
from overlapNode2 import OverlapNode2

class OverlapGroup:
    def __init__(self, overlapNodeList, overlapNodeName):
        self.__overlapNodeList = overlapNodeList
        self.__overlapNodeName = overlapNodeName

        self.__anchorCenter = [0,0]

    #--- Getters ---#
    def getOverlapNodeList(self):
        return self.__overlapNodeList

    def getAnchorCenter(self):
        return self.__anchorCenter

    def getOverlapNodeName(self):
        return self.__overlapNodeName

    #--- Setters - Pay attention to updating every attributes !!! ---#
    def adjustAnchorCenterX(self, value):
        self.__anchorCenter = [self.__anchorCenter[0] + value, self.__anchorCenter[1]]
        # Update All


    def adjustAnchorCenterY(self, value):
        self.__anchorCenter = [self.__anchorCenter[0], self.__anchorCenter[1] + value]

    def updateAll(self, value):
        # update every nodes positions
        overlapNodeList = self.getOverlapNodeList()


    # def findConnectionNode(overlapNode):
    #     for node in overlapNode.getNodesContain():
    #         if node.checkIsConnected() == True:
    #             return node

    def calInitialPositions(self):
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
            #
        else:
            overlapNode1 = overlapNodeList[0]
            overlapNode2 = overlapNodeList[1]
            overlapConnectNode1 = self.findConnectionNode(overlapNode1)
            overlapConnectNode2 = self.findConnectionNode(overlapNode2)

            # calculate positions

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

                # calPosition