import numpy as np
from ._pca import _pca
from .GeValue import  sigma_search


class Tsnewp(object):
    '''
    param : is_reduce_dim : if is_reduce_dim = 1 use pca to reshape the initial data to a low dim data
    param : reduce_dim : if is_reduce_dim = 1 then change the reduce_dim param
    param : out_dim : tsne output data dim
    param : perplexity : change the initial data in the same initial perplexity
    param : max_iters : max iters of the training step
    param : initial_momentum : the initial momentum should be small
    param : final_momentum : during the calculating process, should improve the momentum to improve the speed
    param : eta : learning rate

    Reference:
        Maaten, L., & Hinton, G. (2008). Visualizing data using t-SNE. Journal of Machine Learning Research.
    '''

    def __init__(self, is_reduce_dim=0, reduce_dim=None, out_dim=2, perplexity=30.0, max_iters=1000):
        self.is_reduce_dim = is_reduce_dim
        self.reduce_dim = reduce_dim
        self.out_dim = out_dim
        self.perplexity = perplexity
        self.max_iters = max_iters

    def transform(self, data=None, initial_momentum=0.5, final_momentum=0.8, eta=500, min_gain=0.01):
        if self.is_reduce_dim:
            if isinstance(self.reduce_dim, int):
                data = _pca(data, self.reduce_dim)
            else:
                raise ValueError('reduce_dim should be the format of int')
        (n, m) = data.shape
        max_iters = self.max_iters
        out_dim = self.out_dim
        # random a low dim distribution
        Y = np.random.randn(n, out_dim)
        dY = np.zeros((n, out_dim))
        iY = np.zeros((n, out_dim))
        gains = np.ones((n, out_dim))

        # Compute Pj/i
        P = sigma_search(data, perplexity=self.perplexity)
        # Symmetric SNE
        P = P + np.transpose(P)
        # trick : make scale for early compression
        P = P / np.sum(P)
        # improve the P to increase the speed of the calculation by multiplying by 4
        P = P * 4
        P = np.maximum(P, 1e-10)

        # got the min loss
        for iter in range(max_iters):
            # Compute pairwise affinities
            sum_Y = (Y * Y).sum(axis=1)
            # crowding solving : t - distribution
            num = 1 / (1 + np.add(-2 * np.dot(Y, Y.T), sum_Y).T + sum_Y)
            # keep the Pi/i zero，it will be ignored later
            num[range(n), range(n)] = 0
            Q = num / np.sum(num)
            Q = np.maximum(Q, 1e-10)

            # calculate gradient
            PQ = P - Q
            for i in range(n):
                # ∑(pij-qij)(1 + (yi-yj)^2)^(-1)(yi-yj)
                dY[i, :] = (np.tile(PQ[:, i] * num[:, i], (out_dim, 1)).T * (Y[i, :] - Y)).sum(0)

            # Perform the update
            if iter < 20:
                momentum = initial_momentum
            else:
                momentum = final_momentum
            # adjust the momentum 'gains'  increase if the gradient is the opposite direction with the last time result Y
            gains = (gains + 0.2) * ((dY > 0) != (iY > 0)) + (gains * 0.8) * ((dY > 0) == (iY > 0))
            gains[gains < min_gain] = min_gain

            # update the result with the momentum,gradient,Cumulative attenuation gradient and the learning rate
            iY = momentum * iY - eta * (gains * dY)
            Y = Y + iY
            Y = Y - Y.mean(0)
            # Stop trick of multiplying by 4 about P-values
            if iter == 100:
                P = P / 4
        # Return solution
        return Y
