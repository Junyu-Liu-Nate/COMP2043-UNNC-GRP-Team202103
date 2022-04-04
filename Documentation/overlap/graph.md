class Graph:

    The Graph class stands for the integration of all nodes

    def __init__(self):
        """
        In the form like: [AB, BC_BH_BF, KL], all Node or OverlapNode objects
        AB, KL stands for separate nodes, while BC_BH_BF stands for a group of overlapped nodes
        AB, KL are Node types, while BC_BH_BF is OverlapNode type which is the subtype of Node
        """

    def readInput(self, fileName, patternNum):
        """
        Read input from file and create corresponding Node and OverlapNode objects
        :param fileName: a string which stands for the name of input file
        :param patternNum: a number which stands for which display pattern to be used
        :return: no return
        """

    def findNode(self, nodeName):
        """
        Find and return Node instance through name
        :param nodeName: a string which stands for the name of the node
        :return: no return
        """

    def getNodeNumber(self):
        """
        Get the number of supernodes
        :return: the number of supernodes
        """

    def getNodeList(self):
        """
        Get the node list of this Graph object
        :return: the node list of this Graph object
        """

    def getEdgeList(self):
        """
        Get the edge list of this Graph object
        :return: the edge list of this Graph object
        """