import sys

from PyQt5.QtWidgets import QApplication

from EnterPage import enterPage
from ResultPage import resultPage

def sameSize(w1, w2):
    """
    Resize and relocate w2 to w1
    :param w1: the QWidget to offer its size and location
    :param w2: the QWidget needs to resize and relocate
    :return: None
    """
    w2.move(w1.x(), w1.y())
    w2.resize(w1.width(), w1.height())

if __name__ == "__main__":
    """
    The main function to start the program
    """
    app = QApplication(sys.argv)

    enter = enterPage()
    result = resultPage()

    enter.sign_toResult.connect(result.method_handle_sign)  # 不要加括号
    result.sign_toEnter.connect(enter.method_handle_sign)


    enter.show()

    # 窗口显示位置与大小可以相同
    enter.sign_toResult.connect(lambda: sameSize(enter, result))
    result.sign_toEnter.connect(lambda: sameSize(result, enter))

    sys.exit(app.exec_())


