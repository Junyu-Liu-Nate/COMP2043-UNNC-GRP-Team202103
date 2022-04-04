    def drawLiteralOriginal(node):
        """
        Original drawing function of literals
        :param node: stands for a node object
        :return: no return
        """

    def drawLiteral(node, zoomratio):
        """
        More complex drawing function of literals
        Note that [-6,-6] corresponds to font size 16; and the ratio of main character and suffix is 1.6:1
        :param node: stands for a node object
        :param zoomratio: stands for the zoom ratio of the draw literals
        :return: no return
        """

    def drawRectangle(node, axis):
        """
        Drawing function of a rectangle cover
        :param node: stands for a node object
        :param axis: stands for an axis to be drawn
        :return: no return
        """

    def drawPoint(node, axis):
        """
        Drawing function of a point
        :param node: stands for a node object
        :param axis: stands for an axis to be drawn
        :return: no return
        """

    def drawEdge(node1, node2):
        """
        Drawing function of an edge
        Automatic connect the nearest two points to avoid edge-node crossover.
        :param node1: stand for the nodes which this edge connect
        :param node2: stand for the nodes which this edge connect
        :return: no return
        """

    def drawArc(center, radius, rotateAngle, axis):
        """
        Drawing function of an Arc
        :param center: stands for the circle center from which the Arc is drawn
        :param radius: stands for the circle radius from which the Arc is drawn
        :param rotateAngle: stands for the circle radius from which the Arc is drawn
        :param axis: stands for the axis where the Arc is drawn
        :return: no return
        """

    def drawArcCombo(center, radius, rotateAngle, node, axis, zoomRatio):
        """
        Drawing function of an Arc and rectangle combination
        :param center: stands for the circle center from which the Arc and rectangle combination is drawn
        :param radius: radius stands for the circle radius from which the Arc is drawn
        :param rotateAngle: rotateAngle stands for the circle radius from which the Arc is drawn
        :param node: stands for a node object
        :param axis: stands for the axis where the Arc is drawn
        :param zoomRatio: stands for the zoom ratio of the literals to be drawn
        :return: no return
        """

    def calDistance(point1, point2):
        """
        Calculate the distance bewteen two points
        :param point1: the coordiante of point 1
        :param point2: the coordiante of point 2
        :return: a number which stands for the distance between two points
        """