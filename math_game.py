from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PyQt5.QtGui import QFont
from sys import argv, exit
from random import randint, choice
from threading import Timer


def setParams(obj: QWidget, x: int = None, y: int = None, **kwargs) -> None:
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
    colors = ""
    if "color" in kwargs:
        colors += f"color: {kwargs['color']}; "
    if "bg_color" in kwargs:
        colors += f"background-color: {kwargs['bg_color']}; "
    if colors:
        obj.setStyleSheet(colors)
    if (x is not None) and (y is not None):
        if kwargs.get("right", False):
            x -= obj.fontMetrics().boundingRect(obj.text()).width()
        if kwargs.get("down", False):
            y -= obj.fontMetrics().boundingRect(obj.text()).height()
        obj.move(x, y)


def generateQuestion(obj: QLabel) -> None:
    a = choice(["+", "-", "*", "//"])
    if a == "*":
        b1, b2 = randint(1, 10), randint(1, 20)
    elif a == "//":
        b1, b2 = randint(1, 50), randint(1, 20)
    else:
        b1, b2 = randint(1, 50), randint(1, 50)
    setParams(obj, text=f"{b1} {a} {b2}")


tm1, tm2 = Timer(1.0, print), Timer(1.0, print)


def timerShow(obj: QLabel, *args, sec=1.5, **kwargs) -> None:
    global tm1
    tm1.cancel()
    setParams(obj, *args, **kwargs)
    tm1 = Timer(sec, setParams, args=(obj,), kwargs={"text": ""})
    tm1.start()


app = QApplication(argv)
wnd = QMainWindow()
wnd.setGeometry(100, 50, 700, 800)
wnd.setWindowTitle("Math game")

games, wins = 0, 0

prc = QLabel(parent=wnd)
setParams(prc, 220, 100, color="blue", bg_color="lightblue", scale=14)

yzv = QLabel(parent=wnd)
setParams(yzv, 280, 200, bg_color="orange", scale=18)
generateQuestion(yzv)

ntj = QLabel(parent=wnd)
setParams(ntj, 280, 320, scale=14)

krt = QLineEdit(parent=wnd)
setParams(krt, 250, 380, width=200, scale=12)


def isFinished(result=False) -> None:
    global games, wins, tm2
    if (games == 10) or result:
        tm2.cancel()
        perc = round(((wins / games) * 100), 2)
        setParams(prc, text="")
        tm2 = Timer(
            0.5, setParams, args=(prc,), kwargs={"text": f"sizning bilimingiz {perc}%"}
        )
        tm2.start()
        games, wins = 0, 0


def checkAnswer() -> None:
    global games, wins
    try:
        a, b = eval(yzv.text()), int(krt.text())
    except:
        setParams(krt, text="")
        timerShow(ntj, text="error", bg_color="red")
        return
    games += 1
    if a == b:
        wins += 1
        generateQuestion(yzv)
        setParams(krt, text="")
        timerShow(ntj, text="correct", color="green")
    else:
        timerShow(ntj, text="uncorrect", color="red")
    isFinished()


def getNext() -> None:
    global games
    games += 1
    generateQuestion(yzv)
    setParams(krt, text="")
    isFinished()


def getResult() -> None:
    if games != 0:
        generateQuestion(yzv)
        isFinished(True)
    else:
        timerShow(ntj, text="error", bg_color="red")


knp = QPushButton(text="ok", parent=wnd)
setParams(knp, 370, 490, width=100, height=50, bg_color="orange")
knp.clicked.connect(checkAnswer)

nxt = QPushButton(text="next", parent=wnd)
setParams(nxt, 200, 490, width=100, height=50, bg_color="rgb(0, 200, 0)")
nxt.clicked.connect(getNext)

rslt = QPushButton(text="result", parent=wnd)
setParams(rslt, 285, 600, width=100, height=50, bg_color="lightblue")
rslt.clicked.connect(getResult)

wnd.show()
exit(app.exec_())
