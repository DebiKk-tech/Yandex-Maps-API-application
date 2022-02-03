import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from Get_Map import *
from Geocode import *

MODES = {'Схема': 'map',
         'Спутник': 'sat',
         'Гибрид': 'sat,skl'
         }


class Ui_Form(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MapProject.ui', self)
        self.coords = '37.620070,55.753630'
        self.spn = '0.01,0.01'
        self.mode = 'map'
        self.target = None
        self.fill_chg_mode()
        self.adress = None
        self.postal_code = None
        get_map(self.mode, self.coords, spn=self.spn)
        self.set_image('map.png')

        self.chg_mode_btn.clicked.connect(self.chg_type)


        self.btn_search.clicked.connect(self.search)
        self.chck_index.stateChanged.connect(self.update)
        self.sbrs_btn.clicked.connect(self.sbros)

    def fill_chg_mode(self):
        for key in MODES.keys():
            self.chg_mode.addItem(key)
        self.chg_mode.setCurrentIndex(0)

    def update(self):
        get_map(self.mode, self.coords, spn=self.spn, pt=self.target)
        if self.adress:
            if self.chck_index.isChecked():
                self.edit_output.setText(self.adress + self.postal_code)
            else:
                self.edit_output.setText(self.adress)
        elif self.chck_index.isChecked() and self.edit_output.toPlainText() != '':
            self.edit_output.setText(self.edit_output.toPlainText() + self.postal_code)
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
        self.mode = MODES[self.chg_mode.currentText()]
        print(self.mode)
        self.update()

    def search(self):
        response = geocode(self.fnd_line.text())
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            coords = toponym["Point"]["pos"].split()
            adress = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            try:
                postal_code = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]['postal_code']
                self.postal_code = ', ' + postal_code
            except:
                pass
            self.adress = adress
            self.coords = f'{coords[0]},{coords[1]}'
            self.target = self.coords
            self.update()
        else:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")

    def sbros(self):
        self.target = None
        self.edit_output.setText('')
        self.adress = None
        self.edit_output.setDisabled(True)
        self.postal_code = None
        self.update()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ui_Form()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
