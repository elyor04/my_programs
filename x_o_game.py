from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
)
from PyQt5.QtGui import QFont
from sys import argv, exit
from random import randrange


class Knopka(QPushButton):
    def clicked_connect(self, funk, *args) -> None:
        chaqir = lambda: funk(*args)
        self.clicked.connect(chaqir)


def sozlash(
    oby: QWidget,
    x: int = None,
    y: int = None,
    eni: int = None,
    buyi: int = None,
    rang: str = None,
    text: str = None,
    mashtab: int = None,
    ung: bool = False,
) -> None:
    if text is not None:
        oby.setText(text)
    if mashtab is not None:
        oby.setFont(QFont("Times", mashtab))
    if (eni is None) or (buyi is None):
        oby.adjustSize()
    if eni is not None:
        oby.setFixedWidth(eni)
    if buyi is not None:
        oby.setFixedHeight(buyi)
    if (x is not None) and (y is not None):
        if ung:
            x -= oby.fontMetrics().boundingRect(oby.text()).width()
        oby.move(x, y)
    if rang is not None:
        oby.setStyleSheet(f"background: {rang}")


ilv = QApplication(argv)
oyn = QMainWindow()
oyn.setGeometry(100, 100, 600, 700)
oyn.setWindowTitle("x_o o'yin")

ntj, yzv1, yzv2 = [QLabel(oyn) for i in range(3)]
sozlash(ntj, 200, 250, mashtab=12)
sozlash(yzv1, 10, 10, mashtab=12, text="siz: 0")
sozlash(yzv2, 590, 10, mashtab=12, text="kompyuter: 0", ung=True)

x_o: list[Knopka]
x_o, n = list(), 0
x, y = 150, 300

tkshr = [True for i in range(9)]
for i in range(9):
    n += 1
    knp = Knopka(oyn)
    sozlash(knp, x, y, 75, 75, rang="lightblue", mashtab=18)
    x_o.append(knp)
    if n == 3:
        x, y = 150, y + 80
        n = 0
    else:
        x += 80

rst = Knopka("reset", oyn)
sozlash(rst, 200, 600, buyi=55, rang="orange", mashtab=12)
uynlar, odam, komp = 0, 0, 0


def tbOlish(lst: list) -> list[list]:
    blgs1 = [list(bls) for bls in zip(lst[0], lst[1], lst[2])]
    blgs2 = list()
    blgs2.append([lst[i][i] for i in range(3)])
    blgs2.append([lst[i][-(i + 1)] for i in range(3)])

    return [*blgs1, *blgs2]


def tugrlabOlish() -> list[list]:
    blgs1 = list()
    blgs1.append([knp.text() for knp in x_o[:3]])
    blgs1.append([knp.text() for knp in x_o[3:6]])
    blgs1.append([knp.text() for knp in x_o[6:]])

    blgs2 = tbOlish(blgs1)
    return [*blgs1, *blgs2]


def indexniOlish() -> list[list]:
    blgs1 = list()
    blgs1.append(list(range(3)))
    blgs1.append(list(range(3, 6)))
    blgs1.append(list(range(6, 9)))

    blgs2 = tbOlish(blgs1)
    return [*blgs1, *blgs2]


def yutgan(blg: str) -> bool:
    blgs = tugrlabOlish()
    for i in blgs:
        if i.count(blg) == 3:
            return True
    return False


def durrang() -> bool:
    blgs = [knp.text() for knp in x_o]
    return "" not in blgs


def blokla(text: str, rang: str) -> None:
    global uynlar
    sozlash(ntj, text=text, rang=rang)
    sozlash(yzv1, text=f"siz: {odam}")
    sozlash(yzv2, 590, 10, text=f"kompyuter: {komp}", ung=True)
    for i in range(9):
        tkshr[i] = False
    uynlar += 1
    if uynlar == 100:
        uynlar = 0


ind_olsh = indexniOlish()


def xavfYokiYutuq(blg: str) -> tuple[bool, int]:
    blgs = tugrlabOlish()
    for bls, ins in zip(blgs, ind_olsh):
        if ("" in bls) and (bls.count(blg) == 2):
            return (True, ins[bls.index("")])
    return (False, 0)


def kompyuter() -> None:
    global komp
    if True in tkshr:
        tksh, t_ind = xavfYokiYutuq("o")
        if tksh:
            ind = t_ind
        else:
            tksh, t_ind = xavfYokiYutuq("x")
            if tksh:
                ind = t_ind
            else:
                while True:
                    ind = randrange(0, 9)
                    if tkshr[ind]:
                        break
        x_o[ind].setText("o")
        tkshr[ind] = False
        if yutgan("o"):
            komp += 1
            blokla("siz yutqazdingiz", "red")
        elif durrang():
            blokla("durrang", "orange")


def uyinchi(ind: int) -> None:
    global odam
    if tkshr[ind]:
        x_o[ind].setText("x")
        tkshr[ind] = False
        if yutgan("x"):
            odam += 1
            blokla("siz yutdingiz", "lightgreen")
        elif durrang():
            blokla("durrang", "orange")
        else:
            kompyuter()


def tozala() -> None:
    blgs = [knp.text() for knp in x_o]
    if blgs.count("x") > 0:
        for i in range(9):
            x_o[i].setText("")
            tkshr[i] = True
        ntj.setText("")
        ntj.adjustSize()
        if uynlar % 2 != 0:
            kompyuter()


for ind, knp in enumerate(x_o):
    knp.clicked_connect(uyinchi, ind)
rst.clicked.connect(tozala)

oyn.show()
exit(ilv.exec_())
