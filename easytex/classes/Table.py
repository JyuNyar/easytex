import pandas as pd
from .base_classes.LatexPart import LatexPart
from ..modules.utils import _latex_special_chars, clean_tex

class Table(LatexPart):
    """
    This class represents a latex table.
    
    Currently three primary tables are implemented:
        Table: pass 'table' to Table.table_type
        Tabular: pass 'tabular' to Table.table_type
        Longtable: pass 'longtable' to Table.table_type
        
    See init for more details.
    """

    def __init__(
        self,
        table_type,
        label,
        data=None,
        cols=[],
        caption=None,
        captionof=None,
        empty_label=False,
        alignment=None,
        zebra=False,
        row_colors={},
        mid_rule=False,
        mid_rule_color=None,
        link_target=None,
    ):

        """
        Args
        ----
        table_type: str
            Must be 'table', 'tabular', 'longtable'
            Designates the type of tabular environment used.
        label: str
            A string represnting the table's cross reference label
        data: pd.DataFrame or list
            A pandas dataframe or list object to convert into a latex table.
        cols: list
            List of column names. Used to generate an appropriately sized table.
        caption: str
            A string representing the table's caption.
        captionof: str
            A string representing the table's caption. To be used outside of a float environment.
        empty_label: bool
            A flag representing whether to use a blank caption.
        alignment: str
            A string representing a latex tabular alignment command.
            Used to overwrite default alignment.
        zebra: bool
            Boolean representing whether the table should be zebra stripped or not.
        row_colors: dict
            Dictionary mapping row indexes to row color names.
        mid_rule: bool
            Boolean representing whether the table should have midrules between rows.
        mid_rule_color: str
            The color name the table's midrule lines should be.
        link_target:str
            A string representing an href anchor label the figure should link to.
        """

        LatexPart.__init__(self)

        if zebra is True and len(row_colors) > 0:

            raise ValueError("zebra and row_colors are mutually exclusive.")

        self.table_type = table_type

        self.label = str(label)

        self.data = data

        self.row_colors = row_colors

        self.caption = str(caption)

        self.captionof = captionof

        self.link_target = link_target

        self.empty_label = empty_label
        
        self.multi_column = None
        
        self.multi_index = None
        
        if isinstance(data, pd.DataFrame):
            
            cols = self.get_columns(data)
            
            cols = [col if col is not None else "" for col in cols]
            
        self.cols = cols

        self.num_cols = len(self.cols)

        self.alignment = None

        self.add_table_environment()

        self.mid_rule = mid_rule

        self.mid_rule_color = mid_rule_color

        self.zebra = zebra

        if data is not None:

            self.make_table()

    def make_table(self):

        if self.zebra is True:
            self.add_zebra()

        if self.table_type == "longtable":
            self.set_alignment()

            if self.caption is not None:
                self.add_caption(self.caption)

            if self.label is not None:
                self.add_label(self.label)

        elif self.table_type in ["table", "tabular"]:
            if self.caption is not None:
                self.add_caption(self.caption)

            if self.label is not None:
                self.add_label(self.label)

            self.set_alignment()

        elif self.table_type in ["sidewaystable"]:
            self.add("\\begin{sidewaystable}\n")

            if self.caption is not None:
                self.add_caption(self.caption)

            self.add(
                "\\begin{adjustbox}{max width=1.0\\textheight, max totalheight=1.0\\linewidth}\n\n"
            )

            if self.label is not None:
                self.add_label(self.label)

            self.set_alignment()

        self.add_toprule()

        self.add_table_header()

        self.fill_table(self.data)

        self.add_table_foot()

        if self.table_type == "sidewaystable":
            self.add("\\end{adjustbox}\n")
            self.add("\\end{sidewaystable}\n")

    def add_centering(self):
        """Add a centering command."""

        self.add("\\centering\n")

    def add_toprule(self):
        """Add a toprule (line at the top of the table) command."""

        self.add("\\toprule\n")

    def add_midrule(self):
        """
        Add a midrule command.
        Color is set by mid_rule_color property.
        """

        if self.mid_rule_color is not None:

            self.add("\\arrayrulecolor{" + self.mid_rule_color + "}")

        self.add("\\midrule\n")

        self.add("\\arrayrulecolor{black}")

    def add_bottomrule(self):
        """Add a bottomrule command."""

        self.add("\\bottomrule\n")

    def add_caption(self, caption, captionof=None, empty_label=None):
        """
        Add a caption to the table.
        
        Args
        ----
        caption: str
            A string representing the table's caption.
        captionof: str
            A string representing the table's caption. To be used outside of float environments.
        empty_label: bool
            A boolean representing whether the table caption should be blank.
        """
        
        if self.table_type == 'tabular':
            captionof = 'table'
            
        if empty_label is True:
            self.add("\\captionsetup{labelformat=empty}\n")
        
        if captionof is None:

            if self.link_target is not None:

                self.add(
                    "\\caption["
                    + caption
                    + "]{\\hyperlink{"
                    + self.link_target
                    + "}{"
                    + caption
                    + "}}\n"
                )

            else:
                self.add("\\caption{" + caption + "}\n")

        else:
            if self.link_target is not None:

                self.add(
                    "\\captionof{"
                    + captionof
                    + "}["
                    + caption
                    + "]{\\hyperlink{"
                    + self.link_target
                    + "}{"
                    + caption
                    + "}}\n"
                )

            else:
                self.add("\\captionof{" + captionof + "}{" + caption + "}\n")

    def add_label(self, label):
        """
        Adds a label command.
        
        Args
        ----
        label: str
            A string representing a table's label.
        """

        self.label = label
        
        if self.table_type in ["tabular", "table"]:
            self.add("\\label{" + label + "}\n")
        else:
            # Necessary for longtable to render properly
            self.add("\\label{" + label + "}\\\\\n")

    def add_zebra(self):
        """
        Adds zebra stripping to the table.
        Should not be used in conjunction with row colors.
        """

        self.add("\\rowcolors{1}{white}{gray!15}\n")

    def set_row_colors(self, color_dict):
        """
        Merges Table.row_colors with color_dict.
        
        Args
        ----
        color_dict: dict
            A dictionary with table index values as keys, and row colors as values.
            Rows with a given index will be colored according to the corresponding color in color_dict.
        """
        
        self.row_colors = {**self.row_colors, **color_dict}


    def add_row(self, iterable):
        """
        Adds a row represented as an iterable to the table.
        
        Args
        ----
        iterable: iterable/list-like object
            An iterable representing a row of data from a table.
        """
        
        try:
            is_iterable = iter(iterable)
        except TypeError:
            raise TypeError("Passed row value not iterable.")
        
        if self.alignment is None:
            self.set_alignment()
        
        prev_idx = ""

        idx = iterable[0]

        # Set row color based on index -> color mapping
        # Checks if current index has any values in color_rows dictionary
        # if True, sets row color

        if idx in self.row_colors.keys():

            self.add("\\rowcolor{" + self.row_colors[idx] + "}\n")

        if prev_idx == idx:

            idx = ""

        else:

            prev_idx = idx

        if self.multi_index is not None:
            for i in idx:
                i = clean_tex(i)
                self.add("\\textbf{" + str(i) + "} & ")
                
        else:
            idx = clean_tex(idx)
            self.add("\\textbf{" + str(idx) + "} & ")
                
        clean_values = []

        for item in iterable[1:]:
            
            item = clean_tex(item)
            
            clean_values.append(item)

        self.add(" & ".join(str(value) for value in clean_values) + " \\\\\n")

    def get_columns(self, dataframe):
        
        cols = list(dataframe.index.names)
        
        if isinstance(dataframe.columns, pd.MultiIndex):
            self.multi_index = dataframe.index
    
        if isinstance(dataframe.columns, pd.MultiIndex):
            self.multi_column = dataframe.columns
            try:
                cols += dataframe.columns.codes[len(dataframe.columns.levels)-1].tolist()
            except:
                cols += dataframe.columns.labels[len(dataframe.columns.levels)-1].tolist()
        else:
            cols += dataframe.columns.tolist()

        return cols
    
    def set_columns(self, cols):
        """
        Sets table column.
        
        Args:
        ----
        cols: list
            A list of column names.
        """

        if type(cols) is list:
            self.cols += cols
        else:
            self.cols.append(cols)

        self.num_cols = len(cols)

    def set_alignment(self, alignment=None):
        """
        Sets the table's column alignment.
        Used to overwrite default column alignment.
        
        Args
        ----
        alignment: str
            A string representing a latex tabular alignment command.
        """

        # Default alignment:
        if alignment is None:
            if self.multi_column is not None:
                self.alignment = "{l" + "r" * (self.num_cols - 1) + "}\n"
            else:
                self.alignment = "{l" + "r" * (self.num_cols - 1) + "}\n"
        
        else:
            self.alignment = alignment + "\n"
        
        if self.table_type == "table":
            table_type = "tabular"

        # Overwrite defaults:
        else:
            table_type = self.table_type
            
            if table_type == "sidewaystable":
                table_type = "tabular"

        self.add("\\begin{" + table_type + "}" + self.alignment)

    def add_table_environment(self):
        """Adds a table, tabular or longtable environment based on table_type."""

        if self.table_type == "table":
            self.add("\\begin{table}[!h]\n\\centering\n")
        
        elif self.table_type == "tabular":
            self.add("\n")
        
        elif self.table_type == "longtable":
            self.add("\n")
        
        elif self.table_type == "sidewaystable":
            self.add("\n")
        
        else:
            raise ValueError(
                "table_type must be 'table', 'sidewaystable', 'tabular' or 'longtable'."
            )
    
    # This 'works', but probably needs to be refactored into something more clear.
    def create_multi_column_string(self):
        """Creates column string; allows for multi-index dataframes."""
        
        col_header = ""

        for i in range(0, len(self.multi_column.levels)):
            
            try:
                end_column = len(self.multi_column.codes[i])
            except:
                end_column = len(self.multi_column.labels[i])
                
            index_len = len(self.multi_index.names)
            
            # Add filler slots for index names untill last column row before data:
            if i != len(self.multi_column.levels)-1:
                col_header += ' & ' * index_len
            else:
                for name in self.multi_index.names:
                    col_header += "\\textbf{" + clean_tex(name) + '} & '
                
            positions = []
            
            mid_rules = []
            
            offset = index_len
            
            try:
                position_list = self.multi_column.codes[i]
            except:
                position_list = self.multi_column.labels[i]
                
            for name_position in position_list:

                if name_position in positions and i+1 != len(self.multi_column.levels):
                    pass

                elif i+1 != len(self.multi_column.levels):
                    positions += [name_position]

                    col_name = [col_name for position, col_name in enumerate(self.multi_column.levels[i]) if position == name_position][0]

                    col_name = clean_tex(col_name)
                    
                    try:
                        count = self.multi_column.codes[i].tolist().count(name_position)
                    except:
                        count = self.multi_column.labels[i].tolist().count(name_position)
                        
                    col_header += "\\multicolumn{" + str(count) + "}{c}{\\textbf{" + str(col_name) + "}} & "
                    
                    mid_rules.append('\\cmidrule(lr){' + str(offset + 1) + '-' + str(offset+count) + '}')
                    
                    offset += count
                
                else:
                    positions += [name_position]

                    col_name = [col_name for position, col_name in enumerate(self.multi_column.levels[i]) if position == name_position][0]

                    col_name = clean_tex(col_name)
                    
                    try:
                        count = self.multi_column.codes[i].tolist().count(name_position)
                    except:
                        count = self.multi_column.labels[i].tolist().count(name_position)
                        
                    col_header += "\\textbf{" + str(col_name) + "} & "
                    
                    offset += count
                                     
            col_header = col_header[:-2] + " \\\\\n"
            
            if i+1 != len(self.multi_column.levels):
                col_header = col_header + '\n'.join(mid_rules)

        return col_header
                
    def create_column_string(self):
        
        i = 0
        
        col_header = ""
        
        for col in self.cols:

            i += 1

            col_name = str(col)

            col_name = clean_tex(col_name)

            if i == self.num_cols:
                col_header += "\\textbf{" + col_name + "} \\\\\n"
            else:
                col_header += "\\textbf{" + col_name + "} & "
                
        return col_header
    
    def add_table_header(self):
        """Adds a table header row based on passed column names."""
        
        if self.multi_column is not None or self.multi_index is not None:
            col_header = self.create_multi_column_string()
        else:
            col_header = self.create_column_string()
            
        if self.table_type == "longtable":
            
            self.add(col_header)
            
            self.add_midrule()

            # This line is necessary for zebra stripping. Resets latex internal row counter.
            # This is a way to alternate coloring even and odd rows.
            self.add("\\endfirsthead\n\\noalign{\\global\\rownum=0}\n")

            self.add_toprule()

            self.add(col_header)
            
            if self.multi_column is not None:
                self.add("\\arrayrulecolor{black}\\midrule")
            else:
                self.add_midrule()

            self.add("\\endhead\n\\noalign{\\global\\rownum=0}\n")

            self.add_midrule()

            self.add(
                "\\multicolumn{"
                + str(self.num_cols)
                + "}{c}{{Continued on Next Page\\ldots}}\\\\\n"
            )

            self.add(
                "\\endfoot\n\\bottomrule\n\\endlastfoot\n\\noalign{\\global\\rownum=1}"
            )

        else:
            self.add(col_header)
            
            if self.multi_column is not None:
                self.add("\\arrayrulecolor{black}\\midrule")
            else:
                self.add_midrule()

    def fill_table(self, dataframe):
        """
        Fills a table with data from a pandas.DataFrame.
        Columns are handled seperately.
        
        Args
        ----
        dataframe: pandas.DataFrame
            A pandas dataframe to be rendered in latex.

        """

        # Used to add midrules to non-terminal rows
        rows = dataframe.shape[0]

        row = 0

        for values in dataframe.itertuples():

            row += 1

            self.add_row(values)

#                 # This fixes a wierd floating point issue with floats
#                 if type(val) == float:
#                     try:
#                         left, right = str(val).split(".")
#                         val = left + "." + right[:3]
#                     except:
#                         pass
#                     try:
#                         val = int(val)
#                     except:
#                         pass

            if self.mid_rule is True and row < rows:

                self.add_midrule()

    def add_table_foot(self):
        """Adds latex commands to close a table."""

        if self.table_type == "table":
            self.add_bottomrule()
            self.add("\\end{tabular}\n\\end{table}\n")

        elif self.table_type in ["sidewaystable"]:
            self.add_bottomrule()
            self.add("\\end{tabular}\n")
        
        elif self.table_type in ["tabular"]:
            self.add_bottomrule()
            self.add("\\end{tabular}\n")
            
        elif self.table_type == "longtable":
            self.add("\\end{" + self.table_type + "}\n\n")

        self.add("\\rowcolors{1}{white}{white}\n")
        