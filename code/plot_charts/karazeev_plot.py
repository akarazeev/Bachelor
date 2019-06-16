import matplotlib.pyplot as plt
import numpy as np
from db_communication import db_queries


def simple_plot(file_id, col_1, col_2):
    df = db_queries.get_dataframe(file_id)

    filename = "simple_plot_{}_{}_{}.png".format(file_id, col_1, col_2)
    path = "./images/{}".format(filename)

    x = df[col_1]
    y = df[col_2]

    # Necessary data are received.

    fig, axes = plt.subplots(1, 2)
    plt.subplots_adjust(wspace=0.5)
    fig.set_figheight(7)
    fig.set_figwidth(15)

    axes[0].plot(x, y, label="f({}) = {}".format(col_1, col_2))
    axes[0].legend(loc="upper right")
    axes[0].set_xlabel(col_1, fontsize=15)
    axes[0].set_ylabel(col_2, fontsize=15)

    axes[1].scatter(x, y, label="f({}) = {}".format(col_1, col_2))
    axes[1].legend(loc="upper right")
    axes[1].set_xlabel(col_1, fontsize=15)
    axes[1].set_ylabel(col_2, fontsize=15)

    fig.savefig(path)
    axes[0].clear()
    axes[1].clear()

    return filename


def simple_anomalies(file_id, col_1, col_2):
    df = db_queries.get_dataframe(file_id)

    filename = "simple_anomalies_{}_{}_{}.png".format(file_id, col_1, col_2)
    path = "./images/{}".format(filename)

    x = df[col_1]
    y = df[col_2]

    # Necessary data are received.

    data = x
    outliers_portion = 1

    fig, axes = plt.subplots()
    plt.subplots_adjust(left=0.2)
    fig.set_figheight(7)
    fig.set_figwidth(10)

    positive_indexes = np.array(list(enumerate(data)))[data > 0][:, 0].astype(int)
    negative_indexes = np.array(list(enumerate(data)))[data < 0][:, 0].astype(int)
    zeros_indexes = np.array(list(enumerate(data)))[data == 0][:, 0].astype(int)  # ???

    outliers_indexes = list()

    if len(positive_indexes) / len(data) < outliers_portion:
        outliers_indexes.extend(list(positive_indexes))
    elif len(negative_indexes) / len(data) < outliers_portion:
        outliers_indexes.extend(list(negative_indexes))

    colors = np.zeros(len(data))
    colors[outliers_indexes] = np.ones(len(outliers_indexes))

    # axes.title('Sign feature. max portion={}'.format(outliers_portion))
    axes.scatter(np.arange(len(data)), data, c=colors)
    axes.set_xlabel("Элементы", fontsize=15)
    axes.set_ylabel(col_1, fontsize=15)

    fig.savefig(path)
    axes.clear()

    return filename
