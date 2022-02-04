import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from Get_Map import *
from Geocode import *

MODES = {'Схема': 'map',
         'Спутник': 'sat',
         'Гибрид': 'sat,skl'
         }

SIZES = {
    0: 0.002,
    0.002: 0.005,
    0.005: 0.01,
    0.01: 0.015,
    0.015: 0.025,
    0.025: 0.045,
    0.045: 0.09,
    0.09: 0.175,
    0.175: 0.35,
    0.35: 0.7,
    0.7: 1.395,
    1.395: 2.79,
    2.79: 6,
    6: 12,
    12: 24,
    24: 48,
    48: 70
}


class Ui_Form(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MapProject.ui', self)
        self.setChildrenFocusPolicy(Qt.NoFocus)
        self.coords = '37.620070,55.753630'
        self.spn = '0.01,0.01'
        self.mode = 'map'
        self.target = None
        self.fill_chg_mode()
        self.adress = None
        self.postal_code = ''
        get_map(self.mode, self.coords, spn=self.spn)
        self.set_image('map.png')
        self.chg_mode_btn.clicked.connect(self.chg_type)
        self.btn_search.clicked.connect(self.search)
        self.chck_index.stateChanged.connect(self.update)
        self.sbrs_btn.clicked.connect(self.sbros)

    def setChildrenFocusPolicy(self, policy):
        def recursiveSetChildFocusPolicy(parentQWidget):
            for childQWidget in parentQWidget.findChildren(QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)
        recursiveSetChildFocusPolicy(self)
        self.fnd_line.setFocusPolicy(Qt.ClickFocus)

    def fill_chg_mode(self):
        for key in MODES.keys():
            self.chg_mode.addItem(key)
        self.chg_mode.setCurrentIndex(0)

    def update(self):
        get_map(self.mode, self.coords, spn=self.spn, pt=self.target)
        if self.adress:
            if self.chck_index.isChecked():
                print(self.adress, self.postal_code)
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
        spn = [float(self.spn.split(',')[0]), float(self.spn.split(',')[1])]
        coords = [float(self.coords.split(',')[0]), float(self.coords.split(',')[1])]
        if event.key() == Qt.Key_PageUp:
            if spn[0] < 70:
                spn[0] = SIZES[spn[0]]
                spn[1] = SIZES[spn[1]]
        elif event.key() == Qt.Key_PageDown:
            if spn[0] > 0:
                for key, value in SIZES.items():
                    if value == spn[0]:
                        spn[0], spn[1] = key, key
        if event.key() == Qt.Key_Right:
            coords[0] += spn[0]
        if event.key() == Qt.Key_Up:
            coords[1] += spn[1]
        if event.key() == Qt.Key_Left:
            coords[0] -= spn[0]
        if event.key() == Qt.Key_Down:
            coords[1] -= spn[1]
        if coords[0] - spn[0] < -180 and event.key() == Qt.Key_Left:
            coords[0] = 180 - spn[0]
        elif coords[0] + spn[0] > 180 and event.key() == Qt.Key_Right:
            coords[0] = -180 + spn[0]
        if coords[1] < -90 and event.key() == Qt.Key_Down:
            coords[1] = 180 + coords[1]
        elif coords[1] > 90 and event.key() == Qt.Key_Up:
            coords[1] = -180 + coords[1]
        spn[0], spn[1] = str(spn[0]), str(spn[1])
        coords[0], coords[1] = str(coords[0]), str(coords[1])
        self.spn = ','.join(spn)
        self.coords = ','.join(coords)
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
                self.postal_code = ''

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
        self.postal_code = ''
        self.update()

    def mousePressEvent(self, mouseEvent):
        self.fnd_line.clearFocus()
        self.lbl_image.adjustSize()
        geom = self.lbl_image.geometry()
        center_coord = (geom.x() + 300, geom.y() + 225)
        rads_x = float(self.spn.split(',')[0]) / 600
        rads_y = float(self.spn.split(',')[1]) / 450
        move_x = (mouseEvent.x() - center_coord[0]) * rads_x * 2.55
        move_y = (mouseEvent.y() - center_coord[1]) * -rads_y * 1.1
        map_coords = [float(self.coords.split(',')[0]), float(self.coords.split(',')[1])]
        map_coords[0] += move_x
        map_coords[1] += move_y
        map_coords[0], map_coords[1] = str(map_coords[0]), str(map_coords[1])
        self.target = ','.join(map_coords)
        a = self.fnd_line.text()
        self.fnd_line.setText(self.target)
        coords = self.coords
        self.search()
        self.coords = coords
        self.fnd_line.setText(a)
        self.update()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ui_Form()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())