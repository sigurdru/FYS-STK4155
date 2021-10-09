import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split as tts

#Our files
import resampling
import analysis
import utils
import regression
import plot
import utils

"""
IN THIS FILE:
We perform a lot of tests on our implementations. Namely OLS, Rige and bias variance tradeoff.
In order to run the tests, just run the command:
python3 test.py
"""

utils.np.random.seed(7132)
plt.style.use('seaborn')
plt.rc('text', usetex=True)
plt.rc('font', family='DejaVu Sans')
path_plots = '../output/plots'

def f(x, eps=0):
    """
    Returns the function used for testing of the methods, with noise.

    Args:
        x (array): array of x values
        eps (float): size of error
    """
    noise = np.random.normal(0,eps, x.shape)
    value = np.exp(-x**2) + 1.5 * np.exp(-(x-2)**2) + noise
    return value.reshape(-1,1)

def create_design_matrix(x,p):
    """
    Here we create a simple design matrix using a polynomial fit, i.e
    f(x) = a0 + a1*x^2 + a2*x^3 + ... + a(p-1)*x^(p-1)

    Args:
        x(array): array of x values
        p(int): max polynomial degree
    """
    X = np.zeros((len(x),p))
    for i in range(p):
        X[:,i] = x**i
    return X

def test_OLS():
    """
    Here we perform a test on our ordinary least square method
    using sklearn
    """
    #We will divide by zero when taking log :o
    np.seterr(divide='ignore')
    #polynomial degree
    p_max = 16
    p_array = np.arange(1, p_max, 1)
    our_MSE_test = np.zeros(p_max-1)
    our_MSE_train = np.zeros(p_max-1)
    sklearn_MSE_test = np.zeros(p_max-1)
    sklearn_MSE_train = np.zeros(p_max-1)

    #the noise we want
    eps = 0.1
    #number of data points
    n = 100
    #percentage of data used for testing
    ttsplit = 0.2
    #creating data
    x = np.sort(np.random.uniform(-3,3,size=n))
    z = f(x, eps)

    for p in p_array:
        X = create_design_matrix(x, p)
        data, X_train, X_test, z_train, z_test, beta = resampling.NoResampling(X, z, ttsplit, 0, [0],
                                                                           regression.Ordinary_least_squares,
                                                                           scaler=analysis.scale_conv["S"],
                                                                           Testing=True)
        our_MSE_test[p-1] = data["test_MSE"]
        our_MSE_train[p-1] = data["train_MSE"]

        regOLS = LinearRegression(fit_intercept=False)
        regOLS.fit(X_train, z_train)

        OLS_predict_test = regOLS.predict(X_test)
        OLS_predict_train = regOLS.predict(X_train)

        sklearn_MSE_test[p-1] = utils.MSE(z_test, OLS_predict_test)
        sklearn_MSE_train[p-1] = utils.MSE(z_train, OLS_predict_train)


    fig, ax = plt.subplots()
    xlabel = 'Polynomial degree'
    ylabel = r'MSE'
    title = 'Testing of OLS'
    fname = 'Testing_OLS'
    ax.plot(p_array, sklearn_MSE_test, 'r--',label='sklearn MSE test')
    ax.plot(p_array, sklearn_MSE_train, 'b--', label='sklearn MSE train')
    ax.plot(p_array, our_MSE_test, 'ro',label='our MSE test')
    ax.plot(p_array, our_MSE_train, 'bo', label='our MSE train')
    plot.set_ax_info(ax, xlabel, ylabel, title)
    fig.tight_layout()
    print('Plotting OLS test, see ' + fname + '.pdf')
    fig.savefig(plot.os.path.join(path_plots, fname + '.pdf'))
    plt.close()

def test_Ridge():
    """
    Here we perform a test on our Ridge method
    using sklearn
    """
    #We will divide by zero when taking log :o
    np.seterr(divide='ignore')
    #polynomial degree
    p_max = 16
    p_array = np.arange(1, p_max, 1)
    our_MSE_test = np.zeros(p_max-1)
    our_MSE_train = np.zeros(p_max-1)
    sklearn_MSE_test = np.zeros(p_max-1)
    sklearn_MSE_train = np.zeros(p_max-1)
    #the noise we want
    eps = 0.1
    #number of data points
    n = 100
    lmd = 0.2
    #percentage of data used for testing
    ttsplit = 0.2
    #creating data
    x = np.sort(np.random.uniform(size=n))
    z = f(x, eps)
    for p in p_array:
        X = create_design_matrix(x, p)
        data, X_train, X_test, z_train, z_test, beta = resampling.NoResampling(X, z, ttsplit, 0, [lmd],
                                                                               regression.Ridge,
                                                                               scaler=analysis.scale_conv["S"],
                                                                               Testing=True)
        our_MSE_test[p-1] = data["test_MSE"]
        our_MSE_train[p-1] = data['train_MSE']

        regOLS = Ridge(fit_intercept=True)
        regOLS.fit(X_train, z_train)
        OLS_predict_test = regOLS.predict(X_test)
        OLS_predict_train = regOLS.predict(X_train)
        sklearn_MSE_test[p-1] = utils.MSE(z_test, OLS_predict_test)
        sklearn_MSE_train[p-1] = utils.MSE(z_train, OLS_predict_train)
    #Plotting
    fig, ax = plt.subplots()
    xlabel = 'Polynomial degree'
    ylabel = 'MSE'
    title = 'Testing of Ridge regression'
    fname = 'Testing_Ridge'
    ax.plot(p_array, sklearn_MSE_test, 'r--', label='sklearn MSE test')
    ax.plot(p_array, sklearn_MSE_train, 'b--', label='sklearn MSE train')
    ax.plot(p_array, our_MSE_test, 'ro', label='our MSE test')
    ax.plot(p_array, our_MSE_train, 'bo', label='our MSE train')
    plot.set_ax_info(ax, xlabel, ylabel, title)
    fig.tight_layout()
    print('Plotting Ridge test, see ' + fname + '.pdf')
    fig.savefig(plot.os.path.join(path_plots, fname + '.pdf'))
    plt.close()

