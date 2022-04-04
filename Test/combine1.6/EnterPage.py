from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal
from widgetsCreator import createBtn, createHTML200, createHTML150, createHTML25

from randomGenerator.main import rgGUI


class enterPage(QWidget):
    """
    The class offers the paradigm of the enter page of the program,
    including the original appearance and def calls of functions:
    generate random input and show the result page of the program.
    Class variables: self.layoutBtnPE helps to resize the spacing
    between buttons with the size of enter page window,
    sign_toResult helps to change window.
    """
    sign_toResult = pyqtSignal()

    def __init__(self):
        """
        The def to initialize the enter page QWidget window
        """
        super(enterPage, self).__init__()
        self.layoutBtnPE = None
        # resize the window
        desktop = QApplication.desktop()
        width = desktop.width()
        height = desktop.height()
        self.resize(int(width / 1.5), int(height / 1.5))
        # set window title
        self.setWindowTitle("OVERLAP")
        # set window icon
        pixIcon = QPixmap("resource/icon.png")
        iconEP = QIcon(pixIcon)
        self.setWindowIcon(iconEP)
        # add CSS styles to the page
        with open("resource/styleSettings.txt", "r") as self.style:
            textOfStyle = self.style.read()
            self.setStyleSheet(textOfStyle)
            self.style.close()
        # initialize more UI members
        self.initUI()

    def initUI(self):
        """
        Initialize the main page settings
        :return: None
        """
        layout = QGridLayout()
        self.setLayout(layout)
        pageEnter = QWidget()
        layout.addWidget(pageEnter)

        """Page Enter"""
        layoutPE = QHBoxLayout()
        pageEnter.setLayout(layoutPE)

        # Set buttons layout and spacing
        self.layoutBtnPE = QVBoxLayout()
        self.layoutBtnPE.setSpacing(20)
        layoutPE.addWidget(createHTML200(), 1000)
        layoutPE.addLayout(self.layoutBtnPE, 1618)
        layoutPE.addWidget(createHTML200(), 1000)

        btnRG = createBtn("Random Generator")
        btnSR = createBtn("Show Result")

        self.layoutBtnPE.addWidget(createHTML150(), 8)
        self.layoutBtnPE.addWidget(btnRG, 2)
        self.layoutBtnPE.addWidget(btnSR, 2)
        self.layoutBtnPE.addWidget(createHTML25(), 1)

        """Button Clicked Effects"""
        btnRG.clicked.connect(self.click_goRG)
        btnSR.clicked.connect(self.click_goSR)

    def resizeEvent(self, QResizeEvent):
        """
        Rewrite the resizeEvent of the QWidget to
        help resize the spacing between buttons
        :param QResizeEvent: Detect the size change of window
        :return: None
        """
        self.layoutBtnPE.setSpacing(self.height()/50)

    def click_goRG(self):
        """
        Pop up the window to generate random input
        :return: None
        """
        rgGUI()

    def click_goSR(self):
        """
        Show the result page and hide enter page
        :return: None
        """
        self.sign_toResult.emit()
        self.hide()

    def method_handle_sign(self):
        """
        Handle the signal from ResultPage.py and show enter page
        :return: None
        """
        self.show()
