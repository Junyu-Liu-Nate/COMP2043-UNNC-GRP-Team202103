    def calNodePosition(overlapNode, startAngle, situationNum):
        """
        Calculate the positions of an overlapNode in pattern 1
        :param overlapNode: stands for an overlapNode object
        :param startAngle: stands for the angle which the drawing starts
        :param situationNum: stands for the number of drawing pattern
        :return: no return
        """

    def calNodePosition2(overlapNode, startAngle, situationNum):
        """
        Calculate the positions of an overlapNode in pattern 2
        :param overlapNode: stands for an overlapNode object
        :param startAngle: stands for the angle which the drawing starts
        :param situationNum: stands for the number of drawing pattern
        :return: no return
        """

    def calPairedPositions(overlapNodePair, initialCenter):
        """
        Calculate the positions of a pair overlapNode in pattern 1
        :param overlapNodePair: stands for a pair of overlapNode object
        :param initialCenter: stands for the initial drawing center of this paired nodes
        :return: no return
        """

    def calPairedPositions2(overlapNodePair, initialCenter):
        """
        Calculate the positions of a pair overlapNode in pattern 2
        :param overlapNodePair: stands for a pair of overlapNode object
        :param initialCenter: stands for the initial drawing center of this paired nodes
        :return:
        """

    def findConnectionNode(overlapNode):
        """
        Helper function to find the connection node in a overlapNode
        Find the connection node
        :param overlapNode: an overlapNode object
        :return: no return
        """

    def calGroupPosition1(overlapGroup, initialCenter):
        """
        Calculate the positions of a group overlapNode in pattern 1
        :param overlapGroup: stands for a pair of overlapNode object
        :param initialCenter: stands for the initial drawing center of this paired nodes
        :return: no return
        """

    def calGroupPosition2(overlapGroup, initialCenter):
        """
        Calculate group positions of a group of overlapNode for PATTERN 2
        :param overlapGroup: stands for a pair of overlapNode object
        :param initialCenter: stands for the initial drawing center of this paired nodes
        :return: no return
        """

    def ifOverlap(pos1, pos2):
        """
        Detect if two rectangles are overlapped according to the postions of these two
        :param pos1: [[X1, Y1], [X2, Y2], [X3, Y3], [X4, Y4]], Left-Up, Left-Down, Right-Up, Right-Down
        :param pos2: [[X1, Y1], [X2, Y2], [X3, Y3], [X4, Y4]], Left-Up, Left-Down, Right-Up, Right-Down
        :return: a boolean which stands for whether the two nodes overlap
        """

    def ifIntersect(ls1, ls2):
        """
        Check whether there is an intersection between two line segments
        :param ls1: stands for line segment, ls1 = ls2 = [[X1, Y1], [X2, Y2]]
        :param ls2: stands for line segment, ls1 = ls2 = [[X1, Y1], [X2, Y2]]
        :return: a boolean which stands for whether there is an intersection between two line segments
        """

    def calEdgePosition(node1, node2):
        """
        Calculate the edge connection positions of two nodes
        :param node1: a node object
        :param node2: a node object
        :return: a pair of coordiantes which stands for the edge connection positions of two nodes
        """

    def calDistance(point1, point2):
        """
        Calculate the distance between two nodes
        :param point1: a coordinate which stand for the position node 1
        :param point2: a coordinate which stand for the position node 2
        :return: a number which stands for the distance between two points
        """

    def findOverlapNode(overlapNodeList, name):
        """
        Find a certain overlapNode from a list
        :param overlapNodeList: a list of overlapNode
        :param name: a string which stands for the name
        :return: return a certain overlapNode from a list
        """

    def calOverlapLayout(graph, patternNum):
        """
        Calculate the layout of a graph
        :param graph: stands for a graph object
        :param patternNum: stands for the drawing pattern number
        :return: no return
        """