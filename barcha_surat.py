from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QWidget,
)
from PyQt5.QtGui import QFont
from cv2 import (
    imread,
    imshow,
    waitKey,
    destroyAllWindows,
    resize,
    INTER_AREA,
    INTER_LINEAR,
    INTER_CUBIC,
)
from sys import argv, exit
from time import time, sleep
from keyboard import is_pressed
from os import listdir
from os.path import isfile
from math import sqrt
from numpy import ndarray


def sozQiymat(
    img: ndarray = None, eni: int = None, buyi: int = None, yuza: int = 100000
) -> tuple[int, int]:
    if (eni is None) or (buyi is None):
        buyi, eni = img.shape[:2]
    k = round(sqrt(yuza / (eni * buyi)), 4)
    x, y = int(eni * k), int(buyi * k)
    return (x, y)


def sozlash(
    img: ndarray,
    eni: int = None,
    buyi: int = None,
    sifat: bool = False,
    auto: bool = False,
    yuza: int = 100000,
) -> ndarray:
    if auto:
        x, y = sozQiymat(img, yuza=yuza)
    else:
        x, y = eni, buyi
    buyi, eni = img.shape[:2]

    if x <= eni and y <= buyi:
        return resize(img, (x, y), interpolation=INTER_AREA)
    elif x >= eni and y >= buyi:
        if sifat:
            return resize(img, (x, y), interpolation=INTER_CUBIC)
        else:
            return resize(img, (x, y), interpolation=INTER_LINEAR)
    else:
        return resize(img, (x, y))


class Filelar(object):
    def __init__(self) -> None:
        super(Filelar, self).__init__()
        self.__path, self.__tkshr = list(), str()

    def start(self, path: str, files: list = ["jpg", "png"], all: bool = False) -> list:
        if not self.__tkshr:
            self.__tkshr = path
        for i in listdir(path):
            pth = path + "/" + i
            if not isfile(pth):
                try:
                    self.start(pth, files, all)
                except:
                    pass
            else:
                if all:
                    self.__path.append(pth)
                else:
                    for j in files:
                        if i.endswith("." + j):
                            self.__path.append(pth)
                            break
        if path == self.__tkshr:
            rtrn = self.__path.copy()
            self.__tkshr = ""
            self.__path.clear()
            return rtrn


class Window(QMainWindow):
    def __init__(self) -> None:
        super(Window, self).__init__()
        self.setWindowTitle("barcha suratlar")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background: lightblue")
        self.__files = [
            "jpg",
            "png",
            "jpeg",
            "gif",
            "tiff",
            "psd",
            "pdf",
            "eps",
            "ai",
            "indd",
            "raw",
            "jfif",
            "tif",
        ]
        self.__oby = Filelar()

    def bajar(
        self,
        obj: QWidget,
        x: int,
        y: int,
        mashtab: int = 10,
        sozlash: bool = False,
        rang: str = None,
        eni: int = None,
        buyi: int = None,
    ) -> None:
        if mashtab is not None:
            obj.setFont(QFont("Times", mashtab))
        if not sozlash:
            obj.move(x, y)
        else:
            obj.move(x - obj.fontMetrics().boundingRect(obj.text()).width(), y)
        if rang is not None:
            obj.setStyleSheet(f"background: {rang}")
        obj.adjustSize()
        if eni is not None:
            obj.setFixedWidth(eni)
        if buyi is not None:
            obj.setFixedHeight(buyi)

    def tozala(self) -> None:
        for i in self.__yz:
            i.setText("")

    def surat(self) -> None:
        self.tozala()
        path = self.manzil.text()
        self.__yz[0].setText("FILELARNI QIDIRISH BOSHLANDI ...")
        self.__yz[0].adjustSize()
        waitKey(10)

        tm = time()
        adres = self.__oby.start(path, self.__files)
        tm = time() - tm
        ad_ln, n = len(adres), 0

        self.__yz[1].setText(f"TAXMINAN {ad_ln} TA FILE TOPILDI !!!")
        self.__yz[1].adjustSize()
        self.__yz[2].setText(f"QIDIRUVGA KETGAN VAQT: {round(tm, 2)} sekund")
        self.__yz[2].adjustSize()
        waitKey(10)

        if ad_ln > 0:
            while True:
                if is_pressed("q") or ad_ln == 0:
                    destroyAllWindows()
                    break
                if is_pressed("right"):
                    if n + 1 < ad_ln:
                        n += 1
                    else:
                        n = 0
                if is_pressed("left"):
                    if n - 1 > -1:
                        n -= 1
                    else:
                        n = ad_ln - 1
                try:
                    img = sozlash(imread(adres[n]), sifat=True, auto=True, yuza=300000)
                except:
                    adres.pop(n)
                    ad_ln -= 1
                    if n == ad_ln:
                        n -= 1
                    self.__yz[1].setText(f"TAXMINAN {ad_ln} TA FILE TOPILDI !!!")
                    self.__yz[1].adjustSize()
                else:
                    self.__yz[3].setText(
                        f"{n+1} - surat\n(q harfini bossangiz chiqasiz)"
                    )
                    self.__yz[3].adjustSize()
                    imshow("surat", img)
                    waitKey(0)
                sleep(0.005)
            self.__yz[3].setText("")

    def start(self) -> None:
        m = QLabel("Boshlang`ich manzilni kiriting:", self)
        self.bajar(m, 10, 5)
        self.manzil = QLineEdit("C:/Users", self)
        self.bajar(self.manzil, 10, 30, rang="white", eni=220)

        self.knopka = QPushButton("QIDIRISH", self)
        self.bajar(self.knopka, 10, 70, rang="orange")
        self.knopka.clicked.connect(self.surat)

        self.__yz = [QLabel(self) for i in range(4)]
        self.bajar(self.__yz[0], 250, 70)
        self.bajar(self.__yz[1], 250, 100)
        self.bajar(self.__yz[2], 250, 130)
        self.bajar(self.__yz[3], 210, 210, 12)

        self.show()


ilv = QApplication(argv)
oyn = Window()
oyn.start()
exit(ilv.exec_())
