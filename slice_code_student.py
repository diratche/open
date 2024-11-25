## Slice wasserstein estimation

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def slice_wasserstein_gaussian(mu_1,mu_2,sigma,n_samples=100):
"""
MC estimation of the slice Wasserstein distance between two Gaussian distributions with means mu_1 and mu_2 and standard deviation sigma
"""
return 

def slice_wasserstein_generic(X,Y,n_samples=100,n_slices=100):
    """
    Compute the sliced Wasserstein distance between the empirical distribution of two datasets X and Y
    X and Y are numpy arrays of dimension n_X x d and n_Y x d where n is the number of samples and d is the dimension of the samples
    n_samples is the number of uniform samples used to estimate the sliced Wasserstein distance
    n_slices is the number of slices (random direction) used to estimate the sliced Wasserstein distance
    """
    return 
