from .base_classes.Container import Container
from .base_classes.LatexPart import LatexPart

class Section(Container):
    """
    This class represents a latex Section.
    
    Currently only section and subsection are implemented.
    
    Section(s) can be hyperlinked back to:
        Table of Contents: pass 'toc' to Section.link_target
        List of Figures: pass 'lof' to Section.link_target
        List of Tables: pass 'lot' to Section.link_target
    
    See init for more details.
    """

    def __init__(self, section, child=None, link_target=None, level=1, numbered=True):
        """
        
        Args
        ----
        child: LatexPart
            A latexPart to be contained within the section.
        link_target: str
            A string signifying a cross-reference label to link the section to.
            Default labels include:
                toc (table of contents)
                lof (list of figures)
                lot (list of tables)
        """

        Container.__init__(self, child)

        self.link_target = link_target
        
        t = type(level)
        if isinstance(level, int) is False:
            raise TypeError(f'Expected level to be int, got {t}.')
        
        t = type(numbered)
        if isinstance(numbered, bool) is False:
            raise TypeError(f'Expected numbered to be bool, got {t}.')
            
        self.level = level
        
        self.numbered = numbered
        
        self.add_section(section)
        
    def add_section(self, section):
        """
        Adds a section to the Section object.
        
        Args:
        ----
        section: str
            A string representing the section name.
        """
        
        levels = {
            1: 'section',
            2: 'subsection',
            3: 'subsubsection'
        }
        
        self.type = levels[self.level]

        self.name = section

        if self.link_target is not None:

            self.add(
                "\n\n\\" + self.type + "["
                + section
                + "]{\\hyperlink{"
                + self.link_target
                + "}{"
                + section
                + "}}\n\n"
            )

        else:

            self.add("\n\n\\" + self.type + "{" + section + "}\n\n")

    def add(self, child):
        """Adds a LatexPart child to the Section container."""
        
        if isinstance(child, (LatexPart, Container)):
            self.add_child(child)
            
        else:
            self.tex += child
