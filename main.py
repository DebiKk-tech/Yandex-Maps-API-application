import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from Get_Map import *


class Ui_Form(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MapProject.ui', self)
        self.coords = '37.620070,55.753630'
        self.spn = '0.01,0.01'
        self.mode = 'map'
        get_map(self.mode, self.coords, spn=self.spn)
        self.set_image('map.png')

    def update(self):
        get_map(self.mode, self.coords, spn=self.spn)
        self.set_image('map.png')

    def set_image(self, img_name):
        self.pixmap = QPixmap(img_name)
        self.lbl_image.setPixmap(self.pixmap)
        self.repaint()

    def keyPressEvent(self, event):
        spn = [float(self.spn.split(',')[0]), float(self.spn.split(',')[1])]
        if event.key() == Qt.Key_PageUp:
            spn[0] += 0.005
            spn[1] += 0.005
            if spn[0] > 90:
                spn[1] = 90
                spn[0] = 90
        elif event.key() == Qt.Key_PageDown:
            spn[0] -= 0.005
            spn[1] -= 0.005
            if spn[0] < 0:
                spn[1] = 0
                spn[0] = 0
        spn[0], spn[1] = round(spn[0], 4), round(spn[1], 4)
        spn[0], spn[1] = str(spn[0]), str(spn[1])
        self.spn = ','.join(spn)
        print(self.spn)
        self.update()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ui_Form()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())