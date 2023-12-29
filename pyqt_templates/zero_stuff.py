from typing import *


# TEST STUFF ==========================================================================================================
class Row_:
    NAME: str = "row"
    SKIP: Optional[bool] = None
    result: Optional[bool] = None

    def __init__(self, name: Optional[Any] = None):
        if name:
            self.NAME = str(name)


class Dev_:
    NAME: str = "dev"
    result: Optional[bool] = None

    def __init__(self, name: Optional[Any] = None):
        if name:
            self.NAME = str(name)


class Data_:
    ROWS: List[Row_] = None
    DEVS: List[Dev_] = None

    def __init__(self, rows: List[Row_], devs: List[Dev_]):
        self.ROWS = rows
        self.DEVS = devs


# =====================================================================================================================
