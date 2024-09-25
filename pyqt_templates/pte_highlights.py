from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from object_info import *
from typing import *
from annot_attrs import *


# =====================================================================================================================
def format_make(color_fg: Any = None, style: str = '', color_bg: Any = None) -> QTextCharFormat:
    """
     :returns: QTextCharFormat с указанными атрибутами указанными текстом
     """
    result = QTextCharFormat()

    if color_fg:
        color_fg = QColor(color_fg)
        # color_fg.setNamedColor(color_fg_name)
        result.setForeground(color_fg)

    if color_bg:
        color_bg = QColor(color_bg)
        # color_bg.setNamedColor(color_bg_name)
        result.setBackground(color_bg)

    if 'bold' in style:
        result.setFontWeight(QFont.Bold)
    if 'italic' in style:
        result.setFontItalic(True)

    return result


# =====================================================================================================================
class Style(NamedTuple):
    FORMAT: QTextCharFormat
    P_ITEMS: list[str]
    P_TEMPLATES: list[str] = [r'%s', ]  # FOR ONE LINE!!!
    INDEX: int = 0

    def get_patterns(self) -> set[str]:
        if not self.P_ITEMS:
            result = [pattern for pattern in self.P_TEMPLATES]

        elif not self.P_TEMPLATES:
            result = [pattern for pattern in self.P_ITEMS]

        else:
            result = []
            for template in self.P_TEMPLATES:
                result += [template % item for item in self.P_ITEMS]

        return set(result)

    def get_regexps(self) -> list[QRegExp]:
        return [QRegExp(pattern) for pattern in self.get_patterns()]

    def get_rules(self) -> list[tuple[QRegExp, int, QTextCharFormat]]:
        return [(regexp, self.INDEX, self.FORMAT) for regexp in self.get_regexps()]


# =====================================================================================================================
class Styles(IterAnnotValues):
    """
    EXAMPLE
    -------
    see StylesPython
    """
    def get_rules(self) -> list[tuple[QRegExp, int, QTextCharFormat]]:
        result = []
        for group in self:
            result.extend(group.get_rules())
        return result


# =====================================================================================================================
class StylesPython(Styles):
    KEYWORD: Style = Style(
        FORMAT=format_make('blue'),
        P_ITEMS=[
            'assert', 'exec',
            'global', 'import',
            'lambda', 'print', 'del',

            # def
            'class', "def",

            # blocks
            'if', 'for', 'while', 'try', 'from',
            'elif', 'else', 'except', 'continue', 'finally',
            'raise', 'return', 'yield', 'break', "pass",

            # operators
            'is', 'or', 'and', 'in', 'not',

            # values
            'None', 'True', 'False',
        ],
        P_TEMPLATES=[
            r'\b%s\b',
        ],
    )
    OPERATOR_SIGN: Style = Style(
        FORMAT=format_make('red'),
        P_ITEMS=[
            '=',
            # Comparison
            '==', '!=', '<', '<=', '>', '>=',
            # Arithmetic
            r'\+', '-', r'\*', '/', '//', r'\%', r'\*\*',
            # In-place
            r'\+=', '-=', r'\*=', '/=', r'\%=',
            # Bitwise
            r'\^', r'\|', r'\&', r'\~', '>>', '<<',
        ],
        P_TEMPLATES=[
        ],
    )
    BRACE: Style = Style(
        FORMAT=format_make('darkGray'),
        P_ITEMS=[
            r'\{', r'\}', r'\(', r'\)', r'\[', r'\]',
        ],
        P_TEMPLATES=[
        ],
    )
    DEF: Style = Style(
        FORMAT=format_make('black', 'bold'),
        P_ITEMS=[
            "def", "class"
        ],
        P_TEMPLATES=[
            r'\b%s\b\s*(\w+)',
        ],
        INDEX=1,
    )
    SELF: Style = Style(
        FORMAT=format_make('black', 'italic'),
        P_ITEMS=[
        ],
        P_TEMPLATES=[
            r'\bself\b',
        ],
    )
    NUMBERS: Style = Style(
        FORMAT=format_make('brown'),
        P_ITEMS=[
        ],
        P_TEMPLATES=[
            r'\b[+-]?[0-9]+[lL]?\b',
            r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b',
            r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b',
        ],
    )
    COMMENT: Style = Style(
        FORMAT=format_make('darkGreen', 'italic'),
        P_ITEMS=[
        ],
        P_TEMPLATES=[
            # r'#[^\n]*',
            r'#.*',
        ],
    )
    STRING: Style = Style(
        FORMAT=format_make('magenta'),
        P_ITEMS=[
        ],
        P_TEMPLATES=[
            r'"[^"\\]*(\\.[^"\\]*)*"',
            r"'[^'\\]*(\\.[^'\\]*)*'",
        ],
    )


