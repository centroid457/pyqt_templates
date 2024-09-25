![Ver/TestedPython](https://img.shields.io/pypi/pyversions/pyqt_templates)
![Ver/Os](https://img.shields.io/badge/os_development-Windows-blue)  
![repo/Created](https://img.shields.io/github/created-at/centroid457/pyqt_templates)
![Commit/Last](https://img.shields.io/github/last-commit/centroid457/pyqt_templates)
![Tests/GitHubWorkflowStatus](https://github.com/centroid457/pyqt_templates/actions/workflows/test_linux.yml/badge.svg)
![Tests/GitHubWorkflowStatus](https://github.com/centroid457/pyqt_templates/actions/workflows/test_windows.yml/badge.svg)  
![repo/Size](https://img.shields.io/github/repo-size/centroid457/pyqt_templates)
![Commit/Count/t](https://img.shields.io/github/commit-activity/t/centroid457/pyqt_templates)
![Commit/Count/y](https://img.shields.io/github/commit-activity/y/centroid457/pyqt_templates)
![Commit/Count/m](https://img.shields.io/github/commit-activity/m/centroid457/pyqt_templates)

# pyqt_templates (current v0.1.4/![Ver/Pypi Latest](https://img.shields.io/pypi/v/pyqt_templates?label=pypi%20latest))

## DESCRIPTION_SHORT
pyqt help examples and some other useful objects (overloaded pyqt classes)

## DESCRIPTION_LONG
Designed for ...


## Features
1. good template for TableView/Model/Signals  


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
See tests, sourcecode and docstrings for other examples.  

------------------------------
### 1. template-1=IMPORT_BEST.py
```python
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
```

------------------------------
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

********************************************************************************
