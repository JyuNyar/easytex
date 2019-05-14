import os
import warnings
import subprocess
import shutil
import pandas as pd
import numpy as np
from ..classes.Table import Table
from ..classes.Environment import Environment


def make_table(
    dataframe,
    table_type="table",
    caption=None,
    label=None,
    zebra=False,
    row_colors={},
    mid_rule=False,
    mid_rule_color=None,
    link_target=None,
):
    """
    Deprecated. use Table.make_table() instead.
    
    Returns a latex table from a pandas dataframe.
    
    
    Args
    ----
    dataframe: pandas.DataFrame
        A dataframe to be converted to latex.
    table_type: str
        The type of table to be created
    caption: str
        The table caption.
    label: str
        The table label for cross referencing.
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
    
    warnings.warn("Deprecated - use Table.make_table() instead.", UserWarning)
    
    if zebra is True and len(row_colors) > 0:

        raise ValueError("zebra and row_colors are mutually exclusive.")

    cols = [dataframe.index.name] + dataframe.columns.tolist()

    table = Table(
        table_type=table_type,
        cols=cols,
        label=label,
        row_colors=row_colors,
        link_target=link_target,
    )

    table.mid_rule = mid_rule_color

    table.mid_rule_color = mid_rule_color

    if caption is not None:
        table.add_caption(caption)

    if label is not None:

        table.add_label(label)

    if zebra is True:

        table.add_zebra()

    table.set_alignment()

    table.add_toprule()

    table.add_table_header()

    table.fill_table(dataframe)

    table.add_table_foot()

    return table


# def make_longtable(
#     dataframe,
#     caption=None,
#     label=None,
#     zebra=False,
#     row_colors={},
#     mid_rule=False,
#     mid_rule_color=None,
#     link_target=None
# ):
#     """
#     Returns a latex longtable from a pandas dataframe.

#     Args
#     ----
#     dataframe: pandas.DataFrame
#         A dataframe to be converted to latex.
#     caption: str
#         The table caption.
#     label: str
#         The table label for cross referencing.
#     zebra: bool
#         Boolean representing whether the table should be zebra stripped or not.
#     row_colors: dict
#         Dictionary mapping row indexes to row color names.
#     mid_rule: bool
#         Boolean representing whether the table should have midrules between rows.
#     mid_rule_color: str
#         The color name the table's midrule lines should be.
#     link_target:str
#         A string representing an href anchor label the figure should link to.
#     """

#     if zebra is True and len(row_colors) > 0:

#         raise ValueError("zebra and row_colors are mutually exclusive.")

#     cols = [dataframe.index.name] + dataframe.columns.tolist()

#     table = Table(
#         table_type="longtable",
#         cols=cols,
#         label=label,
#         link_target=link_target,
#         row_colors=row_colors
#     )

#     table.mid_rule = mid_rule

#     table.mid_rule_color = mid_rule_color

#     if zebra is True:
#         table.add_zebra()

#     table.set_alignment()

#     if caption is not None:
#         table.add_caption(caption)

#     if label is not None:
#         table.add_label(label)

#     table.add_toprule()

#     table.add_table_header()

#     table.fill_table(dataframe)

#     table.add_table_foot()

#     return table


def make_row_colors_dict(df, in_values, column=None, color=None):
    """
    This function takes in a dataframe and returns a dictionary
    where the dict.keys are dataframe indexes, and the values are a user specified color.
    
    To be used in conjuction with make_table like functions to highlight table rows
    based on a conditional.
    
    Args
    ----
    df: pandas.DataFrame
        A dataframe 
    column: str
        A column name to be filtered.
    in_values: list-like
        A list of values to filter column on.
    color: str
        A latex interpretable color string (a color name or color!value)
    """

    if type(in_values) == list:

        idxs = list(df[df[column].isin(in_values)].index)

    elif isinstance(in_values, pd.Series):
        if isinstance(in_values.tolist()[0], bool):

            idxs = list(df[in_values].index)

    else:
        raise ValueError("in_values not a list or a pandas boolean series.")

    row_colors = {}

    for idx in idxs:

        row_colors[idx] = color

    return row_colors


def make_sideways_table(
    dataframe,
    caption=None,
    label=None,
    zebra=False,
    row_colors={},
    mid_rule=False,
    mid_rule_color=None,
    link_target=None,
):
    """
    Returns a latex sideways table from a pandas dataframe.
    
    Args
    ----
    dataframe: pandas.DataFrame
        A dataframe to be converted to latex.
    caption: str
        The table caption.
    label: str
        The table label for cross referencing.
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
    
    warnings.warn("Deprecated - use Table.make_table() instead.", UserWarning)
    
    table = make_table(
        dataframe=dataframe,
        table_type="tabular",
        zebra=False,
        label=label,
        row_colors=row_colors,
        mid_rule=mid_rule,
        mid_rule_color=mid_rule_color,
        link_target=link_target,
    )

    side_environment = Environment()

    side_environment.add_sidewaystable()

    adjust_box = Environment()

    adjust_box.add_adjustbox()

    adjust_box.add_tex(table.tex)

    adjust_box.add_env_close()

    adjust_box.add_tex("\\captionsetup{labelformat=empty}\n")

    adjust_box.add_tex("\\caption{" + caption + "}\n")

    side_environment.add_tex(adjust_box.tex)

    side_environment.add_env_close()

    return side_environment


# def render_report(tex_file, destination):
#     """
#     Renders a pdf file from a specified tex file (tex_file),
#     and moves the rendered pdf to 'destination'.

#     Args
#     ----
#     tex_file: str
#         A string representing the tex file to be processed.
#     destination: str
#         A string representing the pdf files final name.
#     """

#     # Tex should be ran three times to ensure TOC and reference are propery generated.
#     for i in range(0, 3, 1):

#         try:
#             subprocess.call(["xelatex", tex_file])

#         except Exception:

#             raise

#     # Move rendered pdf
#     start = tex_file.rfind("/") + 1

#     end = tex_file.rfind(".")

#     tex_file = tex_file[start:end] + ".pdf"

#     shutil.move(tex_file, f"{destination}")

#     # Clean up temporary files
#     os.remove("output.aux")

#     os.remove("output.log")

#     os.remove("output.out")

#     os.remove("output.tex")

#     try:

#         os.remove("output.toc")

#     except:

#         pass
