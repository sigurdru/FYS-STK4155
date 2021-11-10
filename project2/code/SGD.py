import numpy as np
import utils 



def SGD(X, z, args, beta, eta, batch_size, lmb=0, gamma=0):
    """
    Performs OLS regression using SGD

    Args:
        X, tuple: design matrix (train, test)
        z1, tuple: datapoints (train, test)
        args, argparse
        beta, 1darray: parameters
        eta, float: learning rate
        gamma, float: Momentum parameter
        lmb, float: For Ridge regression
    Returns:
        total_gradient 1darray: total gradient
    """

    n = int(X[0].shape[0])  # number of datapoints for training
    if batch_size == 0:
        M = n
    else:
        M = int(batch_size)  # size of minibatch
    m = n // M
    
    v = 0
    X_train, X_test = X
    z_train, z_test = z

    inds = np.arange(0, n)

    MSE_train = np.zeros(args.num_epochs)
    MSE_test  = np.zeros(args.num_epochs)


    eta_0 = eta # To be used for learning schedule 

    for epoch_i in range(args.num_epochs):
        # Initialize randomized training data for epoch
        np.random.shuffle(inds)
        X_train_shuffle = X_train[inds]
        z_train_shuffle = z_train[inds]

        for i in range(0, n, M):
            # Loop over mini batches

            xi = X_train_shuffle[i:i+M]
            zi = z_train_shuffle[i:i+M]


            gradient = 2 * xi.T @ ((xi @ beta)-zi.T[0]) / M \
                        + 2 * lmb * beta
            # print(gradient)
            # input()
            v = v * gamma + eta * gradient
            beta = beta - v

        train_pred = (X_train @ beta)
        test_pred = (X_test @ beta)

        tr_mse = utils.MSE(z_train.T[0], train_pred)
        te_mse = utils.MSE(z_test.T[0], test_pred)
        
        MSE_train[epoch_i] = tr_mse if tr_mse < 1 else np.nan
        MSE_test[epoch_i] = te_mse if te_mse < 1 else np.nan

        # eta = learning_schedule(epoch_i*m + i,args)

    return MSE_train, MSE_test, beta 


def SGDL(X, z, W, args, eta, batch_size, lmb=0, gamma=0):
    """
    Stochastic gradient decent for logistic regression

    Args:
        X, tuple: design matrix (train, test)
        z1, tuple: datapoints (train, test)
        args, argparse
        W, 1darray: weights and biases
        eta, float: learning rate
        gamma, float: Momentum parameter
        lmb, float: For Ridge regression
    Returns:
        accuracy_train, 1d array: accuuacy score for train data
        accuracy_test, 1d array: accuuacy score for test data
        W, 1d array: weights and biases
    """
    #initialize
    X_train, X_test = X
    z_train, z_test = z
    n_points = np.shape(X_train)[0]
    v = 0

    inds = np.arange(0, n_points)

    #Setup accuracy's
    accuracy_train = np.zeros(args.num_epochs)
    accuracy_test = np.zeros(args.num_epochs)

    eta_0 = eta  # To be used for learning schedule

    # train_pred = output_activation(X_train @ W)
    # train_pred_bool = np.where(train_pred < 0.5, 0, 1)
    # a = utils.accuracy_score(train_pred_bool, z_train)

    # test_pred = output_activation(X_test @ W)
    # test_pred_bool = np.where(test_pred < 0.5, 0, 1)
    # print(test_pred_bool, z_test)
    # b = utils.accuracy_score(test_pred_bool, z_test)
    # print(a)
    # print(b)
    # exit()

    for epoch_i in range(args.num_epochs):
        # Initialize randomized training data for epoch
        np.random.shuffle(inds)
        X_train_shuffle = X_train[inds]
        z_train_shuffle = z_train[inds]

        for i in range(0, n_points, batch_size):
            # Loop over mini batches

            xi = X_train_shuffle[i:i+batch_size]
            zi = z_train_shuffle[i:i+batch_size]
            gradient = xi.T@(output_activation(xi@W) - zi)
            v = v * gamma + eta * gradient
            W = W - v
        train_pred = output_activation(X_train @ W)
        test_pred = output_activation(X_test @ W)
        train_pred_bool = np.where(train_pred<0.5, 0, 1)
        test_pred_bool = np.where(test_pred<0.5, 0, 1)
        accuracy_train[epoch_i] = utils.accuracy_score(train_pred_bool, z_train)
        accuracy_test[epoch_i] = utils.accuracy_score(test_pred_bool, z_test)
    
    import matplotlib.pyplot as plt
    plt.plot(accuracy_test, label='test')
    plt.plot(accuracy_train, label='train')
    plt.legend()
    plt.show()
    exit()    
    return accuracy_train, accuracy_test, W


def output_activation(s):
    """
    Output activation for SGDL
    """
    return (1/(1+np.exp(-s)))



def RidgeSG():
    return None


def learning_schedule(t, args):
    t0 = 10
    t1 = 1
    return t0/(t+t1)

