class OverlapNode:

    """
    The OverlapNode class stands for a collection of overlapped nodes in pattern 1
    """

    def __init__(self, name, pattern):
        """
        Initialize the OverlapNode class
        :param name: a string which stands for the name of the overlapNode
        :param pattern: a number which stands for which display pattern to be used
        """

    def getName(self):
        """
        Get the name of the overlapNode
        :return: a string which stands for the name of the overlapNode
        """

    def getNodeNum(self):
        """
        Get the number of nodes of this overlapNode
        :return: a number which stands for the number of nodes of this overlapNode
        """

    def getNodesContain(self):
        """
        Get the nodes contained in this overlapNode
        :return: a list of node which stands for the nodes contained in this overlapNode
        """

    def getCenter(self):
        """
        Get the center position of this overlapNode
        :return: a coordinate which stands for the center position of this overlapNode
        """

    def checkIsPaired(self):
        """
        Check whether this overlapNode is paired with another overlapNode
        :return: a boolean which stands for whether this overlapNode is paired with another overlapNode
        """

    def getPairedNode(self):
        """
        Get the paired overlapNode if this overlapNode is paired with another overlapNode
        :return: an overlapNode object which stands for the paired overlapNode if this overlapNode is paired with another overlapNode
        """

    def checkIsCalculated(self):
        """
        Check whether this overlapNode is calculated in clustering
        :return: a boolean which stands for whether this overlapNode is calculated in clustering
        """

    def getRadius(self):
        """
        Get the radius of this overlapNode
        :return: a number which stands for the radius of this overlapNode
        """

    def getOverlapPattern(self):
        """
        Get the overlap pattern number
        :return: a number which stands for the overlap pattern number
        """

    def getOverlapPartName(self):
        """
        Get the name of the overlap part
        :return: a string which stands for the name of the overlap part
        """

    def setxCenter(self, value):
        """
        Set the x coordinate of this overlapNode center
        :param value: a number which stands for the x coordinate of this overlapNode center
        :return: no return
        """

    def setyCenter(self, value):
        """
        Set the y coordinate of this overlapNode center
        :param value: a number which stands for the y coordinate of this overlapNode center
        :return: no return
        """

    def setIsPaired(self, value):
        """
        Set whether this overlapNode is paired
        :param value: a boolean which stands for whether this overlapNode is paired
        :return: no return
        """

    def setPairedNode(self, value):
        """
        Set the paired overlapNode
        :param value: an overlapNode object which stands for the paired overlapNode
        :return: no return
        """

    def setIsCalculated(self, value):
        """
        Set whether this overlapNod is calculated when clustering
        :param value: a boolean which stands for whether this overlapNod is calculated when clustering
        :return: no return
        """

    def setOverlapPattern(self, value):
        """
        Set the number of overlap pattern
        :param value: a number which stands for the number of overlap pattern
        :return: no return
        """

    def setOverlapName(self):
        """
        Set the name of the overlap part
        :return: no return
        """

    def calRadius(self):
        """
        Calculate the radius of this overlapNode
        :return: no return
        """

    def findSubNode(self, nodeName):
        """
        Find a sub-node inside this overlapNode with a given name
        :param nodeName: a string which stands for the name of a sub-node
        :return: no return
        """

    def calOverlapPartName(self):
        """
        Calculate the overlap part name of this overlapNode
        :return: no return
        """

    def adjustX(self, value):
        """
        Move all the nodes as a group along x coordinate
        :param value: a number which stands for the value of movement along x coordinate
        :return: no return
        """

    def adjustY(self, value):
        """
        Move all the nodes as a group along y coordinate
        :param value: a number which stands for the value of movement along y coordinate
        :return: no return
        """

    def removeNode(self, value):
        """
        Remove a node from the node list of this overlapNode
        :param value: a node object
        :return: no return
        """