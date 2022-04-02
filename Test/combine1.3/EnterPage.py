from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal, QFileInfo, QUrl

from widgetsCreator import createBtn, createText, createRadioBtn, createLabPix, createHTML50, createHTML200, \
    createHTML150, createHTML25


from randomGenerator.main import rgGUI


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
        pageRG = QWidget()
        self.stackedWidget.addWidget(pageEnter)  # index = 0
        self.stackedWidget.addWidget(pageRG)  # index = 1

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

        # btnCS = createBtn("Choose Style")
        # btnRI = createBtn("Random Input")
        # btnMI = createBtn("Manual Input")
        btnRG = createBtn("Random Generator")
        btnSR = createBtn("Show Result")

        # self.layoutBtnPE.addStretch(8)
        self.layoutBtnPE.addWidget(createHTML150(), 8)
        self.layoutBtnPE.addWidget(btnRG, 2)
        self.layoutBtnPE.addWidget(btnSR, 2)
        # self.layoutBtnPE.addStretch(1)
        self.layoutBtnPE.addWidget(createHTML25(), 1)

        '''Page Random Generator'''
        layoutRG = QHBoxLayout()
        pageRG.setLayout(layoutRG)

        btnGS = createBtn("Generate Random Seed")
        btnGI = createBtn("Generate Random Input")
        # label =

        """Button Clicked Effects"""
        btnRG.clicked.connect(self.click_goRG)
        btnSR.clicked.connect(self.click_goSR)

        """radioButton Checked Effects"""
        # self.btnCSCub.toggled.connect(self.set_globalCub)
        # self.btnCSCirc.toggled.connect(self.set_globalCirc)

        # """enter"""
        # self.result = resultPage()
    """重写窗口resizeEvent"""
    def resizeEvent(self, QResizeEvent):
        self.layoutBtnPE.setSpacing(self.stackedWidget.height()/50)

    """Methods for Change StackedPages"""
    def click_goEnter(self):
        self.stackedWidget.setCurrentIndex(0)

    def click_goRG(self):
        rgGUI()
        #self.stackedWidget.setCurrentIndex(1)

    def click_goSR(self):
        self.sign_toResult.emit()  # emit发射信号

        self.hide()

    def method_handle_sign(self):  # 接收信号, main中使用connect
        self.show()
