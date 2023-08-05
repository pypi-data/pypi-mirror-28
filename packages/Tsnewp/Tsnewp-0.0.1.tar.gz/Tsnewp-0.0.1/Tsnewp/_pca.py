import numpy as np


def _pca(data, no_dim=50):
    data = data - data.mean(axis=0)
    _, m = np.linalg.eig(np.dot(data.T, data))
    data = np.dot(data, m[:, :no_dim])
    return data.real
