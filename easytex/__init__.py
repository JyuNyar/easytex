from .classes.Document import Document
from .classes.Preamble import Preamble
from .classes.Section import Section
from .classes.Figure import Figure
from .classes.Environment import Environment
from .classes.Table import Table
from .classes.PageStyle import PageStyle
from .classes.Text import Text
from .classes.Columns import Columns
from .classes.PDFs import PDFs

from .classes.base_classes.LatexPart import LatexPart
from .classes.base_classes.Container import Container

from .modules.report_functions import (
    make_table,
    make_sideways_table,
    make_row_colors_dict,
)

# A bit of a hack
from os import path

resources_dir = path.join(path.dirname(__file__), "parts/preamble.tex")