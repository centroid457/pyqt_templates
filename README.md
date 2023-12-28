# pyqt_templates
Pyqt help examples and some other useful objects (overloaded pyqt classes).  
Designed for ....  


## Features
1. good template for TableView/Model  


********************************************************************************
## License
See the [LICENSE](LICENSE) file for license rights and limitations (MIT).


## Release history
See the [HISTORY.md](HISTORY.md) file for release history.


## Installation
```commandline
pip install pyqt-templates
```


## Import
```python
from pyqt_templates import *
```


********************************************************************************
## USAGE EXAMPLES
See tests and sourcecode for other examples.

******************************
### 1. template-1=IMPORT_BEST.py
```python
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
```

******************************
### 2. template-2=QAPP_in_cls.py
```python
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from typing import *


# =====================================================================================================================
pass


# =====================================================================================================================
class Gui(QWidget):
    TITLE: str = "[GUI] Universal"
    _QAPP: QApplication = QApplication([])

    def __init__(self):
        super().__init__()

        self.wgt_create()
        self.wgt_main__apply_settings()
        self.slots_connect()

        # GUI SHOW ----------------------------------------------------------------------------------------------------
        self.show()
        exit_code = self._QAPP.exec_()
        if exit_code == 0:
            print(f"[OK]GUI({exit_code=})closed correctly")
        else:
            print(f"[FAIL]GUI({exit_code=})closed INCORRECTLY")
        sys.exit(exit_code)

    def wgt_main__apply_settings(self) -> None:
        # MAIN WINDOW -------------------------------------------------------------------------------------------------
        self.setWindowTitle(self.TITLE)

        self.setMinimumSize(300, 100)
        # self.setMinimumWidth(300)
        # self.setMinimumHeight(100)

        self.resize(300, 100)

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

        # layout ------------------------------------------------------------------------------------------------------
        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_grid)
        layout_main.addWidget(self.btn_start)
        self.setLayout(layout_main)

    def slots_connect(self) -> None:
        self.btn_start.toggled.connect(self.btn_toggled)

    def btn_toggled(self, _state: Optional[bool] = None) -> None:
        print(f"btn {_state=}")


# =====================================================================================================================
if __name__ == '__main__':
    Gui()


# =====================================================================================================================
```

******************************
### 3. template-3=TableModel.py
```python
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from typing import *


# =====================================================================================================================
class _Row:
    NAME: str = "_Row"
    SKIP: Optional[bool] = None


class _Dev:
    result: Optional[bool] = None


class _Data:
    ROWS: List = None
    DEVS: List = None

    def __init__(self, rows: List, devs: List):
        self.ROWS = rows
        self.DEVS = devs


# =====================================================================================================================
class _TableModelTemplate(QAbstractTableModel):
    DATA: _Data

    def __init__(self, data: _Data):
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

    DATA: _Data
    QTV: QTableView = None

    def __init__(self, data: _Data):
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
        tm = _TableModelTemplate(self.DATA)

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
    data = _Data(list(range(1,5)), list(range(1,4)))
    Gui(data)


# =====================================================================================================================
```

********************************************************************************
