import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from Get_Map import *
from Geocode import *

MODES = ['map', 'sat', 'skl', 'trf']


class Ui_Form(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MapProject.ui', self)
        self.targets = None
        self.coords = '37.620070,55.753630'
        self.spn = '0.01,0.01'
        self.mode = MODES[0]
        get_map(self.mode, self.coords, spn=self.spn)
        self.set_image('map.png')
        self.chg_type_btn.clicked.connect(self.chg_type)
        self.found_btn.clicked.connect(self.found)

    def update(self):
        get_map(self.mode, self.coords, spn=self.spn, pt=self.targets[0])
        self.set_image('map.png')

    def set_image(self, img_name):
        self.pixmap = QPixmap(img_name)
        self.lbl_image.setPixmap(self.pixmap)
        self.repaint()

    def keyPressEvent(self, event):
        print('click')
        spn = [float(self.spn.split(',')[0]), float(self.spn.split(',')[1])]
        coords = [float(self.coords.split(',')[0]), float(self.coords.split(',')[1])]
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
        if event.key() == Qt.Key_Right:
            coords[0] += spn[0]
        if event.key() == Qt.Key_Up:
            coords[1] += spn[1]
        if event.key() == Qt.Key_Left:
            coords[0] -= spn[0]
        if event.key() == Qt.Key_Down:
            coords[1] -= spn[1]
        spn[0], spn[1] = str(spn[0]), str(spn[1])
        coords[0], coords[1] = str(coords[0]), str(coords[1])
        self.spn = ','.join(spn)
        self.coords = ','.join(coords)
        print(self.coords)
        self.update()

    def chg_type(self):
        self.mode = MODES[len(MODES) % (MODES.index(self.mode) + 1)]
        self.type_lbl.setText(f'Тип: {self.mode}')
        self.update()

    def found(self):
        response = geocode(self.fnd_line.getText())
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            coords = toponym["Point"]["pos"].split()
            self.coords = f'{coords[0]},{coords[1]}'
            self.targets = self.coords
            self.update()
        else:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ui_Form()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
