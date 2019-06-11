import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


def norm_generate(size, mean, std):
    data = stats.norm.rvs(size=size, loc=mean, scale=std)
    return data


def norm_params(data):
    """Calculate basic statistics of gaussian data -- mean and standard deviation.

    Parameters
    ----------
    data : np.array
        Input data.

    Returns
    -------
    tuple(float, float)
        (mean, standard deviation).

    """
    var = np.var(data)
    std = np.sqrt(var)
    mean = np.mean(data)
    # res = dict(var=var, std=std, mean=mean)
    return mean, std


def norm_probs(data, mean, std):
    probs = stats.norm.pdf(data, loc=mean, scale=std)
    return probs


def plot_by_probs(data, mean, std):
    probs = norm_probs(data, mean, std)

    plt.figure()
    plt.scatter(np.arange(len(data)), data, c=probs)
    plt.colorbar()
    plt.xlabel('position')
    plt.ylabel('value')
    plt.show()


def plot_outliers_std(data, std_factor=3):
    mean, std = norm_params(data)
    outliers_std = np.array(list(filter(lambda x: abs(x[1] - mean) > std * std_factor, enumerate(data))))

    colors = np.zeros(len(data))
    outliers_std_indexes = outliers_std[:, 0].astype(int)
    colors[outliers_std_indexes] = np.ones(len(outliers_std_indexes))

    plt.figure()
    plt.title('Standard deviation cutoff. factor={}'.format(std_factor))
    plt.scatter(np.arange(len(data)), data, c=colors)
    plt.xlabel('position')
    plt.ylabel('value')
    plt.show()


def plot_outliers_eps(data, eps=1e-5):
    mean, std = norm_params(data)
    probs = norm_probs(data, mean, std)
    outliers_eps = np.array(list(filter(lambda x: x[1] < eps, enumerate(probs))))

    colors = np.zeros(len(data))
    outliers_eps_indexes = outliers_eps[:, 0].astype(int)
    colors[outliers_eps_indexes] = np.ones(len(outliers_eps_indexes))

    plt.figure()
    plt.title('EPS cutoff. eps={}'.format(eps))
    plt.scatter(np.arange(len(data)), data, c=colors)
    plt.xlabel('position')
    plt.ylabel('value')
    plt.show()


def plot_outliers_sign(data, outliers_portion=0.3):
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

    plt.figure()
    plt.title('Sign feature. max portion={}'.format(outliers_portion))
    plt.scatter(np.arange(len(data)), data, c=colors)
    plt.xlabel('position')
    plt.ylabel('value')
    plt.show()
