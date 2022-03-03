# 没有第二个界面的用户输入方法，但是按钮太多了，需要删改

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtCore import Qt, pyqtSignal
import sys

### 第一个用户刚进入的界面
import overlapDemo

class EnterApp(QWidget):
    sign_toResult = pyqtSignal()

    def __init__(self):
        super(QWidget, self).__init__()
        self.resize(1000, 800)
        self.setWindowTitle("OVERLAP")

        icon_pixmap = QPixmap("icon.png")
        icon_image = QIcon(icon_pixmap)
        self.setWindowIcon(icon_image)

        # Style Sheet 换主题颜色
        self.setStyleSheet("QWidget{\
                	                        background-color: rgb(253, 253, 253);\
                                            }\
                                            QWidget#centralWidget{\
                	                        border-top:1px solid gray;\
                                            }\
                                            QPushButton{\
                	                        background-color: rgb(250, 250, 250);\
                	                        border:1px solid gray; border-radius:5px;\
                                            }\
                                            QPushButton:hover{\
                	                        background-color: rgb(245, 245, 245);\
                	                        border:1px solid gray; border-radius:5px;\
                                            }\
                                            QPushButton:pressed{\
                	                        background-color: rgb(240, 240, 240);\
                	                        border:1px solid gray; border-radius:5px;\
                                            }\
                                            QRadioButton{\
                	                        border:1px solid gray; border-radius:5px;\
                                            }")

        self.initUI()

    def initUI(self):
        # 嵌套的逻辑一定要清楚
        # 这个layout时EnterApp最外层的Layout
        layout = QGridLayout()

        # 设置QStackedWidget
        self.stackedWidget = QStackedWidget()
        layout.addWidget(self.stackedWidget)

        ### Enter Page 登入界面
        pageEnter = QWidget()
        layoutEnter = QGridLayout()
        pageEnter.setLayout(layoutEnter)
        self.stackedWidget.addWidget(pageEnter)  # index = 0

        for i in range(3):
            frame = QFrame(self)
            layoutEnter.addWidget(frame, 0, i)
        for i in range(3):
            frame = QFrame(self)
            layoutEnter.addWidget(frame, 1, i)

        # 按钮的layout
        enterButtonLayout = QVBoxLayout()
        layoutEnter.addLayout(enterButtonLayout, 1, 1)
        # 按钮设置
        btnCS = QPushButton("Choose style")
        btnCS.setMinimumHeight(80)
        enterButtonLayout.addWidget(btnCS)
        btnRI = QPushButton("Random Input")
        btnRI.setMinimumHeight(80)
        enterButtonLayout.addWidget(btnRI)
        btnMI = QPushButton("Manual Input")
        btnMI.setMinimumHeight(80)
        enterButtonLayout.addWidget(btnMI)
        btnSR = QPushButton("Show Result")
        btnSR.setMinimumHeight(80)
        enterButtonLayout.addWidget(btnSR)

        # 几个多次使用的控件，不能共用
        # btnRe = QPushButton("Finish")
        # btnRe.setMinimumHeight(80)
        # frameOcy = QFrame()  # 占位frame

        ### Choose Style 选择overlap样式
        pageCS = QWidget()
        layoutCS = QGridLayout()
        pageCS.setLayout(layoutCS)
        self.stackedWidget.addWidget(pageCS)  # index = 1

        btnCSRe = QPushButton("Finish")
        btnCSRe.setMinimumHeight(80)
        layoutCS.addWidget(btnCSRe, 0, 0, 1, 1)
        frameCSOcy = QFrame()  # 占位frame
        layoutCS.addWidget(frameCSOcy, 0, 1, 1, 1)

        ########################################################################################################
        # btnCS1 = QRadioButton("Cubes")
        # btnCS1.setStyleSheet("image: url(cubes.png);")
        ### import overlapDemo 会直接把界面撑大
        btnCS1 = QRadioButton("From overlapDemo")
        img = overlapDemo.plt.gcf()
        img.savefig("overlap.png")
        btnCS1.setStyleSheet("image: url(overlap.png);")
        ########################################################################################################
        btnCS1.setMinimumHeight(650)
        btnCS1.setChecked(1)  # 设置默认checked
        layoutCS.addWidget(btnCS1, 1, 0, 1, 1)
        btnCS2 = QRadioButton("Circles")
        btnCS2.setStyleSheet("image: url(circles.png);")
        btnCS2.setMinimumHeight(650)
        layoutCS.addWidget(btnCS2, 1, 1, 1, 1)

        ### Random Input 电脑随机输入界面
        pageRI = QWidget()
        layoutRI = QGridLayout()
        pageRI.setLayout(layoutRI)
        self.stackedWidget.addWidget(pageRI)  # index = 2

        btnRIRe = QPushButton("Finish")
        btnRIRe.setMinimumHeight(80)
        layoutRI.addWidget(btnRIRe, 0, 0, 1, 1)
        frameRIOcy = QFrame()  # 占位frame
        layoutRI.addWidget(frameRIOcy, 0, 1, 1, 1)

        # 读文件，写文件在下面的def returnEnter
        # 这里的逻辑要注意
        self.textRI = QPlainTextEdit()
        with open("input.txt", "r") as self.f:
            textOfRI = self.f.read()
            self.textRI.setPlainText(textOfRI)
            self.f.close()
        self.textRI.setMinimumSize(900, 650)
        layoutRI.addWidget(self.textRI, 1, 0, 1, 2)
        self.f.close()

        ### Manual Input 用户自由输入界面
        pageMI = QWidget()
        layoutMI = QGridLayout()
        pageMI.setLayout(layoutMI)
        self.stackedWidget.addWidget(pageMI)  # index = 3

        btnMIRe = QPushButton("Finish")
        btnMIRe.setMinimumHeight(80)
        layoutMI.addWidget(btnMIRe, 0, 0, 1, 1)
        frameMIOcy = QFrame()  # 占位frame
        layoutRI.addWidget(frameMIOcy, 0, 1, 1, 1)

        # 读文件，写文件在下面的def returnEnter
        self.textMI = QPlainTextEdit("Standard shows here")
        self.textMI.setMinimumSize(900, 650)
        layoutMI.addWidget(self.textMI, 1, 0, 1, 2)

        # self最终的加入layout
        self.setLayout(layout)

        # 按钮事件
        btnCSRe.clicked.connect(self.click_goEnter)
        btnRIRe.clicked.connect(self.click_RIgoEnter)
        btnMIRe.clicked.connect(self.click_MIgoEnter)
        btnCS.clicked.connect(self.click_goCS)
        btnRI.clicked.connect(self.click_goRI)
        btnMI.clicked.connect(self.click_goMI)
        btnSR.clicked.connect(self.click_goSR)

    def click_goEnter(self):
        # 前面的stackedWidget不加self，这里就找不到stackedWidget
        self.stackedWidget.setCurrentIndex(0)
        # 这样不行，变成了后面再加
        # with open("input.txt", "w") as self.f:
        #     self.f.write(self.textRI.toPlainText())
        #     self.f.write(self.textMI.toPlainText())

    def click_RIgoEnter(self):
        self.stackedWidget.setCurrentIndex(0)
        with open("input.txt", "w") as self.f:
            self.f.write(self.textRI.toPlainText())
            self.f.close()

    def click_MIgoEnter(self):
        self.stackedWidget.setCurrentIndex(0)
        with open("input.txt", "w") as self.f:
            self.f.write(self.textMI.toPlainText())
            self.f.close()

    def click_goCS(self):
        self.stackedWidget.setCurrentIndex(1)

    def click_goRI(self):
        self.stackedWidget.setCurrentIndex(2)

    def click_goMI(self):
        self.stackedWidget.setCurrentIndex(3)

    def click_goSR(self):
        self.sign_toResult.emit()
        self.hide()

