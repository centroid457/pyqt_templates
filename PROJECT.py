from typing import *


# =====================================================================================================================
class PROJECT:
    # AUX --------------------------------------------------
    _VERSION_TEMPLATE: Tuple[int] = (0, 0, 2)

    # MAIN -------------------------------------------------
    AUTHOR_NAME: str = "Andrei Starichenko"
    AUTHOR_EMAIL: str = "centroid@mail.ru"
    AUTHOR_HOMEPAGE: str = "https://github.com/centroid457/"

    # PROJECT ----------------------------------------------
    NAME_IMPORT: str = "pyqt_templates"
    NAME_INSTALL: str = NAME_IMPORT.replace("_", "-")
    KEYWORDS: List[str] = [
        "pyqt",
        "pyqt templates", "pyqt guide",
        "pyqt usage", "pyqt examples", "pyqt usage examples", "pyqt help", "pyqt help examples",
        "pyqt signals",
    ]
    CLASSIFIERS_TOPICS_ADD: List[str] = [
        # "Topic :: Communications",
        # "Topic :: Communications :: Email",
    ]
    # README --------------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "pyqt help examples and some other useful objects (overloaded pyqt classes)"
    DESCRIPTION_LONG: str = """Designed for ..."""
    FEATURES: List[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        "good template for TableView/Model/Signals",
    ]

    # HISTORY -----------------------------------------------
    VERSION: Tuple[int, int, int] = (0, 0, 5)
    VERSION_STR: str = ".".join(map(str, VERSION))
    TODO: List[str] = [
        "add Events for TM/TV/PTE/...",

    ]
    FIXME: List[str] = [
        "..."
    ]
    NEWS: List[str] = [
        "apply new pypi template",
        "fix TvHeaderVelection on nonSelectable column",
        # "HeaderViewCB",
    ]


# =====================================================================================================================
if __name__ == '__main__':
    pass


# =====================================================================================================================
