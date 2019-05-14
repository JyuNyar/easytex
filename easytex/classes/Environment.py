from .base_classes.Container import Container
from .Table import Table


class Environment(Container):
    """ 
    Currently only supports adjustbox and sidewaystable.
    
    """

    def __init__(self, child):

        Container.__init__(self, child)

        self.type = []
    
    def add_minipage(self, max_width):
        """Adds a minipage environment."""
        
        t = type(max_width)
        if isinstance(max_width, (int, float)) is False:
            raise TypeError(f'max_width expected to be int or float, got {t}')
        
        if 0 >= max_width or max_width > 1.0:
            raise ValueError("max_width should be between 0.0 and 1.0.")
        
        for child in self.children:
            if isinstance(child, Table):
                if child.table_type != 'tabular':
                    raise TypeError(f"Minipages may only encapsulate 'tabular' type tables.")
                    
        self.add('\n\\hfill\n')
        self.add(
            "\\begin{minipage}{" + str(max_width) + "\\linewidth}\n\\centering\n"
        )
        
        self.type.append('Minipage')
        
        self.set_close_command('\n\\end{minipage}\n\\hfill')
    
    def add_centering(self):
        """
        Adds centering environment.
        """
        
        command = "\n\\begin{center}\n"
        
        self.add(command)
        
        self.type.append('Centering')
        
        self.set_close_command("\n\\end{center}\n")
        
#     def add_sidewaystable(self):
#         """
#         Adds tex representing a sideways table environment.
#         Adds a tex closing command to Environment.close_command.
#         """

#         command = "\\begin{sidewaystable}\n"

#         self.add(command)

#         self.type.append("Sidewaystable")

#         self.set_close_command("\n\\end{sidewaystable}\n")

    def add_landscape(self):
        """
        Adds tex representing a landscape environment.
        Adds a tex closing command to Environment.close_command.
        """

        command = "\\begin{landscape}\n"

        self.add(command)

        self.type.append("Landscape")

        self.set_close_command("\n\\end{landscape}\n")

    def add_adjustbox(self, max_height=1.0, max_width=1.0):
        """
        Adds tex representing an adjustbox environment.
        Adds a tex closing command to Environment.close_command.
        
        Args
        ----
        max_height: float
            Float representing fraction of text height box is allowed to take up.
        max_width: float
            Float representing fraction of text width box is allowed to take up.
        """

        if "Sidewaystable" in self.type:
            raise ValueError(
                "Cannot encapsulate sidewaystable in adjustbox.\nPlease review environment."
            )

        for child in self.children:
            if isinstance(child, Table):
                if child.table_type == "longtable":
                    raise ValueError("Cannot encapsulate longtable in adjustbox.")

        self.type.append("Adjustbox")

        if max_height > 1.0:
            raise ValueError("max_height should be between 0.0 and 1.0.")

        if 0 >= max_width or max_width > 1.0:
            raise ValueError("max_width should be between 0.0 and 1.0.")

        command = (
            "\\begin{adjustbox}"
            + "{max width="
            + str(max_height)
            + "\\textheight, "
            + "max totalheight="
            + str(max_width)
            + "\\linewidth}\n"
        )

        self.add(command)

        self.set_close_command("\n\\end{adjustbox}\n")
