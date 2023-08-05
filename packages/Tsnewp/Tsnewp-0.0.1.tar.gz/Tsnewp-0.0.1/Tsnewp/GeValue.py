import numpy as np


def GeValue(D, Ge=1.0):
    # Pj/i molecule
    P = np.exp(-D * Ge)
    # Pj/i denominator
    sumP = sum(P)
    # new perplexity
    H = np.log(sumP) + Ge * np.sum(D * P) / sumP
    # similarity Pj/i
    P = P / sumP
    return H, P


def sigma_search(data, perplexity=25, max_iters=50, tol=1e-5):
    # initial_values
    m, n = data.shape
    data_sum = (data * data).sum(axis=1)

    # calculate the dot between different case
    D = np.add(-2 * np.dot(data, data.T), data_sum).T + data_sum
    P = np.ones((m, m))
    Ge = np.ones((m, 1))
    logperplexity = np.log(perplexity)

    for i in range(m):
        Gemin = -np.inf
        Gemax = np.inf
        # 除去Pi/i的情况
        Di = D[i, np.concatenate((np.r_[0:i], np.r_[i + 1:m]))]
        # calculate the similarity and entropy
        (thisperplexity, thisp) = GeValue(Di, Ge[i])
        P_diff = thisperplexity - logperplexity
        times = 0
        while P_diff > tol and times <= max_iters:
            # Binary Search for the nearest perplexity
            # Ge means the reciprocal value of sigma ，so if thisperplexity larger than logperplexity ， we should improve Ge ，it equals decreasing the sigma
            if P_diff > 0:
                Gemin = Ge[i]
                if Gemax == np.inf or Gemax == -np.inf:
                    Ge[i] = 2 * Ge[i]
                else:
                    Ge[i] = (Ge[i] + Gemax) / 2
            else:
                Gemmax = Ge[i]
                if Gemin == np.inf or Gemin == -np.inf:
                    Ge[i] = Ge[i] / 2
                else:
                    Ge[i] = (Ge[i] + Gemin) / 2
            (thisperplexity, thisp) = GeValue(Di, Ge[i])
            P_diff = thisperplexity - logperplexity
            times = times + 1
        P[i, np.concatenate((np.r_[0:i], np.r_[i + 1:m]))] = thisp
    return P
