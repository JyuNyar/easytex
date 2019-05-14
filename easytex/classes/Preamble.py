from .base_classes.LatexPart import LatexPart
from ..modules.utils import _latex_special_chars, clean_tex

class Preamble(LatexPart):
    """
    This class represents a latex preamble.
    A user may specify a preamble upon initialization, or a default will be loaded.
    User may specify further document properties: Font, Author, Date and Title.
    """

    def __init__(self, tex=None, font=None, title=None, author=None, date=None):
        LatexPart.__init__(self)

        """
        Args
        ----
        tex: str
            Can pass a custom preamble here.
            If None, then pre-defined preamble is loaded.
        font: str
            Name of font to use with the document.
        title: str
            Title of the report.
        author: str
            Author(s) of the report.
        date: str
            String representing the date to appear on the document.
        """

        self.font = font

        if tex is None:
            self.tex = ""
            self.add_preamble(self.font)
        else:
            self.tex = tex

        self.title = clean_tex(title)

        self.author = clean_tex(author)

        self.date = clean_tex(date)

        self.set_document_title()

    def add_preamble(self, font=None):
        """
        Loads a saved latex preamble and saves it in Preamble.tex
         
         Args
        ----
        font: str
            Name of font to use with the document.
        """

        from easytex import resources_dir
 
        with open(resources_dir, "r") as file:

            preamble = file.read()

            if font is not None:
                preamble = preamble.replace("%__", "")
                preamble = preamble.replace("__font__", font)

            self.add(preamble + "\n\n")

    def set_document_title(self):
        """Adds the title, author(s) and date to the document)"""

        if self.title is not None:
            
            self.tex += "\\title{" + self.title + "}\n"

        if self.author is not None:

            self.tex += "\\author{" + self.author + "}\n"

        if self.date is not False:

            self.tex += "\\date{" + self.date + "}\n"
