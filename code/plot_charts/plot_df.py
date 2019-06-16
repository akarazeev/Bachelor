import matplotlib.pyplot as plt
from db_communication import db_queries

import os


def naive_plot_df(file_id, col_1, col_2):
    df = db_queries.get_dataframe(file_id)

    if col_1 is None and col_2 is None:
        col_1 = df.columns[0]
        col_2 = df.columns[-1]

    filename = "output_{}_{}_{}_{}.png".format(
        file_id, col_1, col_2, len(os.listdir("./images/"))
    )
    path = "./images/{}".format(filename)

    fig, axes = plt.subplots(2, 1)
    fig.set_figheight(11)
    fig.set_figwidth(11)
    plt.subplots_adjust(wspace=0.5, hspace=0.5)

    axes[1].plot(
        df[col_1], df[col_2], label="f({}) = {}".format(col_1, col_2), color="blue"
    )
    axes[1].set_title("Line plot")
    axes[1].legend(loc="upper right")
    axes[1].set_xlabel("Координата: {}".format(col_1), fontsize=15)
    axes[1].set_ylabel("Координата: {}".format(col_2), fontsize=15)

    axes[0].scatter(
        df[col_1],
        df[col_2],
        label="f({}) = {}".format(col_1, col_2),
        color="blue",
        marker="^",
    )
    axes[0].set_title("Scatter plot")
    axes[0].legend(loc="upper right")
    axes[0].set_xlabel("Координата: {}".format(col_1), fontsize=15)
    axes[0].set_ylabel("Координата: {}".format(col_2), fontsize=15)

    fig.savefig(path, dpi=100, bbox_inches="tight")
    axes[0].clear()
    axes[1].clear()
    plt.close()

    return filename