class StylesMultilines(Styles):
    STRING_3S: Style = Style(
        FORMAT=format_make('darkMagenta'),
        P_ITEMS=[
        ],
        P_TEMPLATES=[
            "'''",
        ],
        INDEX=1,
    )
    STRING_3D: Style = Style(
        FORMAT=format_make('darkMagenta'),
        P_ITEMS=[
        ],
        P_TEMPLATES=[
            '"""',
        ],
        INDEX=2,
    )


# ---------------------------------------------------------------------------------------------------------------------
class StylesUser(StylesPython):
    RESULT_TRUE: Style = Style(
        FORMAT=format_make("", "", "lightGreen"),
        P_ITEMS=[
            "True"
        ],
        P_TEMPLATES=[
            r'.*=\s*%s.*',
        ],
    )
    RESULT_FALSE: Style = Style(
        FORMAT=format_make("", "", "red"),
        P_ITEMS=[
            "False"
        ],
        P_TEMPLATES=[
            r'.*=\s*%s.*',
        ],
    )


# =====================================================================================================================
class PythonHighlighter(QSyntaxHighlighter):
    """
    Синтаксические маркеры для языка Python
    """
    # settings --------------------
    STYLES_LINE: Styles = StylesUser()
    STYLES_MULTYLINES: Styles = StylesMultilines()

    # aux --------------------
    RULES_LINE: list[tuple[QRegExp, int, QTextCharFormat]]
    RULES_MULTILINES: list[tuple[QRegExp, int, QTextCharFormat]]

    def __init__(self, document: QTextDocument, styles: Styles = None):
        QSyntaxHighlighter.__init__(self, document)
        if styles:
            self.STYLES_LINE = styles

        self.RULES_LINE = self.STYLES_LINE.get_rules()
        self.RULES_MULTILINES = self.STYLES_MULTYLINES.get_rules()

    def highlightBlock(self, text, *args) -> None:
        """Применить выделение синтаксиса к данному блоку текста. """
        for expression, nth, format in self.RULES_LINE:
            index = expression.indexIn(text, 0)
            while index >= 0:
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        # self.setCurrentBlockState(0)
        self.apply_multylines(text)

    def apply_multylines(self, text):
        for delimiter, in_state, style in self.RULES_MULTILINES:
            if self.previousBlockState() == in_state:
                start = 0
                add = 0
            else:
                start = delimiter.indexIn(text)
                add = delimiter.matchedLength()

            while start >= 0:
                end = delimiter.indexIn(text, start + add)
                if end >= add:
                    length = end - start + add + delimiter.matchedLength()
                    self.setCurrentBlockState(0)
                else:
                    self.setCurrentBlockState(in_state)
                    length = len(text) - start + add

                self.setFormat(start, length, style)
                start = delimiter.indexIn(text, start + length)

            if self.currentBlockState() == in_state:
                return True
            else:
                return False


# =====================================================================================================================
EXAMPLE_TEXT = """
from typing import *
# привет hello 123
class Cls:  # привет hello 123
    attr_dict: dict = {1: "123"}
    attr_tuple: tuple[Any] = (None, "hello123 123", 'hello123 123')
    attr_list: list[Any] = [0, "1", '2', '''string''', True, int]
    def meth(self) -> bool:
        pass

print(Cls.__annotations__)
print(Cls().__annotations__)
{'attr1': <class 'int'>}

# USER ----- =========
resul=True123
resul=False 123

# COLLECTIONS ----- =========
()[]{} ([{

[1,2, 3]
[
    1,
    2,
]

(1,2, 3)
(
    1,
    2,
)

{1,2, 3}
{
    1,
    2,
}

{1: "1", 2: "2"}
{
    1: "1":,
    2: "2"
}

# TEXT ----- =========
'''
'''

'''
def hello():
    pass

"""


def start_example():
    app = QApplication([])
    PTE = QPlainTextEdit()

    # font = QFont()
    # font.setPointSize(12)
    # PTE.setFont(font)

    highlight = PythonHighlighter(PTE.document())   # need to keep in not used var!
    PTE.show()
    PTE.setPlainText(EXAMPLE_TEXT)
    print(f"{PTE.document()=}")
    # ObjectInfo(PTE.document()).print()

    app.exec_()


# =====================================================================================================================
if __name__ == '__main__':
    start_example()


# =====================================================================================================================
