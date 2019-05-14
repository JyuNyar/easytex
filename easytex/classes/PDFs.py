from collections import UserList
from .base_classes.Container import Container

class PDFs(Container, UserList):
    """ 
    Used to add one or more external pdf files to document.
    
    Args:
    ------
    
    """

    def __init__(self, arg, rotation=None, scale=None):
        """
        Args
        ----
        arg: int or list
            Int specifying the number of pdf files to add or
            a list of pdf filenames.
        rotation: int or list
            degrees
        table_of_contents: bool
            Int specifying the number of pdf files to add or
            a list ints specifying the degrees of rotation. 
        """
        Container.__init__(self, child=None)
        UserList.__init__(self)
        
        if isinstance(rotation, int) is True:
            self.rotation = [0] * arg
                    
        elif isinstance(arg, list):
            self.rotation = rotation
            
        else:
            self.rotation = None
            
        if isinstance(scale, float) is True:
            self.scale = [1.0] * arg
                    
        elif isinstance(scale, list):
            self.scale = scale
            
        else:
            self.scale = None
            
        if isinstance(arg, int) is True:
            if arg <= 0:
                raise ValueError('Number of columns must be >= 1.')
            else:
                self.data = [None] * arg
                    
        elif isinstance(arg, list):
            self.data = arg
                
        else:
            raise TypeError("""
            Pages class requires either: an int specifying the number of columns,
            or a list of column contents.
            """)

    def unpack(self, container):
        """
        Masks base class Container unpack method.
        Recursively checks passed Container and unpacks tex.
        """
        
        tex = ""
        
        i = 1
        
        if self.rotation is None:
            self.rotation = [0] * len(self.data)
            
        elif len(self.rotation) != len(self.data):
            raise ValueError('Rotation and Data are of different lengths.')
            
        if self.scale is None:
            self.scale = [1.0] * len(self.data)
            
        elif len(self.scale) != len(self.data):
            raise ValueError('Scale and Data are of different lengths.')
        
        elif all(i <= 1.0 for i in self.scale) is False or all(i > 0.0 for i in self.scale) is False:
            raise ValueError('Scale must be between 0 and 1.')
            
        for child, rotation, scale in zip(self.data, self.rotation, self.scale):
            if isinstance(child, str) is True:
                tex += "\\includepdf[pages=1-, angle=" + str(rotation) + ", scale=" + str(scale) + "]{" + child + "}\n"
            else:
                raise TypeError('Expected Pages items to be str.')

        return tex + '\n'
    