### 第二个展示结果的界面
class ShowResult(QWidget):
    def __init__(self):
        super(ShowResult, self).__init__()
        self.resize(1000, 800)
        self.setWindowTitle("OVERLAP")

        icon_pixmap = QPixmap("icon.png")
        icon_image = QIcon(icon_pixmap)
        self.setWindowIcon(icon_image)

        # Style Sheet 换主题颜色
        self.setStyleSheet("QWidget{\
                        	                        background-color: rgb(253, 253, 253);\
                                                    }\
                                                    QWidget#centralWidget{\
                        	                        border-top:1px solid gray;\
                                                    }\
                                                    QPushButton{\
                        	                        background-color: rgb(250, 250, 250);\
                        	                        border:1px solid gray; border-radius:5px;\
                                                    }\
                                                    QPushButton:hover{\
                        	                        background-color: rgb(245, 245, 245);\
                        	                        border:1px solid gray; border-radius:5px;\
                                                    }\
                                                    QPushButton:pressed{\
                        	                        background-color: rgb(240, 240, 240);\
                        	                        border:1px solid gray; border-radius:5px;\
                                                    }\
                                                    QRadioButton{\
                        	                        border:1px solid gray; border-radius:5px;\
                                                    }")

        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        ### 最上面一排按钮
        layoutBtn = QHBoxLayout()
        layout.addLayout(layoutBtn, 0, 0)
        btnSD = QPushButton("Show DIFF")
        btnSD.setMinimumHeight(80)
        layoutBtn.addWidget(btnSD)
        btnAS = QPushButton("Alter Style")
        btnAS.setMinimumHeight(80)
        layoutBtn.addWidget(btnAS)
        btnSR = QPushButton("Show Result")
        btnSR.setMinimumHeight(80)
        layoutBtn.addWidget(btnSR)
        btnFB = QPushButton("Feedback")
        btnFB.setMinimumHeight(80)
        layoutBtn.addWidget(btnFB)
        btnEP = QPushButton("Export")
        btnEP.setMinimumHeight(80)
        layoutBtn.addWidget(btnEP)

        # 下面一排stackedWidget
        self.stackedWidget = QStackedWidget()
        layout.addWidget(self.stackedWidget, 1, 0)

        ### 第一个界面 Show Result，为了比较人性化的顺序？
        pageSR = QWidget()
        layoutSR = QHBoxLayout()
        pageSR.setLayout(layoutSR)
        self.stackedWidget.addWidget(pageSR)

        framSR = QFrame()
        framSR.setStyleSheet("image: url(cubes.png);")
        framSR.setMinimumHeight(650)
        layoutSR.addWidget(framSR)

        ### 第二个界面 Show DIFF
        pageSD = QWidget()
        layoutSD = QHBoxLayout()
        pageSD.setLayout(layoutSD)
        self.stackedWidget.addWidget(pageSD)

        # 图 + 标签
        layoutSD1 = QVBoxLayout()
        layoutSD.addLayout(layoutSD1)
        framSD1 = QFrame()
        framSD1.setStyleSheet("image: url(cubes.png);")
        framSD1.setMinimumHeight(500)
        layoutSD1.addWidget(framSD1)
        labelSD1 = QLabel("Before")
        layoutSD1.addWidget(labelSD1)
        labelSD1.setAlignment(Qt.AlignTop)  # 设置间距，貌似没什么用

        layoutSD2 = QVBoxLayout()
        layoutSD.addLayout(layoutSD2)
        framSD2 = QFrame()
        framSD2.setStyleSheet("image: url(circles.png);")
        framSD2.setMinimumHeight(500)
        layoutSD2.addWidget(framSD2)
        labelSD2 = QLabel("After")
        layoutSD2.addWidget(labelSD2)
        labelSD2.setAlignment(Qt.AlignTop)

        ### 第三个界面 Alter Style
        pageAS = QWidget()
        layoutAS = QHBoxLayout()
        pageAS.setLayout(layoutAS)
        self.stackedWidget.addWidget(pageAS)

        # 俩RadioButton换overlap style
        rbtnAS1 = QRadioButton("Cubes")
        rbtnAS1.setStyleSheet("image: url(cubes.png);")
        rbtnAS1.setMinimumHeight(650)
        rbtnAS1.setChecked(1)  # 设置默认checked，这里要和前面的选择相同，要换sign
        layoutAS.addWidget(rbtnAS1)
        rbtnAS2 = QRadioButton("Circles")
        rbtnAS2.setStyleSheet("image: url(circles.png);")
        rbtnAS2.setMinimumHeight(650)
        layoutAS.addWidget(rbtnAS2)



        ### 第四个界面 Feedback
        pageFB = QWidget()
        layoutFB = QVBoxLayout()
        pageFB.setLayout(layoutFB)
        self.stackedWidget.addWidget(pageFB)

        # 一个单选题，最后一个是填空
        labelFB1 = QLabel("Question 1: ")
        layoutFB.addWidget(labelFB1)  # 选项开头的文本
        layoutRBtn1 = QHBoxLayout()
        layoutFB.addLayout(layoutRBtn1)  # 几个选项
        rbtnFB1 = QRadioButton("choice one")
        layoutRBtn1.addWidget(rbtnFB1)
        rbtnFB2 = QRadioButton("choice two")
        layoutRBtn1.addWidget(rbtnFB2)
        rbtnFB3 = QRadioButton("choice three")
        layoutRBtn1.addWidget(rbtnFB3)
        # 看一下能不能用
        rbtnFB4 = QRadioButton()
        layoutFB4 = QHBoxLayout()
        textFB4 = QPlainTextEdit("Type here")
        layoutFB4.addWidget(textFB4)
        rbtnFB4.setLayout(layoutFB4)
        layoutRBtn1.addWidget(rbtnFB4)

        # 一个答题
        labelFB2 = QLabel("Question 2: ")
        layoutFB.addWidget(labelFB2)
        textFB2 = QPlainTextEdit("Type here")
        layoutFB.addWidget(textFB2)


        self.setLayout(layout)


        # 按钮事件
        # 这里不能在函数后加括号，会报错
        btnSR.clicked.connect(self.click_goRS)
        btnSD.clicked.connect(self.click_goSD)
        btnAS.clicked.connect(self.click_goAS)
        btnFB.clicked.connect(self.click_goFB)
        btnEP.clicked.connect(self.click_export)

    def click_goRS(self):
        self.stackedWidget.setCurrentIndex(0)

    def click_goSD(self):
        self.stackedWidget.setCurrentIndex(1)

    def click_goAS(self):
        self.stackedWidget.setCurrentIndex(2)

    def click_goFB(self):
        self.stackedWidget.setCurrentIndex(3)

    def click_export(self):
        # 保存图片
        fd, fp = QFileDialog.getSaveFileName(self.stackedWidget, "save file", "", "*.png;;All Files(*)")
        image = QImage('cubes.png')
        image.save(fd)

        # 直接保存图片，不会弹出框
        # image.save('overlap.png', 'PNG')

        # 保存txt文件等用，write的para是str
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # fileName, _ = QFileDialog.getSaveFileName(self, 'save file', 'overlap.png', 'All Files (*)', options = options)
        # if fileName:
        #     with open(fileName, "wb") as f:
        #         f.write(QImage('cubes.png'))

        # 提供报错信息
        # Run -> Edit Configurations.. -> Emulate terminal in output console

    # 接class EnterApp的signal
    def method_handle_sign(self):
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    enter = EnterApp()
    showResult = ShowResult()

    enter.sign_toResult.connect(showResult.method_handle_sign)

    enter.show()

    sys.exit(app.exec_())
