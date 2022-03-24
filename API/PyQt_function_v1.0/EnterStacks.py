from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget

# 注意避免循环引用
from widgetsCreator import createBtn, createText


class page0(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        # Page Enter
        # 设置enterPage的Widget
        pageEnter = QWidget()
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



def page1():
    # Page Choose Style
    pageCS = QWidget()
    # layout pageCS
    layoutCS = QVBoxLayout()
    layoutCS.setSpacing(20)
    pageCS.setLayout(layoutCS)

    # 再进一步内部的
    btn2 = createBtn("Finish")
    text2 = createText("NONE")

    layoutCS.addWidget(btn2, 2)
    layoutCS.addWidget(text2, 8)

    return pageCS


# page0 = page0()

def stacksEP(page0):
    stacks = QStackedWidget()
    stacks.addWidget(page0)

    return stacks