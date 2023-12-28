import sys
import pathlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from typing import *


# =====================================================================================================================
Type__SizeTuple = Tuple[Optional[int], Optional[int]]


# TEST STUFF ==========================================================================================================
class _Row:
    NAME: str = "row"
    SKIP: Optional[bool] = None
    result: Optional[bool] = None

    def __init__(self, name: Optional[Any] = None):
        if name:
            self.NAME = str(name)


class _Dev:
    NAME: str = "dev"
    result: Optional[bool] = None

    def __init__(self, name: Optional[Any] = None):
        if name:
            self.NAME = str(name)


class _Data:
    ROWS: List[_Row] = None
    DEVS: List[_Dev] = None

    def __init__(self, rows: List[_Row], devs: List[_Dev]):
        self.ROWS = rows
        self.DEVS = devs


# =====================================================================================================================
class TableModelTemplate(QAbstractTableModel):
    DATA: _Data

    # METHODS USER ----------------------------------------------------------------------------------------------------
    def __init__(self, data: _Data = None):
        super().__init__(parent=None)
        self.DATA = data

    def _data_reread(self) -> None:
        """
        just redraw model by reread all data!
        """
        self.endResetModel()

    # METHODS STD -----------------------------------------------------------------------------------------------------
    def rowCount(self, parent: Any = None, *args, **kwargs) -> int:
        return len(self.DATA.ROWS)

    def columnCount(self, parent: Any = None, *args, **kwargs) -> int:
        return len(self.DATA.DEVS) + 1

    def headerData(self, section: Any, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> str:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "NAME"
                if section > 0:
                    return f"{section}"
            if orientation == Qt.Vertical:
                return section + 1

    def flags(self, index: QModelIndex) -> int:
        """
        VARIANTS FLAGS
        --------------
        Qt.NoItemFlags                      # 0=без флагов - полное отключение и деактивация всего
        flags |= Qt.ItemIsSelectable        # 1=выделяется цветом при выборе, иначе только внешней рамкой!
        flags |= Qt.ItemIsEditable          # 2=можно набирать с клавиатуры!
        flags |= Qt.ItemIsDragEnabled       # 4=
        flags |= Qt.ItemIsDropEnabled       # 8=
        flags |= Qt.ItemIsUserCheckable     # 16=для чекбоксов дает возможность их изменять мышью!
        flags |= Qt.ItemIsEnabled           # 32=если нет - будет затенен! без возможности выбора!
        flags |= Qt.ItemIsTristate=ItemIsAutoTristate    # 64=включение промежуточного значения чекбокса
        flags |= Qt.ItemNeverHasChildren    # 128=
        flags |= Qt.ItemIsUserTristate      # 256=
        """
        flags = super().flags(index)

        if index.column() > 0:
            # flags |= Qt.ItemIsUserCheckable
            # flags |= Qt.ItemIsEditable
            # flags |= Qt.ItemIsSelectable
            # flags |= Qt.ItemIsEnabled
            pass

        elif index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsTristate

        else:
            return Qt.NoItemFlags

        return flags

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        # if not index.isValid():
        #     return QVariant()
        """
        VARIANTS ROLE
        -------------
        DisplayRole = 0
        DecorationRole = 1
        EditRole = 2
        ToolTipRole = 3
        StatusTipRole = 4
        WhatsThisRole = 5
        FontRole = 6
        TextAlignmentRole = 7

        BackgroundRole=BackgroundColorRole = 8
        ForegroundRole=TextColorRole = 9

        CheckStateRole = 10
        SizeHintRole = 13
        InitialSortOrderRole = 14
        UserRole = 256
        """

        # PREPARE -----------------------------------------------------------------------------------------------------
        col = index.column()
        row = index.row()

        tc = list(self.DATA.ROWS)[row]
        if col > 0:
            dut = self.DATA.DEVS[col-1]
        else:
            dut = None

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.DisplayRole:
            if col == 0:
                return f'{tc.NAME}'
            if col > 0:
                return f'{dut.result}'

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.TextAlignmentRole:
            """
            VARIANTS ALIGN
            --------------
            AlignLeft=AlignLeading = 1
            AlignRight=AlignTrailing = 2

            AlignTop = 32
            AlignBottom = 64

            AlignHCenter = 4
            AlignVCenter = 128
            AlignCenter = 132

            AlignAbsolute = 16
            AlignBaseline = 256

            AlignJustify = 8

            AlignHorizontal_Mask = 31
            AlignVertical_Mask = 480
            """
            # return Qt.AlignVCenter | Qt.AlignLeft
            return Qt.AlignCenter

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.FontRole:
            if row % 2:
                # QFont("Arial", 9, QFont.Bold)
                font = QFont()

                font.setBold(True)
                font.setItalic(True)

                font.setOverline(True)      # надчеркнутый
                font.setStrikeOut(True)     # зачеркнутый
                font.setUnderline(True)     # подчеркнутый

                # не понял!! --------------------
                # font.setStretch(5)
                # font.setCapitalization()

                return font

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.BackgroundColorRole:   # =BackgroundRole
            if tc.SKIP:
                return QColor('#f2f2f2')

            if col > 0:
                if tc.result is True:
                    return QColor("green")
                if tc.result is False:
                    return QColor("red")

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.TextColorRole:   # =ForegroundRole
            if tc.SKIP:
                return QColor('#a2a2a2')

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.CheckStateRole:   # для чекбоксов!
            """
            VARIANTS CHECK
            --------------
            Unchecked (или 0) - флажок сброшен;
            PartiallyChecked (или 1) - флажок частично установлен;
            Checked (или 2) - флажок установлен
            """
            if col == 0:
                if tc.SKIP is True:
                    return Qt.Unchecked
                elif tc.SKIP is False:
                    return Qt.Checked
                else:
                    return Qt.PartiallyChecked

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.ToolTipRole:
            return f"{row}/{col}"

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.DecorationRole:   # ИКОНКА в ячейке слева!
            # может не работать! не работало с первого раза, НО потом вдруг заработало само собой когда добавил SizeHintRole!!!
            if col == 1 and not tc.SKIP:
                icon = QIcon()
                icon.addPixmap(QPixmap('logo.jpg'))
                return icon

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.SizeHintRole:     # размер ячейки!
            """
            IMPORTANT: 
            1. meaning like MinimumSize!
            2. BUT if there are IconOrCheck exists - size will be same as before adding it and HIDING oversized text
            """
            if col > 1:
                return QSize(5, 5)

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.EditRole) -> bool:
        """
        NOTE: при фактическом изменении ОБЯЗАТЕЛЬНО возвращать TRUE!!! Иначе Exx!!!!
        in other cases you can return True either, or None!
        """
        # TODO: ALWAYS START data_reread after any SETDATA
        # if not index.isValid():
        #     return False

        # PREPARE -----------------------------------------------------------------------------------------------------
        col = index.column()
        row = index.row()

        tc = list(self.DATA.ROWS)[row]
        if col > 0:
            dut = self.DATA.DEVS[col-1]
        else:
            dut = None

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.CheckStateRole:      # ЧЕКБОКСЫ
            # need used flag ItemIsUserCheckable!
            if col == 0:
                tc.SKIP = value == Qt.Unchecked

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.EditRole:
            # need used flag ItemIsEditable!
            if col == 0:
                print("EditRole")

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.SizeHintRole:
            # хотел увидеть изменение размера НО ЭТО ТАК НЕ РАБОТАЕТ!!!
            print("SizeHintRole")

        # -------------------------------------------------------------------------------------------------------------
        self._data_reread()
        return True


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

    # COMMON WGTS ------------------------------------------------
    BTN_DEBUG: Optional[QPushButton] = None
    QTV: Optional[QTableView] = None
    QTM: Optional[QAbstractTableModel] = None
    QPTE: Optional[QPlainTextEdit] = None

    def __init__(self):
        super().__init__()

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

    # COMMON WGTS =====================================================================================================
    def BTN_DEBUG_create(self) -> None:
        self.BTN_DEBUG = QPushButton("DEBUG")
        self.BTN_DEBUG.setCheckable(True)

    def QTV_create(self) -> None:
        data = _Data([_Row(f"row{index}") for index in range(5)], [_Dev(f"dev{index}") for index in range(4)])
        self.QTM = TableModelTemplate(data)

        self.QTV = QTableView()
        self.QTV.setModel(self.QTM)

        # self.QTV.setStyleSheet("gridline-color: rgb(255, 0, 0)")
        # self.QTV.setMinimumSize(400, 300)
        # self.QTV.setShowGrid(True)
        # self.QTV.setFont(QFont("Calibri (Body)", 12))
        # self.QTV.setSortingEnabled(True)     # enable sorting
        self.QTV.resizeColumnsToContents()   # set column width to fit contents
        # self.QTV.setColumnWidth(0, 100)

        # hh = self.QTV.horizontalHeader()
        # hh.setStretchLastSection(True)

    def QPTE_create(self) -> None:
        self.QPTE = QPlainTextEdit()
        # self.QPTE.setEnabled(True)
        # self.QPTE.setUndoRedoEnabled(True)
        # self.QPTE.setReadOnly(True)
        # self.QPTE.setMaximumBlockCount(15)

        # self.QPTE.clear()
        self.QPTE.setPlainText("setPlainText")
        self.QPTE.appendPlainText("appendPlainText")
        # self.QPTE.appendHtml("")
        # self.QPTE.anchorAt(#)
        # self.QPTE.setSizeAdjustPolicy(#)

    # WINDOW ==========================================================================================================
    def wgt_create(self) -> None:
        self.BTN_DEBUG_create()
        self.QTV_create()
        self.QPTE_create()

        # GRID --------------------------------------------------------------------------------------------------------
        layout_grid = QGridLayout()

        # settings --------------------
        layout_grid.setColumnStretch(1, 2)
        layout_grid.setRowStretch(2, 2)

        layout_grid.setHorizontalSpacing(2)
        layout_grid.setVerticalSpacing(1)
        layout_grid.setSpacing(1)

        layout_grid.setColumnMinimumWidth(0, 100)
        layout_grid.setRowMinimumHeight(1, 50)

        # wgts ------------------------
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
        layout_v.addWidget(self.BTN_DEBUG)
        layout_v.addWidget(self.QPTE)

        # layout_main -------------------------------------------------------------------------------------------------
        layout_main = QHBoxLayout()
        layout_main.addWidget(self.QTV)
        layout_main.addLayout(layout_v)

        self.setLayout(layout_main)

    def slots_connect(self) -> None:
        if self.BTN_DEBUG:
            self.BTN_DEBUG.toggled.connect(self.BTN_DEBUG__toggled)

    def BTN_DEBUG__toggled(self, state: Optional[bool] = None) -> None:
        print(f"btn {state=}")
        self._wgt_main__center()

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
if __name__ == '__main__':
    Gui()


# =====================================================================================================================
