import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from db_communication import db_queries


# df - dataframe; col_1, col_2 - columns you want to plot
def naive_plot_df(file_id, col_1, col_2, columns=None):
    df = db_queries.get_dataframe(file_id)
    if columns is not None:
        df.columns = columns
    else:
        col_1 = col_1.lower()
        col_2 = col_2.lower()

    filename = 'output_{}_{}_{}.png'.format(file_id, col_1, col_2)
    path = './images/{}'.format(filename)
    if (df[col_1].dtype == 'int64' or df[col_1].dtype == 'float64') and (df[col_2].dtype == 'int64' or df[col_2].dtype == 'float64'):
        if len(df[col_1]) > 10:
            fig, axes = plt.subplots(2, 2)
            fig.set_figheight(7)
            fig.set_figwidth(11)
            plt.subplots_adjust(wspace=0.5, hspace=0.5)
            axes[0][0].plot(df[col_1], df[col_2], label='f({}) = {}'.format(col_1,col_2))
            axes[0][0].legend(loc="upper right")
            axes[0][0].set_xlabel(col_1, fontsize=15)
            axes[0][0].set_ylabel(col_2, fontsize=15)

            axes[0][1].scatter(df[col_1], df[col_2], label='f({}) = {}'.format(col_1,col_2))
            axes[0][1].legend(loc="upper right")
            axes[0][1].set_xlabel(col_1, fontsize=15)
            axes[0][1].set_ylabel(col_2, fontsize=15)

            axes[1][0].plot(df[col_2], df[col_1], label='f({}) = {}'.format(col_2,col_1))
            axes[1][0].legend(loc="upper right")
            axes[1][0].set_xlabel(col_2, fontsize=15)
            axes[1][0].set_ylabel(col_1, fontsize=15)

            axes[1][1].scatter(df[col_2], df[col_1], label='f({}) = {}'.format(col_2,col_1))
            axes[1][1].legend(loc="upper right")
            axes[1][1].set_xlabel(col_2, fontsize=15)
            axes[1][1].set_ylabel(col_1, fontsize=15)

            fig.savefig(path)
            axes[0, 1].clear()

        else:
            bar = df.plot.bar()
            fig = bar.get_figure()
            fig.savefig(path)
            plt.clf()
    elif (df[col_1].dtype == 'O' and (df[col_2].dtype == 'int64' or df[col_2].dtype == 'float64')) or (df[col_2].dtype == 'O' and (df[col_1].dtype == 'int64' or df[col_1].dtype == 'float64')):
        if df[col_1].dtype == 'O':
            if df[col_1].nunique() <= 5:
                pie = df.plot.pie(x=col_1, y=col_2, labels=df[col_1], autopct='%1.1f%%', shadow=True, startangle=90)
                fig = pie.get_figure()
                fig.savefig(path)
                plt.clf()
            else:
                bar = df.plot.bar(x=col_1, y=col_2, rot=0)
                fig = bar.get_figure()
                fig.savefig(path)
                plt.clf()
        else:
            if df[col_2].nunique() <= 5:
                pie = df.plot.pie(x=col_2, y=col_1, labels=df[col_2], autopct='%1.1f%%', shadow=True, startangle=90)
                fig = pie.get_figure()
                fig.savefig(path)
                plt.clf()
            else:
                bar = df.plot.bar(x=col_2, y=col_1, rot=0)
                fig = bar.get_figure()
                fig.savefig(path)
                plt.clf()

    return filename
