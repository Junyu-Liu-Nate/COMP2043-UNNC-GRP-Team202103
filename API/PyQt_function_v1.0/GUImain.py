import sys
from time import sleep

from PyQt5.QtWidgets import QApplication, QDesktopWidget
from matplotlib import pyplot as plt

from EnterPage import enterPage
from ResultPage import resultPage
from canvasSetting import setPLT



if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 一开始三个就全部初始化完成了, 所以无法显示最后的
    # 有一些按钮必须要刷新result page
    enter = enterPage()
    # runlater
    result = resultPage()

    # plt.show()
    # show = setPLT()  # 呃呃不初始化第二个界面就进不去

    # 也许这些东西不该在这里写?
    enter.sign_toResult.connect(result.method_handle_sign)  # 不要加括号
    result.sign_toEnter.connect(enter.method_handle_sign)
    # show.sign_showFigure.connect(show.method_handle_sign)  # 展示大图, 不要找错爹了...

    enter.show()

    # 设置窗口位置相同


    # result.move(1000, 1000)

    sys.exit(app.exec_())

