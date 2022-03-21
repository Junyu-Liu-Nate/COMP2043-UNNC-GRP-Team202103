from PyQt5.QtWidgets import QWidget, QVBoxLayout

# 定义一个路径, 到时候直接传过来
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from overlap import overlapPatten


class showFigure(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()

        canvasThis = FigureCanvas(overlapPatten.plt.gcf())
        layoutThis = QVBoxLayout()
        self.setLayout(layoutThis)
        layoutThis.addWidget(canvasThis)

    def method_handle_sign(self):
        self.show()
        overlapPatten.plt.show()