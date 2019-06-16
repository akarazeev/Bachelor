import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from db_communication import db_queries


def naive_plot_df(file_id, col_1, col_2):
    df = db_queries.get_dataframe(file_id)

    filename = 'output_{}_{}_{}.png'.format(file_id, col_1, col_2)
    path = './images/{}'.format(filename)

    fig, axes = plt.subplots(2, 2)
    fig.set_figheight(8)
    fig.set_figwidth(11)
    plt.subplots_adjust(wspace=0.5, hspace=0.5)

    axes[0][0].plot(df[col_1], df[col_2], label='f({}) = {}'.format(col_1,col_2), color='blue')
    axes[0][0].set_title("Line plot")
    axes[0][0].legend(loc="upper right")
    axes[0][0].set_xlabel("Координата: {}".format(col_1), fontsize=15)
    axes[0][0].set_ylabel("Координата: {}".format(col_2), fontsize=15)

    axes[0][1].scatter(df[col_1], df[col_2], label='f({}) = {}'.format(col_1,col_2), color='blue', marker='^')
    axes[0][1].set_title("Scatter plot")
    axes[0][1].legend(loc="upper right")
    axes[0][1].set_xlabel("Координата: {}".format(col_1), fontsize=15)
    axes[0][1].set_ylabel("Координата: {}".format(col_2), fontsize=15)

    axes[1][0].plot(df[col_2], df[col_1], label='f({}) = {}'.format(col_2,col_1), color='orange')
    axes[1][0].set_title("Line plot")
    axes[1][0].legend(loc="upper right")
    axes[1][0].set_xlabel("Координата: {}".format(col_2), fontsize=15)
    axes[1][0].set_ylabel("Координата: {}".format(col_1), fontsize=15)

    axes[1][1].scatter(df[col_2], df[col_1], label='f({}) = {}'.format(col_2,col_1), color='orange', marker='^')
    axes[1][1].set_title("Scatter plot")
    axes[1][1].legend(loc="upper right")
    axes[1][1].set_xlabel("Координата: {}".format(col_2), fontsize=15)
    axes[1][1].set_ylabel("Координата: {}".format(col_1), fontsize=15)

    fig.savefig(path)
    axes[0, 1].clear()

    return filename
