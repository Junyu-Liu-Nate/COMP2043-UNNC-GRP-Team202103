from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout

# 定义一个路径, 到时候直接传过来
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.pyplot import figure

import overlapDef
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import globalVariable as glv
# 这个界面初始化时候, 顺便设置了plt的canvas的一些基本动作

# class showFigure(QWidget):
#     # sign_showFigure = pyqtSignal()
#
#     def __init__(self):
#         super(QWidget, self).__init__()
#         self.resize(1600, 1000)
#
#         # fig = overlapDef.figureCirc()
#         figIn = plt.gcf()
#         self.canvasThis = FigureCanvas(figIn)
#         self.canvasThis.mpl_connect('scroll_event', lambda event: self.zoomEvent(event, figIn))
#         layoutThis = QVBoxLayout()
#         self.setLayout(layoutThis)
#         layoutThis.addWidget(self.canvasThis)
#
#         self.toolBar = NavigationToolbar(self.canvasThis, self)
#         self.toolBar.hide()
#         self.canvasThis.mpl_connect("button_press_event", self.pan)
#         self.canvasThis.mpl_connect("button_release_event", self.onRelease)
#
#     # 算了搞不懂了
#     # def method_handle_sign(self):
#     #     self.show()
#     #     plt.show()

class setPLT(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        fig = plt.gcf()
        # plt.show()
        canvas = FigureCanvas(fig)
        toolBar = NavigationToolbar(canvas, self)
        toolBar.hide()
        canvas.mpl_connect('scroll_event', self.zoomEvent)
        canvas.mpl_connect("button_press_event", self.pan)
        canvas.mpl_connect("button_release_event", self.onRelease)

    def zoomEvent(self, event):
        axtemp = event.inaxes
        x_min, x_max = axtemp.get_xlim()
        y_min, y_max = axtemp.get_ylim()
        fanwei = (x_max - x_min) / 10
        if event.button == 'up':
            axtemp.set(xlim=(x_min + fanwei, x_max - fanwei))
            axtemp.set(ylim=(y_min + fanwei, y_max - fanwei))
            # print('up')
        elif event.button == 'down':
            axtemp.set(xlim=(x_min - fanwei, x_max + fanwei))
            axtemp.set(ylim=(y_min - fanwei, y_max + fanwei))
            # print('down')
        self.fig.canvas.draw_idle()

    def pan(self, event):
        # if event.button == 1:
        print("pan")
        self.toolBar.pan()
        # if event.button == 3:
        #     print("new widget")
        #     self.method_handle_sign()

    def onRelease(self, event):
        print("release")
        self.canvas.mpl_disconnect(self.canvas.mpl_connect("button_press_event", self.pan))