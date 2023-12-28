import sys
import pathlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from typing import *


# =====================================================================================================================
# TODO: add COMBO with context-manu for add+delete+lastValue
# TODO: create blank Objects to change state!!! GREEn/RED/Yellow/bare


# =====================================================================================================================
# original names is not enough soft and comfortable for eyes!
# try to use ROUND NUMBERS!!! start use 0/100/200/255!!!
COLOR_TUPLE_RGB__LIGHT_RED = (255, 200, 200)
COLOR_TUPLE_RGB__LIGHT_GREEN = (200, 255, 200)
COLOR_TUPLE_RGB__LIGHT_BLUE = (200, 200, 255)
COLOR_TUPLE_RGB__LIGHT_YELLOW = (255, 255, 100)
COLOR_TUPLE_RGB__LIGHT_GREY_240 = (240, 240, 240)   # #f2f2f2
COLOR_TUPLE_RGB__LIGHT_GREY_220 = (220, 220, 220)
COLOR_TUPLE_RGB__LIGHT_GREY_150 = (150, 150, 150)
COLOR_TUPLE_RGB__WHITE = (255, 255, 255)

MARGINS_0000 = QMargins(0, 0, 0, 0)
MARGINS_5555 = QMargins(5, 5, 5, 5)
MARGINS_9595 = QMargins(9, 5, 9, 5)

ALIGNMENT_T = Qt.Alignment(Qt.AlignTop)
ALIGNMENT_LT = Qt.Alignment(Qt.AlignLeft | Qt.AlignTop)
ALIGNMENT_CENTER_HV = Qt.Alignment(Qt.AlignHCenter | Qt.AlignVCenter)


# ICONS ===============================================================================================================
class QIcon_Set:
    _path: pathlib.Path = pathlib.Path().parent.joinpath('images')

    def __init__(self):
        # JPG
        self.logo_square_200: QIcon = QIcon(str(self._path.joinpath('logo_square_200.jpg')))

        # PNG
        self.load_settings: QIcon = QIcon(str(self._path.joinpath('load_settings.png')))
        self.init: QIcon = QIcon(str(self._path.joinpath('init.png')))
        self.ok: QIcon = QIcon(str(self._path.joinpath('ok.png')))
        self.error: QIcon = QIcon(str(self._path.joinpath('error.png')))
        self.save: QIcon = QIcon(str(self._path.joinpath('save.png')))

        # SVG
        self.arrow_right: QIcon = QIcon(str(self._path.joinpath('arrow_right.svg')))
        self.folder2_open: QIcon = QIcon(str(self._path.joinpath('folder2_open.svg')))
        self.gear: QIcon = QIcon(str(self._path.joinpath('gear.svg')))


# COLOR ===============================================================================================================
class QWidget_ColorChange(QWidget):
    def _color_set_rgb(self, color=None):
        if color:
            self.setStyleSheet(f"background: rgb{color}")
        else:
            self.setStyleSheet(f"")

    def color_clear(self):
        self._color_set_rgb(None)

    def color_set__light_green(self):
        self._color_set_rgb(COLOR_TUPLE_RGB__LIGHT_GREEN)

    def color_set__light_red(self):
        self._color_set_rgb(COLOR_TUPLE_RGB__LIGHT_RED)

    def color_set__light_yellow(self):
        self._color_set_rgb(COLOR_TUPLE_RGB__LIGHT_YELLOW)


class QPushButton(QPushButton, QWidget_ColorChange):
    pass


class QLineEdit(QLineEdit, QWidget_ColorChange):
    pass


class QComboBox(QComboBox, QWidget_ColorChange):
    pass


class QLabel(QLabel, QWidget_ColorChange):
    pass


# =====================================================================================================================
class QPushButton_Checkable(QPushButton):
    def __init__(self, *args, **kwargs):
        self.__text_toggle: list = ["PushDown", "Release"]  # dont move to class method!!! will not work correct!

        # make available init with list!!! -------------------
        args = list(args)
        for index, arg in enumerate(args):
            if isinstance(arg, str):
                self.__text_toggle[0] = self.__text_toggle[1] = arg
                break
            elif isinstance(arg, list) and len(arg) == 2:
                self.__text_toggle = arg
                args[index] = arg[0]
                break
        super().__init__(*args, **kwargs)

        self.__text_toggle_state()

        # work --------------------------------
        self.setCheckable(True)
        self.toggled.connect(self.__text_toggle_state)

    def __text_toggle_state(self, state=None):
        if state is None:
            state = int(self.isChecked())

        self.setText(self.__text_toggle[state])

    def setText(self, text):
        index = int(self.isChecked())
        self.__text_toggle[index] = text
        super().setText(text)


# TESTS ===============================================================================================================
class __TestExample(QWidget):
    def __init__(self):
        super().__init__()

        self.btn1 = QPushButton_Checkable("1")
        self.btn2 = QPushButton_Checkable(["21", "22"])
        self.btn3 = QPushButton_Checkable()

        layout = QVBoxLayout()
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.btn3)
        self.setLayout(layout)
        self.show()

    def print_msg(self):
        print()
        print(self.btn1.isChecked())
        print(self.btn2.isChecked())
        print(self.btn3.isChecked())


# =====================================================================================================================
if __name__ == "__main__":
    app = QApplication([])
    wgt = __TestExample()
    print(app.exec_())


# =====================================================================================================================
