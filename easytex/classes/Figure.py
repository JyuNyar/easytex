from .base_classes.LatexPart import LatexPart
import matplotlib.pyplot as plt

class Figure(LatexPart):
    """
    This class represents a latex Figure.
    
    Figures are not wrapped in a Figure float environment by default,
    instead a combination of minipage + adjustimage is used.
    
    This ensures that figure are limited to one page size max.
    
    If a figure environment is needed, Figure.add_tex() can be used
    to manually add a Figure float environment.
    """

    def __init__(
        self,
        label,
        figure=None,
        max_height=1.0,
        max_width=1.0,
        graphics_path=None,
        caption=None,
        empty_label=False,
        link_target=None,
    ):

        """
        Args
        ----
        label: str
            A string the figures label - used to cross-reference.
        figure: obj
            An object representing the figure being added
        max_height: float
            A float representing the proportion of max text height the figure can be.
        max_width: float
            A float representing the proportion of max text width the figure can be.
        graphics_path: str
            A string representing the path to a saved figure (if needed).
            Does not include the filename.
        caption: str
            String representing the caption to be used with the Figure.
        empty_label: bool
            A flag used to track whether caption should be empty or not.
        link_target: str
            A string representing an internal href anchor label.
            Used to link back to table of contents, lists of figures and lists of tables.
        """

        LatexPart.__init__(self)

        self.filename = ""

        if max_height <= 0 or max_height > 1.0:

            raise ValueError("max_width must be between 0.0 and 1.0.")

        self.max_height = max_height

        if max_width <= 0 or max_width > 1.0:

            raise ValueError("max_width must be between 0.0 and 1.0.")

        self.max_width = max_width

        self.figure = figure

        self.label = label

        self.graphics_path = graphics_path

        self.empty_label = empty_label

        self.closed_minipage = False

        self.link_target = link_target

        self.set_figure(figure)
        
        self.has_caption=False

        self.add(
            "\\begin{minipage}{" + str(max_width) + "\\linewidth}\n\\centering\n"
        )
        
        
        if caption is not None:
            self.add_caption(caption=caption, empty_label=empty_label)
        else:
            self.caption = caption
            
        self.add_figure()

        self.add("\\label{" + self.label + "}\n")

        self.add_close_minipage()

    def set_figure(self, figure):
        """
        Sets the Figure.figure property to either a filename, 
        or  matplotlib.figure.Figure object.
        
        Args
        ----
        figure: str or <class 'matplotlib.figure.Figure'>
            Either a string representing a saved image's filename,
            or a matplotlib.figure.Figure object.
        """

        if isinstance(figure, plt.Figure):

            try:
                if self.graphics_path is None:

                    graphics_path = ""

                else:

                    graphics_path = self.graphics_path

                filepath = graphics_path + self.label + ".pdf"

                self.filename = self.label

                figure.savefig(filepath, dpi=400, bbox_inches="tight")

                self.figure = figure

            except:

                raise

        elif type(figure) == str:

            try:
                if self.graphics_path is None:

                    graphics_path = ""

                else:

                    graphics_path = self.graphics_path

                self.filename = figure

                self.figure = figure

            except:

                raise

    def add_figure(self):
        """Adds the figure latex commands to Figure.tex."""

        if self.filename != "":

            self.add(
                "\\adjustimage{max size={\\linewidth}{"
                + str(self.max_height)
                + "\\textheight}}{"
                + self.filename
                + "}\n"
            )

    def add_caption(self, caption, empty_label=False):
        """
        Adds a caption to the figure.
        
        Args
        ----
        caption: str
            A string representing the figure caption.
        empty_label: bool
            A flag signifying whether to include a blank capation.
        """

        self.caption = caption

        if empty_label is True:

            self.add("\\captionsetup{labelformat=empty}\n")

        if caption is not None:

            if self.link_target is not None:

                self.add(
                    "\\captionof{figure}["
                    + caption
                    + "]{\\hyperlink{"
                    + self.link_target
                    + "}{"
                    + caption
                    + "}}"
                )

            else:

                self.add("\\captionof{figure}{" + caption + "}\n")

            self.has_caption = True
        else:
            pass

    def add_close_minipage(self):
        """Closes the minipage environment around the figure."""

        if self.closed_minipage is False:

            self.add("\\end{minipage}")

            self.close_minipage = True
