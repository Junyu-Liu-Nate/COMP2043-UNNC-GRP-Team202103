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

    def getOverlapNodeList(self):
        """
        Get a list of overlapNode
        :return: a list of overlapNode object which stands for a list of overlapNode
        """

    def getAnchorCenter(self):
        """
        Get the anchor center of this overlapGroup
        :return: a coordinate which stands for the center of this overlapGroup
        """

    def getOverlapNodeName(self):
        """
        Get the name of the overlapNode
        :return: a string which stands for the name of the overlapNode
        """

    def adjustAnchorCenterX(self, value):
        """
        Adjust the x coordinate of the center
        :param value: a number which stands for the x coordinate of the center
        :return: no return
        """

    def adjustAnchorCenterY(self, value):
        """
        Adjust the y coordinate of the center
        :param value: a number which stands for the y coordinate of the center
        :return: no return
        """

    def updateAll(self, value):
        """
        Update every nodes positions
        :param value: a number which stands for the coordinate of the center
        :return: no return
        """

    def calInitialPositions(self):
        """
        Calculate the initial position of this overlapGroup
        :return: no return
        """