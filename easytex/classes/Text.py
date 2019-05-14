from .base_classes.LatexPart import LatexPart
from ..modules.utils import _latex_special_chars, clean_tex
 
class Text(LatexPart):
    """
    A class representing latex body text.
    """
 
    def __init__(self, text, raw=False, verbatim=False):
        """
        Args
        ----
        text: str
            Text to be added to the Text class. 
        """
        
        LatexPart.__init__(self)
        
        if isinstance(raw, bool):
            self.raw = raw
            
        if isinstance(text, str):
            if verbatim is True:
                self.add_verbatim(text)
            else:
                if self.raw is False:
                    self.add(clean_tex(text))
                else:
                    self.add(text)
        
        if isinstance(text, dict):
            self.add_list(text)
            
    def add_verbatim(self, text):
        """
        Add verbatim (as-is) text to the document. 
        Useful for code blocks.
        """
        
        if isinstance(text, str) is False:
            t = type(text)
            raise TypeError(f'Expected string, got {t}.')
            
        self.add('\n\\begin{verbatim}\n')
        self.add(text)
        self.add('\n\\end{verbatim}\n')
    
    def add_list(self, list_items, bullets=False):
        """
        Adds a list environment with values from list_items.
        
        Args
        ----
        list_items: dict
            Dictionary of list items. Keys are the list entries, value are the list level.
        bullets: bool
            Boolean for whether the list markers should be bullets (True) or numbers (False).
        """
        
        t = type(list_items)
        if isinstance(list_items, dict) is False:
            raise TypeError(f'list_items expected to be dict, instead got {t}')
        
        self.add("\\Activate\n")
        
        if bullets is True:
            self.add("\\begin{easylist}[itemize]\n")
            self.add("\\ListProperties(Hang=true, Progressive=4ex)\n")
        else:
            self.add("\\begin{easylist}[enumerate]\n")
            self.add("\\ListProperties(Hang=true, Progressive=4ex)\n")
        
        for entry in list_items:
            if self.raw is False:
                self.add('&' * list_items[entry] + ' ' + clean_tex(entry) + '\n')
            else: 
                self.add('&' * list_items[entry] + ' ' + entry + '\n')
                
        self.add('\\end{easylist}\n')
        
        self.add("\\Deactivate\n\n")
 
    def add_bold(self, text):
        """Add bold text to the Text environment."""
        
        if isinstance(text, str) is False:
            t = type(text)
            raise TypeError(f'Expected string, got {t}.')
            
        self.add('\\textbf{' + clean_tex(text) + '}')
        