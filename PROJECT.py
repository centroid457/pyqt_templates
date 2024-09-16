from typing import *
from _aux__release_files import release_files_update


# =====================================================================================================================
# VERSION = (0, 0, 3)   # 1/deprecate _VERSION_TEMPLATE from PRJ object +2/place update_prj here in __main__ +3/separate finalize attrs
# VERSION = (0, 0, 4)   # add AUTHOR_NICKNAME_GITHUB for badges
VERSION = (0, 0, 5)     # separate PROJECT_BASE #TODO: need to separate into module!


# =====================================================================================================================
class PROJECT_BASE:
    NAME_IMPORT: str
    VERSION: tuple[int, int, int]

    # AUTHOR ------------------------------------------------
    AUTHOR_NAME: str = "Andrei Starichenko"
    AUTHOR_EMAIL: str = "centroid@mail.ru"
    AUTHOR_HOMEPAGE: str = "https://github.com/centroid457/"
    AUTHOR_NICKNAME_GITHUB: str = "centroid457"

    # AUX ----------------------------------------------------
    CLASSIFIERS_TOPICS_ADD: list[str] = [
        # "Topic :: Communications",
        # "Topic :: Communications :: Email",
    ]

    # FINALIZE -----------------------------------------------
    @classmethod
    @property
    def VERSION_STR(cls) -> str:
        return ".".join(map(str, cls.VERSION))

    @classmethod
    @property
    def NAME_INSTALL(cls) -> str:
        return cls.NAME_IMPORT.replace("_", "-")


# =====================================================================================================================
class PROJECT(PROJECT_BASE):
    # PROJECT ----------------------------------------------
    NAME_IMPORT: str = "pyqt_templates"
    KEYWORDS: list[str] = [
        "pyqt",
        "pyqt templates", "pyqt guide",
        "pyqt usage", "pyqt examples", "pyqt usage examples", "pyqt help", "pyqt help examples",
        "pyqt signals",
    ]
    # README --------------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "pyqt help examples and some other useful objects (overloaded pyqt classes)"
    DESCRIPTION_LONG: str = """Designed for ..."""
    FEATURES: list[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        "good template for TableView/Model/Signals",
    ]

    # HISTORY -----------------------------------------------
    VERSION: tuple[int, int, int] = (0, 1, 3)
    TODO: list[str] = [
        "add Events for TM/TV/PTE/...",
    ]
    FIXME: list[str] = [
        "..."
    ]
    NEWS: list[str] = [
        "add fonts.py",
    ]


# =====================================================================================================================
if __name__ == '__main__':
    release_files_update(PROJECT)


# =====================================================================================================================
