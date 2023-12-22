import sys
import pathlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from typing import *


# =====================================================================================================================
pass


# =====================================================================================================================
class Gui(QWidget):
    TITLE: str = "[GUI] Universal"
    LOGO: str = "logo.jpg"
    FLAGS: Dict[Any, str] = {
        # UNCOMMENT IF NEEDED!
        # values are just for information!
        # if some flags overlays/conflict - used last activated

        # BORDER/FRAME/TITLE ------------------------------------------------------------------
        # Qt.FramelessWindowHint: "[frame]hide outer frame/border (with title), to tern back title add WindowTitleHint",
        # Qt.WindowTitleHint: "[title]force turn on (after FramelessWindowHint) window title",
        # Qt.CustomizeWindowHint: "[title]hide std frame border with title",

        # GEOMETRY ----------------------------------------------------------------------------
        # Qt.MSWindowsFixedSizeDialogHint: "[geometry]block window mouse resizing",

        # BTNS --------------------------------------------------------------------------------
        # Qt.WindowSystemMenuHint: "???[btn]deactivate all btns",
        # Qt.WindowMinimizeButtonHint: "[btn]activate ONLY MINimize",
        # Qt.WindowMaximizeButtonHint: "[btn]activate ONLY MAXimize",
        # Qt.WindowMinMaxButtonsHint: "[btn]activate ONLY MAX+MINimize",
        # Qt.WindowCloseButtonHint: "[btn]keep only CLOSE",
        # Qt.WindowContextHelpButtonHint: "[btn]keep only HELP +CLOSE(but inactivated)",

        # LAYERS -------------------------------------------------------------------------------
        # Qt.WindowStaysOnTopHint: "[layer] always on TOP",
        # Qt.WindowStaysOnBottomHint: "[layer] always on BOTTOM",
    }

    _QAPP: QApplication = QApplication([])

    def __init__(self):
        super().__init__()

        self.wgt_create()
        self.wgt_main__apply_settings()
        self.slots_connect()

        # GUI SHOW ----------------------------------------------------------------------------------------------------
        self.show()
        self._wgt_main__center()
        exit_code = self._QAPP.exec_()
        if exit_code == 0:
            print(f"[OK]GUI({exit_code=})closed correctly")
        else:
            print(f"[FAIL]GUI({exit_code=})closed INCORRECTLY")
        sys.exit(exit_code)

    # MAIN WINDOW =====================================================================================================
    def wgt_main__apply_settings(self) -> None:
        self._wgt_main__apply_logo()
        self.setWindowTitle(self.TITLE)

        for flag in self.FLAGS:
            self.setWindowFlags(flag)

        # self.setGeometry(100, 100, 300, 150)
        # self.setFixedWidth(300)

        self.setMinimumSize(300, 100)
        # self.setMinimumWidth(300)
        # self.setMinimumHeight(100)

        # self.resize(300, 100)
        # self.move(300, 300)

    def _wgt_main__apply_logo(self) -> None:
        """
        need square size for logo!
        """
        logo_filepath = pathlib.Path(self.LOGO)
        if logo_filepath.is_file() and logo_filepath.exists():
            self._QAPP.setWindowIcon(QIcon(logo_filepath.name))

            try:
                # turn on logo for python-applications (only for Windows) as associations
                from PyQt5.QtWinExtras import QtWin
                QtWin.setCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subproduct.version')
            except:
                pass

    def _wgt_main__center(self):
        """
        center the main window considering MULTY MONITORS.
        NOTE: work incorrect in INIT!!! use in root module right after wgt.SHOW() not before!!!
        """
        window_geometry = self.frameGeometry()
        # print(f"window_geometry={window_geometry}")      # PyQt5.QtCore.QRect(100, 100, 500, 500)

        display_obj = QApplication.desktop()
        # print(f"display_obj={display_obj}")      # <PyQt5.QtWidgets.QDesktopWidget object at 0x0000020630E771F0>

        display_index = display_obj.screenNumber(display_obj.cursor().pos())
        # print(f"display_index={display_index}")    # 1

        display_geometry = display_obj.screenGeometry(display_index)
        # print(f"display_geometry={display_geometry}")    # PyQt5.QtCore.QRect(1366, 0, 1920, 1080)

        display_central_point = display_geometry.center()
        # print(f"display_central_point={display_central_point}")    # PyQt5.QtCore.QPoint(2325, 539)

        self.move(
            display_central_point.x() - window_geometry.width()//2,
            display_central_point.y() - window_geometry.height()//2
        )

    # WINDOW ==========================================================================================================
    def wgt_create(self) -> None:
        # GRID --------------------------------------------------------------------------------------------------------
        layout_grid = QGridLayout()
        layout_grid.setSpacing(2)
        layout_grid.addWidget(QLabel("STLINK"), 0, 0)
        layout_grid.addWidget(QLabel("0"), 0, 1)
        layout_grid.addWidget(QLabel("1"), 0, 2)

        # START -------------------------------------------------------------------------------------------------------
        self.btn_start = QPushButton("START")
        self.btn_start.setCheckable(True)

        # layout_main -------------------------------------------------------------------------------------------------
        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_grid)
        layout_main.addWidget(self.btn_start)
        self.setLayout(layout_main)

    def slots_connect(self) -> None:
        self.btn_start.toggled.connect(self.btn_toggled)

    def btn_toggled(self, _state: Optional[bool] = None) -> None:
        print(f"btn {_state=}")
        self._wgt_main__center()

    # EVENTS ==========================================================================================================
    # events list see in source code!

    # def mouseMoveEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None: ...
    # def mouseDoubleClickEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None: ...
    # def mouseReleaseEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None: ...
    # def mousePressEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None: ...

    def moveEvent(self,  a0: Optional[QMoveEvent]) -> None:
        # print(self.geometry().x(), self.geometry().y())
        pass

    def resizeEvent(self, a0: Optional[QResizeEvent]) -> None:
        # print(self.size())
        pass

    def enterEvent(self, a0: Optional[QEvent]) -> None:
        """mouse get aria over the wgt
        """
        # print("mouse enterEvent")
        pass

    def leaveEvent(self, a0: Optional[QEvent]) -> None:
        """mouse leave aria over the wgt
        """
        # print("mouse leaveEvent")
        pass

    # NOT WORKING ------------------------------------------
    # def focusOutEvent(self, a0: Optional[QEvent]) -> None:
    #     """mouse leave aria over the wgt
    #     """
    #     # print("focusOutEvent")
    #     pass
    #
    # def focusInEvent(self, a0: Optional[QEvent]) -> None:
    #     """mouse leave aria over the wgt
    #     """
    #     # print("focusInEvent")
    #     pass


# =====================================================================================================================
if __name__ == '__main__':
    Gui()


# =====================================================================================================================
