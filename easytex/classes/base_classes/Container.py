from .LatexPart import LatexPart


class Container(LatexPart):
    """
    Base Class representing a LatexPart intended to contain 
    one or more other LatexParts.
    """
    
    def __init__(self, child):
        """"
        Args
        ----
        child: LatexPart
            A LatexPart to be contained within the Container.
            Can store one or many children.
        """
        
        LatexPart.__init__(self)

        self.children = []

        if child is not None:
            self.add_child(child)


    def add_child(self, child):
        """
        Adds a child LatexPart to list of contained LatexParts.
        """
        
        if isinstance(child, list) is True:
            
            for item in child:
                
                if isinstance(item, LatexPart) is False:
                    raise TypeError("Child expected to be a Latex object or list of Latex objects.")
                    
                    
        if isinstance(child, LatexPart) is False:
            raise TypeError("Child expected to be a Latex object or list of Latex objects.")
            
        if isinstance(child, list) is True:
            for item in child:
                self.children.append(item)
        else:
            self.children.append(child)
        
    def unpack(self, container):
        """
        Recursively checks passed Container and unpacks tex.
        Repeats as long as the unpacked item is another Container instance.
        This is how Containers within Containers within Containers are handled.
        
        Also properly closes any open Environment objects found.
        
        Args
        ----
        container: LatexPart
            An object represeting either a LatexPart or Container.
        
        Returns:
        tex: str
            A string of latex commands extracted from container.
        """
        
        tex = ""

        if isinstance(container, Container):

            tex = container.tex

            for child in container.children:
                
                if isinstance(child, Container):
                    tex += child.unpack(child)
                    
                else:
                    tex += self.unpack(child)

            commands = container.close_command

            commands.reverse()

            commands = "".join(command for command in commands)

            tex += commands

        else:
            tex += container.tex

        return tex


    def print_tex(self):
        """Unpacks the Container and prints its contents."""
        
        print(self.unpack(self))
