import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from typing import *


# =====================================================================================================================
class Row:
    NAME: str = "Row"
    SKIP: Optional[bool] = None


class Dev:
    result: Optional[bool] = None


class Data:
    ROWS: List = None
    DEVS: List = None

    def __init__(self, rows: List, devs: List):
        self.ROWS = rows
        self.DEVS = devs


# =====================================================================================================================
class MyTableModel(QAbstractTableModel):
    DATA: Data

    def __init__(self, data: Data):
        super().__init__()
        self.DATA = data

    def rowCount(self, parent: QModelIndex = None) -> int:
        return len(self.DATA.ROWS)

    def columnCount(self, parent: QModelIndex = None) -> int:
        return len(self.DATA.DEVS) + 1

    def headerData(self, col: Any, orientation: Qt.Orientation, role: int = None) -> str:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if col == 0:
                    return "NAME"
                if col > 0:
                    return f"{col}"
            elif orientation == Qt.Vertical:
                return col + 1
        return QVariant()

    def flags(self, index):
        flags = super().flags(index)

        if index.column() == 0:
            flags |= Qt.ItemIsUserCheckable
        return flags

    def data(self, index: QModelIndex, role: int = None) -> Any:
        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()

        tc = list(self.DATA.ROWS)[row]
        if col > 0:
            dut = self.DATA.DEVS[col-1]
        else:
            dut = None

        if role == Qt.DisplayRole:
            if col == 0:
                return f'{tc.NAME}'
            if col > 0:
                return f'{dut.result}'

        elif role == Qt.ForegroundRole:
            if tc.SKIP:
                return QColor('#a2a2a2')

        elif role == Qt.BackgroundRole:
            if tc.SKIP:
                return QColor('#f2f2f2')

            if col > 0:
                if tc.result is True:
                    return QColor("green")
                if tc.result is False:
                    return QColor("red")

        if role == Qt.CheckStateRole:
            if col == 0:
                if tc.SKIP:
                    return Qt.Unchecked
                else:
                    return Qt.Checked

    def setData(self, index: QModelIndex, value: Any, role: int = None):
        if not index.isValid():
            return

        row = index.row()
        col = index.column()

        tc = list(self.DATA.ROWS)[row]
        if col > 0:
            dut = self.DATA.DEVS[col-1]
        else:
            dut = None

        if role == Qt.CheckStateRole and col == 0:
            tc.SKIP = value == Qt.Unchecked
            return True


# =====================================================================================================================
class Gui(QWidget):
    _QAPP: QApplication = QApplication([])

    DATA: Data
    QTV: QTableView = None

    def __init__(self, data: Data):
        super().__init__()
        self.DATA = data

        self.wgt_create()
        self.slots_connect()

        self.show()
        exit_code = self._QAPP.exec_()
        if exit_code == 0:
            print(f"[OK]GUI({exit_code=})closed correctly")
        else:
            print(f"[FAIL]GUI({exit_code=})closed INCORRECTLY")
        sys.exit(exit_code)

    def wgt_create(self):
        self.setWindowTitle("[TestPlan] Universal")
        self.setMinimumSize(600, 300)
        self.qtv_create()

    def qtv_create(self):
        tm = MyTableModel(self.DATA)

        self.QTV = QTableView(self)
        self.QTV.setModel(tm)

        # self.QTV.setStyleSheet("gridline-color: rgb(255, 0, 0)")
        # self.QTV.setMinimumSize(400, 300)
        # self.QTV.setShowGrid(True)
        # self.QTV.setFont(QFont("Calibri (Body)", 12))
        # self.QTV.setSortingEnabled(True)     # enable sorting
        self.QTV.resizeColumnsToContents()   # set column width to fit contents
        # self.QTV.setColumnWidth(0, 100)

        # hh = self.QTV.horizontalHeader()
        # hh.setStretchLastSection(True)

    def slots_connect(self):
        pass


# =====================================================================================================================
if __name__ == '__main__':
    data = Data(list(range(1,5)), list(range(1,4)))
    Gui(data)


# =====================================================================================================================