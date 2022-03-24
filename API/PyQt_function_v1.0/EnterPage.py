from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal
from matplotlib import pyplot as plt

from ResultPage import resultPage
import overlapDef
from widgetsCreator import createBtn, createText, createRadioBtn, createLabPix

import globalVariable as glv
glv._init()



# 改单击拖动，双击打开新窗口
class enterPage(QWidget):
    # 一个可以转换QWidget的信号
    sign_toResult = pyqtSignal()  # 定义为类属性, 不要放进__init__

    def __init__(self):
        super(QWidget, self).__init__()
        # 调整窗口大小
        self.resize(1600, 1000)
        # 窗口名
        self.setWindowTitle("OVRELAP")
        # 窗口图标
        pixIcon = QPixmap("resource/icon.png")
        iconEP = QIcon(pixIcon)  # icon for Enter Page
        self.setWindowIcon(iconEP)

        # 加载更多UI
        self.initUI()

    def initUI(self):
        # 给界面设置基础layout: GridLayout
        layout = QGridLayout()
        self.setLayout(layout)

        # 设置堆部件: StackedWidget
        # 便于接下来设置界面切换: setCurrentIndex(n)
        self.stackedWidget = QStackedWidget()
        layout.addWidget(self.stackedWidget)
        pageEnter = QWidget()
        pageCS = QWidget()
        pageRI = QWidget()
        pageMI = QWidget()
        self.stackedWidget.addWidget(pageEnter)  # index = 0
        self.stackedWidget.addWidget(pageCS)  # index = 1
        self.stackedWidget.addWidget(pageRI)  # index = 2
        self.stackedWidget.addWidget(pageMI)  # index = 3

        """Page Enter"""
        # 设置enterPage的Widget
        # layout pageEnter
        layoutPE = QHBoxLayout()
        pageEnter.setLayout(layoutPE)

        # Enter Page的按钮
        layoutBtnPE = QVBoxLayout()
        layoutBtnPE.setSpacing(20)  # 控件间的间隔
        layoutPE.addStretch(1)
        layoutPE.addLayout(layoutBtnPE, 2)  # addLayout(layout, stretch)
        layoutPE.addStretch(1)

        btnCS = createBtn("Choose Style")
        btnRI = createBtn("Random Input")
        btnMI = createBtn("Manual Input")
        btnSR = createBtn("Show Result")

        layoutBtnPE.addStretch(8)
        layoutBtnPE.addWidget(btnCS, 2)
        layoutBtnPE.addWidget(btnRI, 2)
        layoutBtnPE.addWidget(btnMI, 2)
        layoutBtnPE.addWidget(btnSR, 2)
        layoutBtnPE.addStretch(1)

        """Page Choose Style"""
        # layout pageCS
        layoutCS = QVBoxLayout()
        layoutCS.setSpacing(20)
        pageCS.setLayout(layoutCS)

        # 进一步内部的
        btnCSRe = createBtn("Finish")

        layoutCSRe = QHBoxLayout()
        layoutCSRe.addWidget(btnCSRe, 1)
        layoutCSRe.addStretch(3)
        layoutCS.addLayout(layoutCSRe, 1)

        # 一些图相关
        layoutCSOps = QHBoxLayout()
        layoutCS.addLayout(layoutCSOps, 3)
        layoutCSCub = QVBoxLayout()  # 本layout包括canvas承载figure与radioButton
        layoutCSCirc = QVBoxLayout()
        layoutCSOps.addLayout(layoutCSCub, 1)
        layoutCSOps.addLayout(layoutCSCirc, 1)

        self.btnCSCub = createRadioBtn("Cubes")
        self.btnCSCirc = createRadioBtn("Circles")
        self.btnCSCirc.setChecked(True)
        # 不要这样, 在下面写新的函数来设置
        if(self.btnCSCub.isChecked()):
            glv.set("cub", "true")
        else:
            glv.set("cub", "false")
        if(self.btnCSCirc.isChecked()):
            glv.set("circ", "true")
        else:
            glv.set("circ", "false")

        canvasCSCub = createLabPix("resource/cubes.png")
        canvasCSCirc = createLabPix("resource/circles.png")

        layoutCSCub.addWidget(canvasCSCub, 3)
        layoutCSCub.addWidget(self.btnCSCub, 1)
        layoutCSCirc.addWidget(canvasCSCirc, 3)
        layoutCSCirc.addWidget(self.btnCSCirc, 1)

        """Page Random Input"""
        # layout pageRI
        layoutRI = QVBoxLayout()
        layoutRI.setSpacing(20)
        pageRI.setLayout(layoutRI)

        # 再进一步内部的
        btnRIRe = createBtn("Finish")
        textRI = createText("NONE")

        layoutRIRe = QHBoxLayout()
        layoutRIRe.addWidget(btnRIRe, 1)
        layoutRIRe.addStretch(3)
        layoutRI.addLayout(layoutRIRe, 1)  # 注意大小写

        layoutRIText = QHBoxLayout()
        layoutRIText.addStretch(1)
        layoutRIText.addWidget(textRI, 4)
        layoutRI.addLayout(layoutRIText, 3)

        """Page Manual Input"""
        # layout pageMI
        layoutMI = QVBoxLayout()
        layoutMI.setSpacing(20)
        pageMI.setLayout(layoutMI)

        # 再进一步内部的
        btnMIRe = createBtn("Finish")
        textMI = createText("NONE")

        layoutMIRe = QHBoxLayout()
        layoutMIRe.addWidget(btnMIRe, 1)
        layoutMIRe.addStretch(3)
        layoutMI.addLayout(layoutMIRe, 1)  # 注意大小写

        layoutMIText = QHBoxLayout()
        layoutMIText.addStretch(1)
        layoutMIText.addWidget(textMI, 4)
        layoutMI.addLayout(layoutMIText, 3)

        """Button Clicked Effects"""
        btnCS.clicked.connect(self.click_goCS)  # 这里不能要()
        btnCSRe.clicked.connect(self.click_goEnter)
        btnRI.clicked.connect(self.click_goRI)
        btnRIRe.clicked.connect(self.click_goEnter)
        btnMI.clicked.connect(self.click_goMI)
        btnMIRe.clicked.connect(self.click_goEnter)
        btnSR.clicked.connect(self.click_goSR)

        """radioButton Checked Effects"""
        self.btnCSCub.toggled.connect(self.set_globalCub)
        self.btnCSCirc.toggled.connect(self.set_globalCirc)

        # """enter"""
        # self.result = resultPage()

    """Methods for Change StackedPages"""
    def click_goEnter(self):
        self.stackedWidget.setCurrentIndex(0)

    def click_goCS(self):
        self.stackedWidget.setCurrentIndex(1)

    def click_goRI(self):
        self.stackedWidget.setCurrentIndex(2)

    def click_goMI(self):
        self.stackedWidget.setCurrentIndex(3)

    def set_globalCub(self):
        # plt.close()
        plt.clf()
        if self.btnCSCub.isChecked():
            glv.set("cub", "true")
            overlapDef.figureCub()
            QApplication.processEvents()
        else:
            glv.set("cub", "false")

    def set_globalCirc(self):
        # plt.close()
        plt.clf()
        if self.btnCSCirc.isChecked():
            glv.set("circ", "true")
            overlapDef.figureCirc()
            QApplication.processEvents()
            # plt.show()
        else:
            glv.set("circ", "false")

    # def show_fullScreen(self, event):  # event不能少
    #     self.sign_showFigure.emit()  # 这次没有self.hide()

    def click_goSR(self):
        self.sign_toResult.emit()  # emit发射信号
        self.hide()
        # self.sign_toResult.connect(self.result.method_handle_sign)

    def method_handle_sign(self):  # 接收信号, main中使用connect
        self.show()