class params:
    """
    This class is so we can create a series of values our functions use
    """
    def __init__(self, N, P, eps, resampling,
                 tts, resampling_iter, lmb, method,
                 scaling_conv):
        self.num_points = N
        self.polynomial = P
        self.epsilon = eps
        self.resampling = resampling
        self.tts = tts
        self.resampling_iter = resampling_iter
        self.lmb = lmb
        self.method = method
        self.scaling = scaling_conv
        self.dataset = "Test"

def test_BV(N):
    """
    Test bias variance tradeoff using bootstrap
    """
    #Variables we are going to use
    N = N
    maxdegree = 16
    P = np.arange(0,maxdegree,1)
    eps = 0.1
    resampling_m = "Bootstrap"
    ttsplit = 0.2
    resampling_iter = 100
    lmb = [0.1]
    method = "OLS"
    scaling_conv = "S"
    #Using our method
    args = params(N, P, eps,
                resampling_m, ttsplit, resampling_iter,
                lmb, method, scaling_conv)
    our_results = analysis.bias_var_tradeoff(args, testing=True)


    #Using sklearn
    utils.np.random.seed(7132)
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import PolynomialFeatures, StandardScaler
    from sklearn.utils import resample

    x = np.sort(np.random.uniform(-3, 3, size=N)).reshape(-1,1)
    y = f(x, eps)
    error = np.zeros(maxdegree)
    bias = np.zeros(maxdegree)
    variance = np.zeros(maxdegree)
    scaler = StandardScaler()
    x_train, x_test, y_train, y_test = resampling.split_scale(x, y, ttsplit=0.2, scaler=StandardScaler())


    for degree in range(maxdegree):
        model = make_pipeline(PolynomialFeatures(degree=degree), LinearRegression(fit_intercept=False))
        y_pred = np.empty((y_test.shape[0], resampling_iter))
        for i in range(resampling_iter):  # ling_iter):
            x_, y_ = resample(x_train, y_train)
            y_pred[:, i] = model.fit(x_, y_).predict(x_test).ravel()
        error[degree] = np.mean( np.mean((y_test - y_pred)**2, axis=1, keepdims=True) )
        bias[degree] = np.mean( (y_test - np.mean(y_pred, axis=1, keepdims=True))**2 )
        variance[degree] = np.mean( np.var(y_pred, axis=1, keepdims=True) )

    fig, ax = plt.subplots()

    xlabel = 'Polynomial degree'
    ylabel = 'Bias, variance and MSE'
    title = 'Bias Variance Tradeoff comparison for Bootstrap. Using N={}'.format(N)
    fname = 'Testing_OLS_BV_compare' \
            + '_n' + str(N)

    ax.plot(P, error, label='SKlearn MSE')
    ax.plot(P, variance, label='SKlearn Variance')
    ax.plot(P, bias, label='SKlearn Bias')

    ax.plot(P, our_results["test_errors"], '--', label='Test MSE')
    ax.plot(P, our_results["test_vars"], '--', label='Test Variance')
    ax.plot(P, our_results["test_biases"], '--', label='Test Bias')
    plot.set_ax_info(ax, xlabel, ylabel, title)
    fig.tight_layout()
    print('Plotting BV comparison, see ' + fname + '.pdf')
    fig.savefig(plot.os.path.join(path_plots, fname + '.pdf'))


def plot_test_func():
    """
    Here save the plot of the test data along with the analytical test function.
    """
    n = 100
    eps = 0.1
    x = np.sort(np.random.uniform(size=n))
    y_nonoise = f(x)
    y_withnoise = f(x, eps)
    fig, ax = plt.subplots()
    xlabel = '$x$'
    ylabel = '$y$'
    title = 'Our test data plotted with the analytical function'
    fname = 'Testing_data'
    ax.plot(x, y_nonoise, label='Analytical function')
    ax.plot(x, y_withnoise, label='Testing data')
    plot.set_ax_info(ax, xlabel, ylabel, title)
    fig.tight_layout()
    print('Plotting testing function, see ' + fname + '.pdf')
    fig.savefig(plot.os.path.join(path_plots, fname + '.pdf'))
    plt.close()

plot_test_func()
test_OLS()
test_Ridge()
# test_BV(169)
# test_BV(170)
