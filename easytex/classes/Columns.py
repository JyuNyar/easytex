from collections import UserList
from .base_classes.Container import Container

class Columns(Container, UserList):
    """ 
    Currently only supports adjustbox and sidewaystable.
    
    """

    def __init__(self, arg):

        Container.__init__(self, child=None)
        UserList.__init__(self)
        
        
        if isinstance(arg, int) is True:
            if arg <= 0:
                raise ValueError('Number of columns must be >= 1.')
            else:
                self.num_cols = arg
                self.data = [None] * arg
                    
        elif isinstance(arg, list):
            self.data = arg
            self.num_cols = len(arg)
                
        else:
            raise TypeError("""
            Columns class requires either: an int specifying the number of columns,
            or a list of column contents.
            """)

    def unpack(self, container):
        """
        Masks base class Container unpack method.
        Recursively checks passed Container and unpacks tex.
        """
        
        tex = "\n\\begin{multicols}{" + str(self.num_cols) + "}\n"
        
        i = 1
        
        for child in self.data:
            if isinstance(child, Container) is True and isinstance(child, UserList) is False:
                if i < self.num_cols:
                    tex += child.unpack(child) + "\n\n\\columnbreak\n\n"
                else:
                    tex += child.unpack(child)
            else:
                if i < self.num_cols:
                    tex += child.tex  + "\n\n\\columnbreak\n\n"
                else:
                    tex += child.tex
            i += 1
        
        return tex + "\n\\end{multicols}"