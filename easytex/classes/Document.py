# Import classe namespaces for class type comparisons
from .Environment import Environment
from .Figure import Figure
from .PageStyle import PageStyle
from .Preamble import Preamble
from .Section import Section
from .Table import Table
from .Text import Text
from .Columns import Columns
from .PDFs import PDFs

from .base_classes.LatexPart import LatexPart
from .base_classes.Container import Container
from ..modules.utils import _latex_special_chars, clean_tex

class Document:
    """
    This class represents a latex document.
    
    Latex parts are added to self.parts.
    
    These parts are then merged together when exported or printed.
    
    from .base_classes import LatexPart
    """

    def __init__(
        self,
        preamble,
        include_title=True,
        cover_page=False,
        table_of_contents=True,
        list_of_figures=True,
        list_of_tables=True,
    ):
        """
        Args
        ----
        preamble: Preamble
            A Preamble object.
        include_title: bool
            True: Include title, author, date in the report.
            False: Do not include title, author, date.
        table_of_contents: bool
            True: Include a table of contents.
            False: Do not include a table of contents.
        list_of_figures: bool
            True: Include a list of figures.
            False: Do not include a list of figures.
        list_of_tables: bools
            True: Include a list of tables.
            False: Do not include a list of tables.
        
        """

        if isinstance(preamble, Preamble):
            self.preamble = preamble.tex
            self.title = preamble.title

        else:
            raise ValueError("Document preamble should be a Preamble() class.")

        self.parts = []
        
        if isinstance(cover_page, bool):

            self.cover_page = True

        else:

            raise TypeError("cover_page not a boolean.")
            
        if isinstance(table_of_contents, bool):

            self.toc = table_of_contents

        else:

            raise TypeError("table_of_contents not a boolean.")

        if isinstance(list_of_figures, bool):

            self.lof = list_of_figures

        else:

            raise TypeError("list_of_figures not a boolean.")

        if isinstance(list_of_tables, bool):

            self.lot = list_of_tables

        else:

            raise TypeError("list_of_tables not a boolean.")

        if isinstance(include_title, bool):

            self.include_title = include_title

        else:

            raise TypeError("include_title not a boolean.")

        self.tex = ""

    def add_toc(self):
        """Adds the table of contents to the document. Also adds a fixed hyperlink anchor."""

        self.body += "\\addtocontents{toc}{\\protect\\hypertarget{toc}{}}"

        self.body += "\\tableofcontents\n"

    def add_list_figures(self):
        """Adds the list of figures to the document. Also adds a fixed hyperlink anchor."""

        self.body += "\\addtocontents{lof}{\\protect\\hypertarget{lof}{}}"

        self.body += "\\listoffigures\n"

    def add_list_tables(self):
        """Adds the list of tables to the document. Also adds a fixed hyperlink anchor."""

        self.body += "\\addtocontents{lot}{\\protect\\hypertarget{lot}{}}"

        self.body += "\\listoftables\n"

    def add(self, part):
        """ Adds a LatexPart to list self.Parts """
        if isinstance(part, LatexPart) is False:
            raise TypeError("Tried to add a non-LatexPart object to document.")

        if isinstance(part, Preamble) is True:
            raise TypeError(
                "Tried to add a Preamble, preamble should be specified on document creation."
            )

        if isinstance(part, Table) is True:
            if part.table_type == "tabular":
                raise TypeError(
                    "Cannot add naked tabular table to document. Encapsulate in an environment such as sidetable, or remake as table or longtable."
                )
        
        if isinstance(part, Section) is True:
            if part.type != "section":
                raise TypeError("Cannot append a subsection or a sub-subsection directly to a document; subsections should be contained within their parent section only.")
                
        self.parts += [part]

    def add_clearpage(self):
        """Adds a clearpage command to the document's body."""

        self.add(LatexPart("\n\\clearpage\n"))

    def print_map(self):
        """
        Iterates through Document.parts and runs _doc_map.
        Constructs a document map.
        """
        
        i = 1
        for part in self.parts:
            self._doc_map(part, i)
            i += 1

    def _doc_map(self, part, i, space=0):
        """
        Takes in a document part and prints out a part summary.
        Nested parts within containers are printed with an offset.
        
        Args
        ----
        part: a LatexPart
            A part of the document to print.
        i: int
            Counter.
        space:
            Number of spaces to offset the printout.
        """
        
        spacer = " " * space

        part_printed = False

        if isinstance(part, PageStyle):

            part_printed = True

            print(spacer, i, "PageStyle")
            print(
                f"""
    {spacer}    |
    {spacer}     `--| lhead: {part.lhead}
    {spacer}        | rhead: {part.rhead}
    {spacer}        | lfoot: {part.lfoot}
    {spacer}        | rfoot: {part.rfoot}
            """
            )

        if isinstance(part, Section):

            part_printed = True

            print(spacer, i, "Section")
            print(
                f"""
    {spacer}    |
    {spacer}     `--| Type: {part.type}
    {spacer}        | Name: {part.name}
            """
            )

        if isinstance(part, Environment):
            
            part_printed = True

            print(spacer, i, "Environment")

            for env in part.type:
                print(
                    f"""
    {spacer}    |
    {spacer}     `--| {env}
                """
                )

        if isinstance(part, Table):

            part_printed = True

            print(spacer, i, "Table")
            print(
                f"""
    {spacer}    |
    {spacer}     `--| caption: {part.caption}
    {spacer}        | label: {part.label}
    {spacer}        | Data: {part.data.shape}
            """
            )

        if isinstance(part, Figure):

            part_printed = True

            print(spacer, i, "Figure")
            print(
                f"""
    {spacer}    |
    {spacer}     `--| caption: {part.caption}
    {spacer}        | label: {part.label}
    {spacer}        | figure: {part.figure}
            """
            )

        if isinstance(part, Text) and part_printed is False:
            
            part_printed = True
                
            text = part.tex
            text = text.replace('\n', '')
            text = text[0:20] + '...'

            print(spacer, i, "Text")
            print(
                f"""
    {spacer}    |
    {spacer}     `--| Contains: {text}
            """
            )
            
        if isinstance(part, Container):

            part_printed = True
            
            ii = 1
            for child in part.children:
                self._doc_map(child, ii, space + 8)
                ii += 1
                
        if isinstance(part, LatexPart) and part_printed is False:
            text = part.tex
            text = text.replace('\n', '')
            text = text[0:20] + '...'
            
            print(spacer, i, "LatexPart")
            print(
                f"""
    {spacer}    |
    {spacer}     `--| Contains: {text}
            """
            )
        
        if isinstance(part, Columns):
            part_printed = True

            print(spacer, i, "Column")

            num_cols = part.num_cols
            print(
                f"""
    {spacer}    |
    {spacer}     `--| Column: {num_cols}
                """
                )
            
            ii = 1
            
            for child in part.data:
                self._doc_map(child, ii, space + 8)
                ii += 1
                
        if isinstance(part, PDFs):
            part_printed = True

            print(spacer, i, "Pages")
            
            print(
                f"""
    {spacer}    |
    {spacer}     `--| Pages: {len(part.data)}
                """
                )
            
            ii = 1
            
            for child in part.data:
                self._doc_map(child, ii, space + 8)
                ii += 1
                
    def merge_parts(self):
        """
        Iterates through Document.parts and combines each part's .tex contents
        into Document.tex.
        
        This is used by both ~.export_tex() and ~.print_tex().
        
        Ensures that nested LatexParts are properly unpacked and merged.
        """
        parts = self.parts

        self.body = "\n\n\\begin{document}\n"
        
        if self.include_title is True:
            if self.title is not None:
                self.body += "\n\\maketitle\n\n"
        
        if self.cover_page is True:
            self.body += '\\clearpage\n'
            
        if self.toc is True:
            self.add_toc()

        if self.lof is True:
            self.add_list_figures()

        if self.lot is True:
            self.add_list_tables()

        for part in parts:

            if isinstance(part, Container):
                self.body += part.unpack(part)
            else:
                self.body += part.tex

        self.body += "\n\n\\end{document}\n"

        self.tex = self.preamble + self.body

    def print_tex(self):

        self.merge_parts()

        print(self.tex)

        self.tex = ""

    def export_tex(self, file="output.tex"):
        """
        Adds an end document command if end_doc is False, and sets the end_doc flag to True.
        Combines document's preamble and body and then saves to 'output.tex' in the local directory.
        """

        self.merge_parts()

        with open(f"{file}", "w+") as output:

            output.write(self.tex)

            output.close()

        self.tex_path = file

    def render_report(self, destination):
        """
        Renders a pdf file from a specified tex file (tex_file),
        and moves the rendered pdf to 'destination'.

        Args
        ----
        tex_file: str
            A string representing the tex file to be processed.
        destination: str
            A string representing the pdf files final name.
        """

        import subprocess
        import shutil
        import os
        
        self.export_tex("output.tex")
        
        # Tex should be ran three times to ensure TOC and references are propery generated.

        tex_file = self.tex_path

        for i in range(0, 3, 1):

            try:
                subprocess.call(["xelatex", tex_file])

            except Exception:

                raise

        # Move rendered pdf
        start = tex_file.rfind("/") + 1

        end = tex_file.rfind(".")

        tex_file = tex_file[start:end] + ".pdf"

        shutil.move(tex_file, f"{destination}")

        # Clean up temporary files
        os.remove("output.aux")

        os.remove("output.log")

        os.remove("output.out")

        os.remove("output.tex")

        try:

            os.remove("output.toc")

        except:

            pass
