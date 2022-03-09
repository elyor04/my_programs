from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QLineEdit)
from PyQt5.QtGui import QFont
from sys import argv, exit
from datetime import datetime

def setParams(obj:QWidget, x:int=None, y:int=None, **kwargs) -> None:
    if "text" in kwargs:
        obj.setText(kwargs["text"])
    if "scale" in kwargs:
        obj.setFont(QFont("Times", kwargs["scale"]))
    if ("width" not in kwargs) or ("height" not in kwargs):
        obj.adjustSize()
    if "width" in kwargs:
        obj.setFixedWidth(kwargs["width"])
    if "height" in kwargs:
        obj.setFixedHeight(kwargs["height"])
    if "color" in kwargs:
        obj.setStyleSheet(f"background: {kwargs['color']}")
    if (x is not None) and (y is not None):
        if kwargs.get("right", False):
            x -= obj.fontMetrics().boundingRect(obj.text()).width()
        if kwargs.get("down", False):
            y -= obj.fontMetrics().boundingRect(obj.text()).height()
        obj.move(x, y)


ilv = QApplication(argv)
oyn = QMainWindow()
oyn.setGeometry(100,100, 550,500)
oyn.setWindowTitle("Yashagan kun")

yzv = QLabel(text="tug\'ilgan kun.oy.yil ni kiriting:", parent=oyn)
krt = QLineEdit(parent=oyn)
setParams(yzv, 80, 10, scale=10)
setParams(krt, 80, 40, width=200, scale=9)

knp = QPushButton(text="hisoblash", parent=oyn)
ntj = QLabel(text="yashagan kuningiz", parent=oyn)
setParams(knp, 80, 90, color="lightgreen", scale=10)
setParams(ntj, 80, 135, color="white", scale=10)

def yashaganKun() -> None:
    bgn = datetime.now()
    sna = krt.text().split('.')
    utgn = datetime(int(sna[2]), int(sna[1]), int(sna[0]))
    b_y = int(bgn.strftime("%Y"))
    u_y = int(utgn.strftime("%Y"))
    kun = (b_y - u_y) * 365 + (int(bgn.strftime("%j")) - int(utgn.strftime("%j")))
    for i in range(u_y, b_y):
        if i % 4 == 0: kun += 1
    setParams(ntj, text=f"{kun} kun yashagansiz", color="lightblue")

knp.clicked.connect(yashaganKun)

oyn.show()
exit(ilv.exec_())
