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
            'assert', 'class', 'exec',
            'global', 'import',
            'lambda', 'print', 'del',

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
        INDEX=0,
    )
    OPERATOR: Style = Style(
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
        INDEX=0,
    )
    BRACE: Style = Style(
        FORMAT=format_make('darkGray'),
        P_ITEMS=[
            r'\{', r'\}', r'\(', r'\)', r'\[', r'\]',
        ],
        P_TEMPLATES=[
        ],
        INDEX=0,
    )
    DEFCLASS: Style = Style(
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
        INDEX=0,
    )
    STRING: Style = Style(
        FORMAT=format_make('magenta'),
        P_ITEMS=[
        ],
        P_TEMPLATES=[
            r'"[^"\\]*(\\.[^"\\]*)*"',
            r"'[^'\\]*(\\.[^'\\]*)*'",
        ],
        INDEX=0,
    )
    QUOTTED_3S: Style = Style(
        FORMAT=format_make('darkMagenta'),
        P_ITEMS=[
        ],
        P_TEMPLATES=[
            "'''",
        ],
        INDEX=1,
    )
    QUOTTED_3D: Style = Style(
        FORMAT=format_make('darkMagenta'),
        P_ITEMS=[
        ],
        P_TEMPLATES=[
            '"""',
        ],
        INDEX=2,
    )
    COMMENT: Style = Style(
        FORMAT=format_make('darkGreen', 'italic'),
        P_ITEMS=[
        ],
        P_TEMPLATES=[
            # r'#[^\n]*',
            r'#.*',
        ],
        INDEX=0,
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
        INDEX=0,
    )

    # UserSyntax -------------------------------
    RESULT_TRUE: Style = Style(
        FORMAT=format_make("", "", "lightGreen"),
        P_ITEMS=[
            "True"
        ],
        P_TEMPLATES=[
            r'.*=\s*%s.*',
        ],
        INDEX=0,
    )
    RESULT_FALSE: Style = Style(
        FORMAT=format_make("", "", "red"),
        P_ITEMS=[
            "False"
        ],
        P_TEMPLATES=[
            r'.*=\s*%s.*',
        ],
        INDEX=0,
    )


# =====================================================================================================================
class PythonHighlighter(QSyntaxHighlighter):
    """
    Синтаксические маркеры для языка Python
    """
    STYLES: Styles = StylesPython()
    quotted_3s = StylesPython().QUOTTED_3S.get_rules()[0]
    quotted_3d = StylesPython().QUOTTED_3D.get_rules()[0]

    RULES: list[tuple[QRegExp, int, QTextCharFormat]]

    def __init__(self, document: QTextDocument, styles: Styles = None):
        QSyntaxHighlighter.__init__(self, document)
        if styles:
            self.STYLES = styles

        self.RULES = self.STYLES.get_rules()

    def highlightBlock(self, text, *args) -> None:
        """Применить выделение синтаксиса к данному блоку текста. """
        # Сделайте другое форматирование синтаксиса
        for expression, nth, format in self.RULES:
            index = expression.indexIn(text, 0)
            while index >= 0:
                index  = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Многострочные строки
        in_multiline = self.match_multiline(text, *self.quotted_3s)
        if not in_multiline:
            self.match_multiline(text, *self.quotted_3d)

    def match_multiline(self, text, delimiter, in_state, style):
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
hello # comment привет
def
результат =  True  результат =True
результат =True результат =False
======
''' 111''' 222''' 000'''
123
pass
break 
assert 1 == 2
if True:
   return None 123 # hello 123
   
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
