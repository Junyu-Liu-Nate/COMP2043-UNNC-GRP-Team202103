**GUImain.py**

The main python file to start the program.

------

* def sameSize(w1, w2)

  ```python
  Resize and relocate w2 to w1
  :param w1: the QWidget to offer its size and location
  :param w2: the QWidget needs to resize and relocate
  :return: None
  ```



**EnterPage.py**

The python file to initialize the enter page of the program.

****

* class enterpage(QWidget)

```
The class offers the paradigm of the enter page of the program,
including the original appearance and def calls of functions:
generate random input and show the result page of the program.
Class variables: self.layoutBtnPE helps to resize the spacing
between buttons with the size of enter page window,
sign_toResult helps to change window.
```

class defs are as followings:

* def \__init__(self)

  ```
  The def to initialize the enter page QWidget window
  ```

* def initUI(self)

  ```
  Initialize the main page settings
  :return: None
  ```

* def resizeEvent(self, QResizeEvent)

  ```
  Rewrite the resizeEvent of the QWidget to
  help resize the spacing between buttons
  :param QResizeEvent: Detect the size change of window
  :return: None
  ```

* def click_goRG(self)

  ```
  Pop up the window to generate random input
  :return: None
  ```

* def click_goSR(self)

  ```
  Show the result page and hide enter page
  :return: None
  ```

* def method_handle_sign(self)

  ```
  Handle the signal from ResultPage.py and show enter page
  :return: None
  ```



**ResultPage.py**

The python file to initialize the result page of the program.

---

* class resultPage(QWidget)

  ```
  The class offers the paradigm of the result page of the program,
  including the original overlap result and def calls of functions:
  switch pages of the window to see the difference before and after overlap,
  alter overlap style, zoom and drag the result figure,
  export result image and return the enter page.
  Class variables: self.stackedWidget helps to switch page contents,
  self.btnSR helps to confirm the first page is shown every time result page is shown,
  self.layoutSR, self.figureSR and self.canvasSR help to change the content of show result page,
  self.layoutFB and self.webFB help tp refresh the content of feedback page
  self.patternNum helps to change the alter overlap style,
  self.inputChoice helps to record the available choices of overlap style for one input file,
  self.btnASCub and self.btnASCirc help to deliver alter style information,
  self.toolBar helps to link the figure pan function with the canvas.
  ```

class defs are as followings:

* def \__init__(self)

  ```
  The def to initialize the enter page QWidget window
  ```

* def initUI(self)

  ```
  Initialize the main page settings
  :return: None
  ```

* def resizeEvent(self, a0: QtGui.QResizeEvent) -> None

  ```
  Rewrite the resizeEvent of the QWidget to
  help resize the spacing between buttons
  :param a0: QtGui.QResizeEvent: Detect the size change of window
  :return: None
  ```

* def click_goSR(self)

  ```
  Show the result page
  :return: None
  ```

* def click_goSD(self)

  ```
  Show the show difference page
  :return: None
  ```

* def click_goAS(self)

  ```
  Show the alter style page
  :return: None
  ```

* def click_goFB(self)

  ```
  Show the feedback HTML and refresh it every click
  :return: None
  ```

* def click_goEX(self)

  ```
  Transform the result figure into png and export to local computer
  :return: None
  ```

* def click_goEP(self)

  ```
  Show the enter page and hide result page
  :return: None
  ```

* def method_handle_sign(self)

  ```
  Handle the signal from EnterPage.py and load the result figure
  :return: None
  ```

* def set_styleCub(self)

  ```
  The def called by alter style page Cubes button,
  change the figure of result and images of show difference page,
  or forbid user from changing style
  :return: None
  ```

* def setStyleCirc(self)

  ```
  The def called by alter style page Circles button,
  change the figure of result and images of show difference page
  :return: None
  ```

* def refreshCanvas(self)

  ```
  Refresh the figure of result page and images of show difference page
  :return: None
  ```

* def canvasSetting(self)

  ```
  Set the basic functions of the canvas of result page
  :return: None
  ```

* def zoomEvent(self, event)

  ```
  Zoom in and zoom out functions
  :param event: cursor actions from user
  :return: None
  ```

* def pan(self, event)

  ```
  Drag figure function
  :param event: cursor actions from user
  :return: None
  ```

* def onRelease(self, event)

  ```
  Cancel the functions of zoom and drag of the canvas
  :param event: cursor actions from user
  :return: None
  ```

* def reSizeCanvas(self)

  ```
  Resize the margins of result canvas
  :return: None
  ```



**widgetsCreator.py**

The python file to initialize the partial duplicated QWidgets of the program.

---

* def createBtn(str)

  ```
  Create QPushButton and restrict its size
  :param str: text of button
  :return: created push button
  ```

* def createRadioBtn(str)

  ```
  Create QRadioButton and restrict its size
  :param str: text of button
  :return: created radio button
  ```

* def createToolBtn(str, imgPath)

  ```
  Create QToolButton, add icons and restrict its size
  :param str: text of button
  :param imgPath: path of icon image
  :return: created tool button
  ```

* def createLabPix(str)

  ```
  Create QLabel to display image
  :param str: path of image
  :return: created label
  ```

* def createHTML150()

  ```
  Create QWebEngineView to display HTML information
  :return: HTML with js effects
  ```

* def createHTML200()

  ```
  Create QWebEngineView to display HTML information
  :return: HTML with js effects
  ```

* def createHTML25()

  ```
  Create QWebEngineView to display HTML information
  :return: HTML with js effects
  ```



**overlapDef.py**

The python file to transplant the matplot defs to GUI.

---

* def figurePrint(patternNum)

  ```
  Create before and after overlap images and figure
  :param patternNum: overlap pattern choice
  :return: overlap figure
  ```