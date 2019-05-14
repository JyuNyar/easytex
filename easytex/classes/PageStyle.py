from .base_classes.LatexPart import LatexPart
from ..modules.utils import _latex_special_chars, clean_tex

class PageStyle(LatexPart):
    """
    A class representing latex pagestyles. Currently only handles headers and footers.
    """

    def __init__(self, lhead=None, rhead=None, lfoot=None, rfoot=None):
        LatexPart.__init__(self)

        """
        Args
        ----
        lhead: str
            Left header.
        rhead: str
            Right header.
        lfoot: str
            Left footer.
        rfoot: str
            Right footer.
        """

        self.tex = ""

        self.lhead = clean_tex(lhead)
        self.rhead = clean_tex(rhead)
        self.lfoot = clean_tex(lfoot)
        self.rfoot = clean_tex(rfoot)

        if any(
            [
                isinstance(i, str)
                for i in [self.lhead, self.rhead, self.lfoot, self.rfoot]
            ]
        ):

            self.add("\\pagestyle{fancy}\n\n")

            try:
                self.add("\\fancyhead[L]{" + self.lhead + "}\n")

            except:
                pass

            try:
                self.add("\\fancyhead[R]{" + self.rhead + "}\n")

            except:
                pass

            try:
                self.add("\\fancyfoot[L]{" + self.lfoot + "}\n")

            except:
                pass

            try:
                self.add("\\fancyfoot[R]{" + self.rfoot + "}\n")

            except:
                pass

            self.add("\n\\thispagestyle{fancy}\n\n")
