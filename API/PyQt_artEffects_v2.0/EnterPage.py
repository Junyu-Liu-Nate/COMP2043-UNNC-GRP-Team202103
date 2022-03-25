import PyQt5.Qt
from PyQt5 import Qt, QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal, QFileInfo, QUrl
from matplotlib import pyplot as plt

from ResultPage import resultPage
import overlapDef
from widgetsCreator import createBtn, createText, createRadioBtn, createLabPix, createHTML50, createHTML200, \
    createHTML150, createHTML25

from PyQt5.QtCore import Qt

import globalVariable as glv
glv._init()


# 改单击拖动，双击打开新窗口
class enterPage(QWidget):
    # 一个可以转换QWidget的信号
    sign_toResult = pyqtSignal()  # 定义为类属性, 不要放进__init__

    def __init__(self):
        super(enterPage, self).__init__()
        # 调整窗口大小
        self.resize(1600, 1200)
        # 窗口名
        self.setWindowTitle("OVRELAP")
        # 窗口图标
        pixIcon = QPixmap("resource/icon.png")
        iconEP = QIcon(pixIcon)  # icon for Enter Page
        self.setWindowIcon(iconEP)
        # 美化界面
        with open("resource/styleSettings.txt", "r") as self.style:
            textOfStyle = self.style.read()
            self.setStyleSheet(textOfStyle)
            self.style.close()
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
        self.layoutBtnPE = QVBoxLayout()
        self.layoutBtnPE.setSpacing(20)  # 控件间的间隔
        # layoutPE.addStretch(1000)
        layoutPE.addWidget(createHTML200(), 1000)
        layoutPE.addLayout(self.layoutBtnPE, 1618)  # addLayout(layout, stretch)
        # layoutPE.addStretch(1000)
        layoutPE.addWidget(createHTML200(), 1000)

        btnCS = createBtn("Choose Style")
        btnRI = createBtn("Random Input")
        btnMI = createBtn("Manual Input")
        btnSR = createBtn("Show Result")

        # self.layoutBtnPE.addStretch(8)
        self.layoutBtnPE.addWidget(createHTML150(), 8)
        self.layoutBtnPE.addWidget(btnCS, 2)
        self.layoutBtnPE.addWidget(btnRI, 2)
        self.layoutBtnPE.addWidget(btnMI, 2)
        self.layoutBtnPE.addWidget(btnSR, 2)
        # self.layoutBtnPE.addStretch(1)
        self.layoutBtnPE.addWidget(createHTML25(), 1)

        """Page Choose Style"""
        # layout pageCS
        self.layoutCS = QVBoxLayout()
        self.layoutCS.setSpacing(20)
        # self.layoutCS.setAlignment(QtCore.Qt.AlignCenter)
        pageCS.setLayout(self.layoutCS)

        # 进一步内部的
        btnCSRe = createBtn("Finish")

        layoutCSRe = QHBoxLayout()
        layoutCSRe.addWidget(btnCSRe, 100)
        layoutCSRe.addStretch(424)
        self.layoutCS.addLayout(layoutCSRe, 100)

        # 一些图相关
        layoutCSOps = QHBoxLayout()
        self.layoutCS.addLayout(layoutCSOps, 1108)
        layoutCSCub = QVBoxLayout()  # 本layout包括canvas承载figure与radioButton
        layoutCSCirc = QVBoxLayout()
        layoutCSOps.addLayout(layoutCSCub, 1)
        layoutCSOps.addLayout(layoutCSCirc, 1)

        self.btnCSCub = createRadioBtn("Cubes")
        self.btnCSCirc = createRadioBtn("Circles")
        self.btnCSCirc.setChecked(True)  # 默认使用circ
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
        self.layoutRI = QVBoxLayout()
        self.layoutRI.setSpacing(20)
        pageRI.setLayout(self.layoutRI)

        # 再进一步内部的
        btnRIRe = createBtn("Finish")
        with open("resource/sample_input.txt", "r") as self.RGenerator:
            textOfRI = self.RGenerator.read()
            textRI = createText(textOfRI)
            self.RGenerator.close()
        # textRI = createText("NONE")

        layoutRIRe = QHBoxLayout()
        layoutRIRe.addWidget(btnRIRe, 100)
        layoutRIRe.addStretch(424)
        self.layoutRI.addLayout(layoutRIRe, 100)  # 注意大小写

        layoutRIText = QHBoxLayout()
        layoutRIText.addStretch(100)
        layoutRIText.addWidget(textRI, 1108)
        self.layoutRI.addLayout(layoutRIText, 1108)

        """Page Manual Input"""
        # layout pageMI
        self.layoutMI = QVBoxLayout()
        self.layoutMI.setSpacing(20)
        pageMI.setLayout(self.layoutMI)

        # 再进一步内部的
        btnMIRe = createBtn("Finish")
        textMI = createText("NONE")

        layoutMIRe = QHBoxLayout()
        layoutMIRe.addWidget(btnMIRe, 100)
        layoutMIRe.addStretch(424)
        self.layoutMI.addLayout(layoutMIRe, 100)  # 注意大小写

        layoutMIText = QHBoxLayout()
        layoutMIText.addStretch(100)
        layoutMIText.addWidget(textMI, 1108)
        self.layoutMI.addLayout(layoutMIText, 1108)

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
    """重写窗口resizeEvent"""
    def resizeEvent(self, QResizeEvent):
        self.layoutBtnPE.setSpacing(self.stackedWidget.height()/50)
        self.layoutCS.setSpacing(self.stackedWidget.height()/50)
        self.layoutRI.setSpacing(self.stackedWidget.height()/50)
        self.layoutMI.setSpacing(self.stackedWidget.height()/50)

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
        # plt.clf()
        if self.btnCSCub.isChecked():
            glv.set("cub", "true")
            overlapDef.figureCub()
            QApplication.processEvents()
        else:
            glv.set("cub", "false")

    def set_globalCirc(self):
        # plt.clf()
        if self.btnCSCirc.isChecked():
            glv.set("circ", "true")
            overlapDef.figureCirc()
            QApplication.processEvents()
        else:
            glv.set("circ", "false")

    def click_goSR(self):
        self.sign_toResult.emit()  # emit发射信号
        self.hide()

    def method_handle_sign(self):  # 接收信号, main中使用connect
        self.show()
