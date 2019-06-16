import matplotlib.pyplot as plt
from db_communication import db_queries
import numpy as np
from sklearn.manifold import TSNE
from pyod.utils.data import get_outliers_inliers

from pyod.models.knn import KNN
from pyod.models.pca import PCA
from pyod.models.ocsvm import OCSVM
from pyod.models.lof import LOF
from pyod.models.hbos import HBOS
from pyod.models.iforest import IForest
from pyod.models.so_gaal import SO_GAAL
from pyod.models.mo_gaal import MO_GAAL

from pyod.utils.utility import standardizer, precision_n_scores

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score


def simple_plot(file_id, col_1, col_2):
    df = db_queries.get_dataframe(file_id)

    filename = "simple_plot_{}_{}_{}.png".format(file_id, col_1, col_2)
    path = "./images/{}".format(filename)

    x = df[col_1]
    y = df[col_2]

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

    fig.savefig(path, dpi=100, bbox_inches="tight")
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

    outliers_indexes = list()

    if len(positive_indexes) / len(data) < outliers_portion:
        outliers_indexes.extend(list(positive_indexes))
    elif len(negative_indexes) / len(data) < outliers_portion:
        outliers_indexes.extend(list(negative_indexes))

    colors = np.zeros(len(data))
    colors[outliers_indexes] = np.ones(len(outliers_indexes))

    axes.scatter(np.arange(len(data)), data, c=colors)
    axes.set_xlabel("Элементы", fontsize=15)
    axes.set_ylabel(col_1, fontsize=15)

    fig.savefig(path, dpi=100, bbox_inches="tight")
    axes.clear()

    return filename


algo_mapping = {
    "KNN": KNN,
    "PCA": PCA,
    "OCSVM": OCSVM,
    "LOF": LOF,
    "HBOS": HBOS,
    "IFOREST": IForest,
    "SO-GAAL": SO_GAAL,
    "MO-GAAL": MO_GAAL,
}

random_state = np.random.RandomState(42)


def analyze_selected_algorithm(file_id, dataset_title, selected_algortihm):
    clf_name = selected_algortihm.split()[-1].strip("()")
    mat = db_queries.get_dataframe(file_id)
    filename = "analyze_{}_{}.png".format(file_id, clf_name)
    path = "./images/{}".format(filename)

    mat = mat.drop(["Unnamed: 0", "Index", "id", "Id"], axis=1, errors="ignore")

    y = mat["outlier"].values
    X = mat.drop("outlier", axis=1).values
    X_embedded = TSNE(n_components=2).fit_transform(X)

    outliers_fraction = np.count_nonzero(y) / len(y)

    b = np.arange(X.shape[0]).reshape((X.shape[0], 1))
    X = np.hstack((X, b))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=random_state
    )
    train_ids = X_train[:, -1].astype(int)
    X_train = X_train[:, :-1]
    test_ids = X_test[:, -1].astype(int)
    X_test = X_test[:, :-1]

    # standardizing data for processing, mean=0, var=1
    X_train_norm, X_test_norm = standardizer(X_train, X_test)

    if clf_name in ["PCA", "IFOREST"]:
        clf = algo_mapping[clf_name](
            contamination=outliers_fraction, random_state=random_state
        )
    else:
        clf = algo_mapping[clf_name](contamination=outliers_fraction)

    clf.fit(X_train_norm)
    test_scores = clf.decision_function(X_test_norm)
    roc = round(roc_auc_score(y_test, test_scores), ndigits=4)
    y_test_predicted = clf.predict(X_test_norm)

    # Building the Plot.
    fig = plt.figure(figsize=(10, 4))

    fig.add_subplot(1, 2, 1)
    X_out, X_in = X_embedded[test_ids[y_test == 1]], X_embedded[test_ids[y_test == 0]]
    plt.scatter(X_in[:, 0], X_in[:, 1], color="blue", marker="^", alpha=0.4)
    plt.scatter(X_out[:, 0], X_out[:, 1], color="orange", marker="h", alpha=0.5)
    plt.title("Ground truth")

    fig.add_subplot(1, 2, 2)
    X_out, X_in = (
        X_embedded[test_ids[y_test_predicted == 1]],
        X_embedded[test_ids[y_test_predicted == 0]],
    )
    plt.scatter(X_in[:, 0], X_in[:, 1], color="blue", marker="^", alpha=0.4)
    plt.scatter(X_out[:, 0], X_out[:, 1], color="orange", marker="h", alpha=0.5)
    plt.title("Predicted")

    sptl = plt.suptitle(
        "Датасет: {}, ROC: {}\nАлгоритм: {}".format(dataset_title[:-4], roc, clf_name),
        y=1.08,
        fontsize=14,
    )
    lgd = plt.legend(
        labels=["Нормальные данные", "Аномальные данные"],
        title="Обозначения",
        shadow=True,
        ncol=1,
        fontsize=12,
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )
    plt.savefig(path, dpi=100, bbox_extra_artists=(lgd, sptl), bbox_inches="tight")

    return filename


def data_overview(file_id, dataset_title):
    mat = db_queries.get_dataframe(file_id)

    filename = "overview_{}.png".format(file_id)
    path = "./images/{}".format(filename)

    mat = mat.drop(["Unnamed: 0", "Index", "id", "Id"], axis=1, errors="ignore")

    y = mat["outlier"].values
    X = mat.drop("outlier", axis=1).values

    X_embedded = TSNE(n_components=2).fit_transform(X)
    X_out, X_in = get_outliers_inliers(X_embedded, y)

    plt.figure(figsize=(6, 6))
    plt.scatter(X_in[:, 0], X_in[:, 1], color="blue", marker="^", alpha=0.4)
    plt.scatter(X_out[:, 0], X_out[:, 1], color="orange", marker="h", alpha=0.5)
    ttl = plt.title(dataset_title[:-4])
    lgd = plt.legend(
        labels=["Нормальные данные", "Аномальные данные"],
        title="Обозначения",
        shadow=True,
        ncol=1,
        fontsize=12,
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )
    plt.subplots_adjust(hspace=0.3)
    plt.savefig(path, dpi=100, bbox_extra_artists=(lgd, ttl), bbox_inches="tight")

    return filename
