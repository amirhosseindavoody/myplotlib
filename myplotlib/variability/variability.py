# Original code by:
#       Amirhossein Davoody (amirhossein.davoody@gmail.com)


from typing import Optional

import matplotlib as mpl
import numpy as np
from matplotlib.axes import Axes
from matplotlib.transforms import Bbox
from .table import Table

import pandas as pd


def variability_chart(  # noqa: PLR0913
    ax: Axes,
    xaxis: list[tuple[str]],
    y_values: list[list[float]],
    marker_size: int = 5,
    marker: str = ".",
    table_height: float = 0.5,
    row_heights: Optional[list[float]] = None,
    line_color: str = None,
    marker_color: str = None,
    legend: str = None,
    line_width: float = 1,
    iterate_marker_color: bool = False,
):
    if marker_color is None and (not iterate_marker_color):
        marker_color = ax._get_lines.get_next_color()

    if line_color is None:
        line_color = mpl.rcParams["grid.color"]

    cols = len(y_values)

    xlow, xhigh = ax.get_xlim()
    delta_x = (xhigh - xlow) / cols

    rng = np.random.default_rng()

    for col in range(cols):
        y_vector = y_values[col]

        x_vector = rng.normal(
            loc=(0.5 + col) * delta_x, scale=0.1 / cols, size=(len(y_vector),)
        )
        ax.plot(
            x_vector,
            y_vector,
            marker=marker,
            markersize=marker_size,
            color=marker_color,
            linestyle="None",
            label=legend,
        )
        ax.axvline(col * delta_x, color=line_color, linewidth=1)

    if legend is not None:
        handles, labels = ax.get_legend_handles_labels()
        legend_dict = dict(zip(labels, handles))

        ax.legend(
            handles=legend_dict.values(),
            labels=legend_dict.keys(),
            # scatterpoints=1,
            # numpoints=1,
            # handler_map={tuple: mpl.legend_handler.HandlerTuple(ndivide=None)},
        )

    ax.set_xlim(xlow, xhigh)
    ax.set_xticks([])
    ax.set_xticklabels([])

    if xaxis is None:
        return ax

    rows = len(xaxis[0])

    # bounding box is in axis coordinate system
    bbox = Bbox([[0, -table_height], [1, 0]])

    table = Table(ax=ax, bbox=bbox)
    table.edges = "BTLR"

    # Height is in relative unites to the total height of the table.
    if row_heights is None:
        row_heights = [1.0 / rows] * rows

    colWidths = [1.0 / cols] * cols
    cell_colors = "w"
    cellLoc = "right"

    # Add the cells
    for row_index in range(rows):
        for col_index in range(cols):
            row = rows - row_index - 1
            col = col_index
            table.add_cell(
                row,
                col,
                width=colWidths[col],
                height=row_heights[row],
                text=xaxis[col][row_index],
                facecolor=cell_colors,
                loc=cellLoc,
                linewidth=line_width,
                edgecolor=line_color,
                text_kwargs={"rotation": 90},
            )

    ax.add_artist(table)

    return ax


def dataframe_variability_chart(
    df: pd.DataFrame,
    groups: list[str],
    values: list[str],
    ax: Axes,
    iterate_marker_color: bool = False,
    marker_size: int = 5,
):
    xaxis = []
    y_values = {value: [] for value in values}
    for group, grouped_df in df.groupby(groups):
        xaxis.append(group)
        for value in values:
            y_values[value].append(grouped_df[value].to_numpy())

    for value in values:
        variability_chart(
            ax=ax,
            xaxis=xaxis,
            y_values=y_values[value],
            table_height=1,
            row_heights=[1, 0.5],
            marker_size=marker_size,
            marker_color=None,
            legend=value,
            iterate_marker_color=iterate_marker_color,
        )

        # Make this none so that next iterations does not make the xaxis table.
        xaxis = None
