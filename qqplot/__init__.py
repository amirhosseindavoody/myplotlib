import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


def qq_plot(
    dataframe: pd.DataFrame,
    groups: list[str],
    value: str,
    ax: plt.Axes = None,
    fit_line=True,
):
    if ax is None:
        fig, ax = plt.subplots()

    for label, grouped_df in dataframe.groupby(groups):
        (osm, osr), (slope, intercept, r) = stats.probplot(
            grouped_df[value], dist="norm", fit=True
        )
        line = ax.plot(osm, osr, "o", label=label)
        if fit_line:
            ax.plot(osm, slope * osm + intercept, "-", color=line[0].get_color())

    ax.set_xlabel("Theoretical quantiles")
    ax.set_ylabel(value)
    ax.set_title("QQ Plot")

    ax.legend()

    return ax
