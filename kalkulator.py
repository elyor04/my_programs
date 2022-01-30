from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QPushButton)
from PyQt5.QtGui import QFont
from sys import argv, exit
from threading import Timer
from math import pi, e, sqrt

class KnopkaAmal(QPushButton):
    def __init__(
        self, blg:str, oyn:QMainWindow, x:int, y:int, rng:str=None, eni:int=None, buyi:int=None
    ) -> None:
        super().__init__(blg, oyn)
        self.adjustSize()
        self.move(x, y)
        if rng != None:
            self.setStyleSheet("background: {0};".format(rng))
        if eni != None: self.setFixedWidth(eni)
        if buyi != None: self.setFixedHeight(buyi)
        self.tksh, self.vqtt = False, 0
    
    def quyibYuborish(self, funk, arg=None) -> None:
        def amal() -> None:
            if arg != None: funk(arg)
            else: funk()
        self.clicked.connect(amal)

    def bosibTurish(self, vqt, funk, funk2=None) -> None:
        def amal() -> None:
            self.tksh = False
            funk()
        def boshla() -> None:
            self.tksh = True
            self.vqtt = Timer(vqt, amal)
            self.vqtt.start()
        def toxta() -> None:
            self.vqtt.cancel()
            if (funk2 != None) and self.tksh: funk2()
        self.pressed.connect(boshla)
        self.clicked.connect(toxta)

class Kalkulyatr(QMainWindow):
    def __init__(self, komp_uchn:bool=True, tell_uchn:bool=False) -> None:
        super().__init__()
        self.setWindowTitle('kalkulator')
        self.blg = ['e', 'π', '√(', ')', '(']
        self.num9_1: list[KnopkaAmal]
        self.num9_1, self.ntj = list(), '0'
        if komp_uchn:
            self.setGeometry(300,500, 800,850)
            self.buyi, self.shrift = 50, 10
        elif tell_uchn:
            self.buyi, self.shrift = 70, 16

    def bajar(self, k:str) -> None:
        yzv, n = list(k), 0
        for i in range(len(yzv)-1, 0, -1):
            if yzv[i].isdigit() and yzv[i-1].isdigit(): n += 1
            else: n = 0
            if n == 3:
                yzv.insert(i, ' ')
                n = 0
            elif yzv[i] == '=':
                yzv.insert(i, ' ')
                yzv.insert(i+2, ' ')
        self.ntj.setText(''.join(yzv))
        self.ntj.adjustSize()
        self.ntj.move(
            560-self.ntj.fontMetrics().boundingRect(self.ntj.text()).width(), 300)
    def yuqot(self) -> None:
        yzv = self.ntj.text()
        if '=' in yzv: yzv = yzv.split('=')[1]
        if ' ' in yzv: yzv = yzv.replace(' ', '')
        self.ntj.setText(yzv)
    def bajar2(self, k:str) -> None:
        self.yuqot()
        yzv = self.ntj.text()
        if yzv == '0' and (k.isdigit() or k in self.blg): yzv = ''
        self.bajar(yzv+k)

    def natija(self) -> None:
        self.yuqot()
        try:
            yzv = self.ntj.text()
            if 'π' in yzv: yzv = yzv.replace('π', 'pi')
            if '^' in yzv: yzv = yzv.replace('^', '**')
            if '√' in yzv: yzv = yzv.replace('√', 'sqrt')
            yzv = round(eval(yzv), 8)
        except: yzv = 'ERROR'
        finally: self.bajar2('=' + str(yzv))
    def uchir(self) -> None:
        yzv = self.ntj.text()
        if ' ' in yzv: yzv = yzv.replace(' ', '')
        if yzv != '0':
            if len(yzv) == 1: self.bajar('0')
            else: self.bajar(yzv[:len(yzv)-1])
    def uchir2(self) -> None:
        if self.ntj.text() != '0': self.bajar('0')
    def funkely(self) -> None:
        if self.ntj.text() != '0': self.bajar2('Elyor')
        else: self.bajar('Elyor')

    def start(self) -> None:
        self.ntj = QLabel(self)
        self.ntj.setFont(QFont('Times', self.shrift))
        self.bajar('0')

        x, y, n = 300, 400, 0
        blg, b = ['=', '0', '.'], self.buyi
        for i in range(9, -3, -1):
            n += 1
            if i > 0:
                num = KnopkaAmal(str(i), self, x, y, "lightblue", 80, b)
            elif i == 0:
                num = KnopkaAmal(blg[i], self, x, y, "green", 160, b)
            else:
                num = KnopkaAmal(blg[abs(i)], self, x, y, "lightblue", 80, b)
            self.num9_1.append(num)
            if n == 3:
                x, n = 300, 0
                y += b+5
            else: x -= 80

        x, y, n = 540, 400, 0
        blg = ['del', 'e', 'π', '^', '/', '*', '√', '-', '+', ')', '(', 'close']
        for i in blg:
            n += 1
            if i == 'del':
                num = KnopkaAmal(i, self, x, y, "gray", 80, b)
            elif i == 'close':
                num = KnopkaAmal(i, self, 460, y+100, "red", 160, b)
            else:
                num = KnopkaAmal(i, self, x, y, "orange", 80, b)
            self.num9_1.append(num)
            if n == 3:
                x, n = 540, 0
                y += b+5
            else: x -= 80

        for i in self.num9_1:
            stl = i.text()
            if stl == '=': i.bosibTurish(2, self.funkely, self.natija)
            elif stl == 'del': i.bosibTurish(1, self.uchir2, self.uchir)
            elif stl == 'close': i.quyibYuborish(self.close)
            else:
                if stl == '√': stl = '√('
                i.quyibYuborish(self.bajar2, stl)
        self.show()

ilv = QApplication(argv)
oyn = Kalkulyatr()
oyn.start()
exit(ilv.exec_())
