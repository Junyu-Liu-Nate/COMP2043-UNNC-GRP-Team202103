from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.pyplot import figure


class forTest(QWidget):
    signalTest = pyqtSignal()

    def __init__(self):
        super(forTest, self).__init__()
        canvas = FigureCanvas(figure(facecolor="blue"))
        self.cid = canvas.mpl_connect('button_press_event', self.one)
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(canvas)

    def one(self, event):
        self.signalTest.emit()
        print("emit()")