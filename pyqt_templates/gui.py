import sys
import pathlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from typing import *

from .zero_stuff import Row_, Dev_, Data_
from .tm import TableModelTemplate


# =====================================================================================================================
Type__SizeTuple = Tuple[Optional[int], Optional[int]]


# =====================================================================================================================
class Gui(QWidget):
    # SETTINGS --------------------------------------------------
    TITLE: str = "[GUI] Template"
    LOGO: str = "logo.jpg"
    CENTER: bool = True

    SIZE_MINIMUM: Type__SizeTuple = (None, None)
    SIZE_MAXIMUM: Type__SizeTuple = (None, None)
    SIZE_FIXED: Type__SizeTuple = (None, None)
    SIZE: Type__SizeTuple = (None, None)
    MOVE: Type__SizeTuple = (None, None)

    FLAGS: Dict[Any, str] = {
        # TODO: use separated as CLASS!!! with special FLAG methods!!! sum/del/check/... and try to mark as True/False/None

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

    # AUXILIARY --------------------------------------------------
    _QAPP: QApplication = QApplication([])

    # COMMON ------------------------------------------------------
    DATA: Optional[Any] = None

    BTN: Optional[QPushButton] = None
    TV: Optional[QTableView] = None
    TM: Optional[QAbstractTableModel] = None
    PTE: Optional[QPlainTextEdit] = None

    def __init__(self, data: Optional[Any] = None):
        super().__init__()

        if data is not None:
            self.DATA = data

        self.wgt_create()
        self.slots_connect()

        # GUI SHOW ----------------------------------------------------------------------------------------------------
        self._wgt_main__apply_settings()
        self.show()
        if self.CENTER:
            self._wgt_main__center()
        exit_code = self._QAPP.exec_()
        if exit_code == 0:
            print(f"[OK]GUI({exit_code=})closed correctly")
        else:
            print(f"[FAIL]GUI({exit_code=})closed INCORRECTLY")
        sys.exit(exit_code)

    # MAIN WINDOW =====================================================================================================
    def _wgt_main__apply_settings(self) -> None:
        # TITLE --------------------------------------------------
        self.setWindowTitle(self.TITLE)
        self._wgt_main__apply_logo()

        # FLAGS ---------------------------------------------------
        flag_cum = 0
        for flag in self.FLAGS:
            flag_cum |= flag
        if flag_cum:
            self.setWindowFlags(flag_cum)

        # GEOMETRY ------------------------------------------------
        if self.SIZE_MINIMUM[0]:
            self.setMinimumWidth(self.SIZE_MINIMUM[0])
        if self.SIZE_MINIMUM[1]:
            self.setMinimumHeight(self.SIZE_MINIMUM[1])

        if self.SIZE_MAXIMUM[0]:
            self.setMaximumWidth(self.SIZE_MAXIMUM[0])
        if self.SIZE_MAXIMUM[1]:
            self.setMaximumHeight(self.SIZE_MAXIMUM[1])

        if self.SIZE_FIXED[0]:
            self.setFixedWidth(self.SIZE_FIXED[0])
        if self.SIZE_FIXED[1]:
            self.setFixedHeight(self.SIZE_FIXED[1])

        if self.SIZE[0] or self.SIZE[1]:
            width = self.SIZE[0] or self.width()
            height = self.SIZE[1] or self.height()
            self.resize(width, height)

        if self.MOVE[0] or self.MOVE[1]:
            x = self.MOVE[0] or self.x()
            y = self.MOVE[1] or self.y()
            self.move(x, y)

        # USER ------------------------------------------------

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

    # COMMON ==========================================================================================================
    def BTN_create(self) -> None:
        self.BTN = QPushButton("BTN")

        self.BTN.set(True)

        # SETTINGS -------------------------
        self.BTN.setText("BTN_mod")
        self.BTN.setToolTip("ToolTip")

        self.BTN.setCheckable(True)
        # self.BTN.setChecked(False)
        # self.BTN.setFlat(True)        # без явного выделения формы кнопки как виджета!!! вид Label!!!  НО нажатия визуализирует как виджет BTN!!!
        # self.BTN.setDefault(True)     # кажется выделяет рамкой навсегда среди всех?

        # self.BTN.setEnabled(True)
        # self.BTN.setDisabled(True)
        # self.BTN.setVisible(True)
        # self.BTN.setHidden(True)

        # GEOMETRY ----------------------
        # self.BTN.setSizeIncrement(100, 100)     # не понял!!!

        # self.BTN.setMinimumWidth(5)
        # self.BTN.setMinimumHeight(5)
        # self.BTN.setMinimumSize(5, 5)

        # self.BTN.setMaximumWidth(300)
        # self.BTN.setMaximumHeight(20)
        # self.BTN.setMaximumSize(300, 20)

        # если это сделать, то расширяться не будет!!!!!
        # self.BTN.setFixedWidth(100)      # in pixels
        # self.BTN.setFixedHeight(20)
        # self.BTN.setFixedSize(5, 5)

        # OBJECTS ---------------------------
        # self.BTN.setFont(...)

        # self.BTN.setIcon(...)
        # self.BTN.setIconSize(...)

        # DONT UNDERSTAND -------------------
        # self.BTN.setAutoRepeat(True)
        # self.BTN.setAutoRepeatDelay(2)
        # self.BTN.setAutoRepeatInterval(2)

        # PROPERTIES ------------------------
        print(self.BTN.isCheckable())
        print(self.BTN.isChecked())
        print(self.BTN.isDown())
        print(self.BTN.isFlat())
        print(self.BTN.isHidden())

    def TV_create(self) -> None:
        # PREPARE ------------------------
        if self.DATA is None:
            self.DATA = Data_([Row_(f"row{index}") for index in range(5)], [Dev_(f"dev{index}") for index in range(4)])

        self.TM = TableModelTemplate(self.DATA)

        # WORK ---------------------------
        self.TV = QTableView()
        self.TV.setModel(self.TM)

        # self.TV.setStyleSheet("gridline-color: rgb(255, 0, 0)")
        # self.TV.setMinimumSize(400, 300)
        # self.TV.setShowGrid(True)
        # self.TV.setFont(QFont("Calibri (Body)", 12))
        # self.TV.setSortingEnabled(True)     # enable sorting
        self.TV.resizeColumnsToContents()   # set column width to fit contents
        # self.TV.setColumnWidth(0, 100)

        # hh = self.TV.horizontalHeader()
        # hh.setStretchLastSection(True)

    def PTE_create(self) -> None:
        self.PTE = QPlainTextEdit()

        # METHODS ORIGINAL ---------------------------------
        # self.PTE.setEnabled(True)
        # self.PTE.setUndoRedoEnabled(True)
        # self.PTE.setReadOnly(True)
        # self.PTE.setMaximumBlockCount(15)

        # self.PTE.clear()
        self.PTE.setPlainText("setPlainText")
        self.PTE.appendPlainText("appendPlainText")
        # self.PTE.appendHtml("")
        # self.PTE.anchorAt(#)
        # self.PTE.setSizeAdjustPolicy(#)

        # METHODS COMMON -----------------------------------
        self.PTE.setFont(QFont("Calibri (Body)", 7))

    # WINDOW ==========================================================================================================
    def wgt_create(self) -> None:
        self.BTN_create()
        self.TV_create()
        self.PTE_create()

        # GRID --------------------------------------------------------------------------------------------------------
        layout_grid = QGridLayout()

        # settings ---------------------------------------------
        layout_grid.setColumnStretch(1, 2)
        layout_grid.setRowStretch(2, 2)

        layout_grid.setHorizontalSpacing(2)
        layout_grid.setVerticalSpacing(1)
        layout_grid.setSpacing(1)

        layout_grid.setColumnMinimumWidth(0, 100)
        layout_grid.setRowMinimumHeight(1, 50)

        # wgts --------------------------------------------------
        layout_grid.addWidget(QLabel("00"), 0, 0)
        layout_grid.addWidget(QLabel("01"), 0, 1)
        layout_grid.addWidget(QLabel("02"), 0, 2)
        layout_grid.addWidget(QLabel("03"), 0, 3)

        layout_grid.addWidget(QLabel("10"), 1, 0)
        layout_grid.addWidget(QLabel("11-12"), 1, 1, 1, 2)
        layout_grid.addWidget(QLabel("13"), 1, 3)

        layout_grid.addWidget(QLabel("20"), 2, 0)
        layout_grid.addWidget(QLabel("21-end"), 2, 1, 2, -1)

        # layout_main -------------------------------------------------------------------------------------------------
        layout_v = QVBoxLayout()
        layout_v.addLayout(layout_grid)
        layout_v.addWidget(self.BTN)
        layout_v.addWidget(self.PTE)

        # layout_main -------------------------------------------------------------------------------------------------
        layout_main = QHBoxLayout()
        layout_main.addWidget(self.TV)
        layout_main.addLayout(layout_v)

        self.setLayout(layout_main)

    # SLOTS ===========================================================================================================
    def slots_connect(self) -> None:
        if self.BTN:
            self.BTN.clicked.connect(self._wgt_main__center)
            if self.BTN.isCheckable():
                self.BTN.toggled.connect(self.BTN__toggled)
            else:
                self.BTN.clicked.connect(self.BTN__toggled)

        if self.TV:
            self.TV.selectionModel().selectionChanged.connect(self.TV_selection_changed)

    def BTN__toggled(self, state: Optional[bool] = None) -> None:
        print(f"btn {state=}")

    def TV_selection_changed(self, first: QItemSelection, last: QItemSelection) -> None:
        # print("selectionChanged")
        # print(f"{first=}")  # first=<PyQt5.QtCore.QItemSelection object at 0x000001C79A107460>
        # ObjectInfo(first.indexes()[0]).print(_log_iter=True, skip_fullnames=["takeFirst", "takeLast"])

        if not first:
            print(f"selected first NotSelectable Index {first=}")
            return

        index: QModelIndex = first.indexes()[0]

        row = index.row()
        col = index.column()

        self.PTE.setPlainText(f"{row=}/{col=}")

    # EVENTS ==========================================================================================================
    pass    # events list see in source code!
    pass    # events list see in source code!
    pass    # events list see in source code!
    pass    # events list see in source code!
    pass    # events list see in source code!

    # def mouseMoveEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None: ...

    def moveEvent(self,  a0: Optional[QMoveEvent] = None, QMoveEvent: Any = None) -> None:
        # print(self.geometry().x(), self.geometry().y())
        pass

    def resizeEvent(self, a0: Optional[QResizeEvent] = None, ResizeEvent: Any = None) -> None:
        # print(self.size())
        pass

    # mouse POINTER -------------------------------------------------
    def enterEvent(self, a0: Optional[QEvent] = None) -> None:
        """mouse get aria over the wgt
        """
        # print("mouse enterEvent")
        pass

    def leaveEvent(self, a0: Optional[QEvent] = None) -> None:
        """mouse leave aria over the wgt
        """
        # print("mouse leaveEvent")
        pass

    # mouse CLICK -------------------------------------------------
    def mousePressEvent(self, a0: Optional[QMouseEvent] = None) -> None:
        """will not apply when click on wgt btns!"""
        # print("mouse mousePressEvent")
        pass

    def mouseDoubleClickEvent(self, a0: Optional[QMouseEvent] = None) -> None:
        """will not apply when click on wgt btns!
        DIFFERENCE between DoubleClick and PressEvent
            if detected DoubleClick it will generate DoubleClickEvent else PressEvent
                mouse mousePressEvent
                mouse mouseReleaseEvent
                mouse mouseDoubleClickEvent
                mouse mouseReleaseEvent
        """
        # print("mouse mouseDoubleClickEvent")
        pass

    def mouseReleaseEvent(self, a0: Optional[QMouseEvent] = None) -> None:
        """
        work always! both for One/Double click!
            mouse mousePressEvent
            mouse mouseReleaseEvent
            mouse mouseDoubleClickEvent
            mouse mouseReleaseEvent
        """
        # print("mouse mouseReleaseEvent")
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
