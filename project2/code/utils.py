import numpy as np
import imageio

def get_features(i):
    """ Returns the number of features of the design matrix for polynomial degree i """
    return (i + 1) * (i + 2) // 2

def load_data(args):
    """
    Creates / loads specified dataset.
    3 possibile datasets:
        Franke:  Bivariate analytic function we will study
        Test:    Simpler exponential func to test implementation of methods towards scikit-learn
        SRTM:    Real-world terrain data loaded from file
    Args:
        args (argparse): object to store runtime args, specifies dataset and size
    Returns
        x, y (2darray): uniformly drawn numbers in domain (0, 1)
        z    (2darray): function values
    """
    N = args.num_points
    if args.dataset == "Franke":
        x = np.sort(np.random.uniform(size=N))
        y = np.sort(np.random.uniform(size=N))
        x, y = np.meshgrid(x, y)
        z = FrankeFunction(x, y, eps=args.epsilon)

    elif args.dataset == "SRTM":
        if args.data_file is None:
            path = "./../DataFiles/SRTM_data_Norway_1.tif"
        else:
            path = args.data_file

        # numbers stolen from other group, can be changed
        xstart = 50
        ystart = 50

        terrain = imageio.imread(path)
        # to not deal with too large image, only NxN
        if N != 0:
            # Plot entire terrain map by setting N=0
            terrain = terrain[xstart: xstart + N, ystart: ystart + N]
        nx, ny = terrain.shape
        x = np.sort(np.random.uniform(size=nx))
        y = np.sort(np.random.uniform(size=ny))
        x, y = np.meshgrid(x, y)

        z = terrain.ravel().reshape(-1, 1) / np.max(terrain)

    return x, y, z

def FrankeFunction(x, y, eps=0):
    """
    Franke Function with noise.

    Parameters:
        x, y: array-like
            x,y-values
        eps0: flaot
            scale value for noise. Defaults to 0
    Returns:
        z: ndarray
            z-values
    """
    term1 = 0.75*np.exp(-(0.25*(9*x-2)**2) - 0.25*((9*y-2)**2))
    term2 = 0.75*np.exp(-((9*x+1)**2)/49.0 - 0.1*(9*y+1))
    term3 = 0.5*np.exp(-(9*x-7)**2/4.0 - 0.25*((9*y-3)**2))
    term4 = -0.2*np.exp(-(9*x-4)**2 - (9*y-7)**2)
    noise = eps * np.random.normal(size=x.shape)
    return (term1 + term2 + term3 + term4 + noise).ravel().reshape(-1, 1)


def create_X(x, y, n, intercept=True):
    """
    Sets up design matrix

    Parameters:
        x, y: array-like
            Are flattened if not already
        n: int
            max polynomial degree
    Returns:
        X: 2darray
            Design matrix. Includes intercept.
    """
    if type(y) == int:
        X = np.zeros((len(x), n+1))
        for i in range(n+1):
            X[:, i] = x**i
        if intercept:
            return X
        else:
            return X[:, 1:]

    if not 1 in x.shape:
        x = np.ravel(x)
        y = np.ravel(y)

    N = len(x)
    l = get_features(n)  # Number of elements in beta
    X = np.ones((N, l))

    for i in range(1, n + 1):
        q = i * (i + 1) // 2
        for k in range(i + 1):
            X[:, q + k] = (x ** (i - k)) * (y ** k)
    if intercept:
        return X
    else:
        return X[:, 1:]