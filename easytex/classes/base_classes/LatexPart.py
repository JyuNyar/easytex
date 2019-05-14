class LatexPart:
    """A base class represeting a set of latex commands."""
    
    def __init__(self, tex=""):
        """
        Args
        ----
        tex: str
            A string representing latex commands to initialize in LatexPart.
        """
        self.close_command = []

        self.tex = "" + tex

    def add(self, tex):
        """
        Universal method for combining LatexParts.
        
        If two LatexPart objects are combined using ~.add(), their ~.tex
        strings are combined together.
        
        Args
        ----
        tex: str or LatexPart
            A string or LatexPart object.
        """
        if self.tex is None:

            self.tex = ""

        if isinstance(tex, LatexPart):

            self.tex += tex.tex

        else:

            self.tex += tex


    def set_close_command(self, close_command):
        """
        Universal method call for storing closing commands.
        A closing command is used to end certain latex environments.
        """
        commands = self.close_command

        if type(close_command) == list:

            self.close_command += close_command
        else:

            self.close_command.append(close_command)


    def print_tex(self):
        """Print latex commands stored in ~.tex."""
        print(self.tex)
