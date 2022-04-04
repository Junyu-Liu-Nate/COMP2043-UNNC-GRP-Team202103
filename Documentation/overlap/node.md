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

    def getName(self):
        """
        Get the name of the node
        :return: a string which stands for the name of the node
        """

    def getLen(self):
        """
        Get the length of the node equals to the number of letter in the name
        :return: a number which stands for the length of the node equals to the number of letter in the name
        """

    def getXAnchor(self):
        """
        Get the x coordinate of this node position
        :return: a number which stands for the x coordinate of this node position
        """

    def getYAnchor(self):
        """
        Get the y coordinate of this node position
        :return: a number which stands for the y coordinate of this node position
        """

    def getAngle(self):
        """
        Get the rotate angle of this node
        :return: a number which stands for the rotate angle of this node
        """

    def getConnectPoint1(self):
        """
        Get the first edge connection point of this node
        :return: a coordinate which stands for the first edge connection point of this node
        """

    def getConnectPoint2(self):
        """
        Get the second edge connection point of this node
        :return: a coordinate which stands for the second edge connection point of this node
        """

    def getEnd1Coordinate(self):
        """
        Get the point of the first end-literals of this node
        :return: a coordinate which stands for the first end-literals of this node
        """

    def getEnd2Coordinate(self):
        """
        Get the point of the second end-literals of this node
        :return: a coordinate which stands for the second end-literals of this node
        """

    def getOverlapName(self):
        """
        Get the overlapNode name if this node belongs to an overlapNode
        :return: a string which stands for the overlapNode name if this node belongs to an overlapNode
        """
    
    def checkIsConnected(self):
        """
        Check whether the node is connected in overlap pairs or groups
        :return: a boolean which stands for whether the node is connected in overlap pairs or groups
        """

    def setName(self, value):
        """
        Set the name for this node
        :param value: s string which stands for the name of this node
        :return: no return
        """

    def setAngle(self, value):
        """
        Set the rotate angle of this node
        :param value: a number which indicates the rotate angle of this node
        :return: no return
        """

    def adjustX(self, value):
        """
        Adjust the node position along x axis
        :param value: a number which stands for the value of movement along x axis
        :return: no return
        """

    def adjustY(self, value):
        """
        Adjust the node position along y axis
        :param value: a number which stands for the value of movement along y axis
        :return: no return
        """

    def setConnectPonit1(self, value):
        """
        Set the first edge connection point of this node
        :param value: a coordinate which stands for the first edge connection point of this node
        :return: no return
        """

    def setConnectPonit2(self, value):
        """
        Set the second edge connection point of this node
        :param value: a coordinate which stands for the second edge connection point of this node
        :return: no return
        """

    def setIsConnected(self, value):
        """
        Set whether this node is a connection node of an overlap pair or overlap group
        :param value: a boolean which stands for whether this node is a connection node of an overlap pair or overlap group
        :return: no return
        """

    def setOverlapName(self, value):
        """
        Set the overlapNode name if this node belongs to an overlapNode
        :param value: a string which stands for the overlapNode name if this node belongs to an overlapNode
        :return: no return
        """

    def setAngle(self, value):
        """
        Set the rotate angle of this node
        :param value: a number which stands for the rotate angle of this node
        :return: no return
        """

    def calEndCoordinate(self):
        """
        Calculate the end coordinate of the two end-literal positions
        :return: no return
        """

    def getLiteralsLength(self):
        """
        Calculate the length between 1st letter to last letter
        :return: a number which stands for the length between 1st letter to last letter
        """

    def getNodeWidth(self):
        """
        Calculate the width of the rectangle
        :return: a number which stands for the width of the rectangle
        """

    def getNodeHeight(self):
        """
        Calculate the height of the rectangle
        :return: a number which stands for the height of the rectangle
        """

    def getNodeCorners(self):
        """
        Calculate the positions of four corners of this node
        :return: a list of coordinates which stands for the positions of four corners of this node
        """