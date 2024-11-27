## Slice wasserstein estimation

import numpy as np
from scipy.stats import norm

def slice_wasserstein_gaussian(mu_1, mu_2, sigma, n_samples=100, n_slices=100, n_replications=100, confidence=0.95):
    """
    MC estimation of the slice Wasserstein distance between two Gaussian distributions with means mu_1 and mu_2 and standard deviation sigma
    """
    
    def sphere(d, n_slices):
        S = np.random.randn(n_slices, d)
        S /= np.linalg.norm(S, axis=1, keepdims=True)
        return S

    def diese(v, sample):
        projection = sample @ v
        mu = np.mean(projection)
        sigma = np.var(projection)
        return mu, sigma

    def w_operator(m, sigma, sigma_square, epsilon=1e-8):
        if sigma < epsilon:
            W = np.abs(m)
        else:
            inside_phi_N = - np.abs(m) / np.abs(sigma)
            phi_N = norm.cdf(inside_phi_N)
            left = np.abs(m) * (1 - 2 * phi_N)
            inside_exp = - m**2 / (2 * sigma_square)
            right = np.abs(sigma) * np.sqrt(2 / np.pi) * np.exp(inside_exp)
            W = left + right
        return W

    SWs = []

    d = sigma.shape[0]

    rng = np.random.default_rng()

    for replication in range(n_replications):

        Ws = []

        samples_1 = rng.multivariate_normal(mu_1, sigma, n_samples)
        samples_2 = rng.multivariate_normal(mu_2, sigma, n_samples)

        S = sphere(d, n_slices)

        for v in S:
            m_1, sigma_1 = diese(v, samples_1)
            m_2, sigma_2 = diese(v, samples_2)

            m_y = m_1 - m_2
            sigma_y_square = (sigma_1 - sigma_2) ** 2
            sigma_y = np.sqrt(sigma_y_square)

            W = w_operator(m_y, sigma_y, sigma_y_square)

            Ws.append(W)

        SW = np.mean(Ws)
        SWs.append(SW)

    SW_mean = np.mean(SWs)
    SW_std = np.std(SWs)
    margin_of_error = norm.ppf(confidence / 2) * SW_std / np.sqrt(n_samples)
    CI = (SW_mean - margin_of_error, SW_mean + margin_of_error)

    return SW_mean, SW_std, margin_of_error, CI

def slice_wasserstein_generic(X, Y, n_samples=100, n_slices=100, n_us=100, n_replications=100, confidence=0.95):
    """
    Compute the sliced Wasserstein distance between the empirical distribution of two datasets X and Y
    X and Y are numpy arrays of dimension n_X x d and n_Y x d where n is the number of samples and d is the dimension of the samples
    n_samples is the number of uniform samples used to estimate the sliced Wasserstein distance
    n_slices is the number of slices (random direction) used to estimate the sliced Wasserstein distance
    """

    def sphere(d, n_slices):
        S = np.random.randn(n_slices, d)
        S /= np.linalg.norm(S, axis=1, keepdims=True)
        return S

    def diese(v, sample):
        projection = sample @ v
        return projection

    def w_operator(proj_1, proj_2, n_us=n_us, epsilon=1e-8):
        us = rng.uniform(low=0, high=1, size=n_us)
        W = 0
        for u in us:
            W += np.abs(np.quantile(proj_1, u) - np.quantile(proj_2, u))
        W /= n_us
        return W

    SWs = []

    d = X.shape[1]
    n_x = X.shape[0]
    n_y = Y.shape[0]

    rng = np.random.default_rng()

    for replication in range(n_replications):

        Ws = []

        x_samples_id = rng.integers(low=0, high=n_x, size=n_samples)
        x_samples = X[x_samples_id, :]
        y_samples_id = rng.integers(low=0, high=n_y, size=n_samples)
        y_samples = Y[y_samples_id, :]

        S = sphere(d, n_slices)

        for v in S:
            proj_x = diese(v, x_samples)
            proj_y = diese(v, y_samples)

            W = w_operator(proj_x, proj_y)

            Ws.append(W)

        SW = np.mean(Ws)
        SWs.append(SW)

    SW_mean = np.mean(SWs)
    SW_std = np.std(SWs)
    margin_of_error = norm.ppf(confidence / 2) * SW_std / np.sqrt(n_samples)
    CI = (SW_mean - margin_of_error, SW_mean + margin_of_error)

    return SW_mean, SW_std, margin_of_error, CI
