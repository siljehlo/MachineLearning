import numpy as np

from Frankefunction import FrankeFunction
from design_matrix import design_matrix
from k_fold_CV import k_fold_CV
from plot3d import plot3d
import metrics

# Data
n = 20
x = np.linspace(0, 1, n)
y = np.linspace(0, 1, n)

n = n * n
x, y = np.meshgrid(x, y)
x = np.reshape(x, (n,))
y = np.reshape(y, (n,))
z = FrankeFunction(x, y)

# Parameters
number_of_models = 4
highest_number_of_betas = 27
k = 5

# Regression statistics matrices
MSE_train = np.zeros([number_of_models,])
R2_train = np.zeros([number_of_models,])
MSE_test = np.zeros([number_of_models,])
R2_test = np.zeros([number_of_models,])
Beta_conf_interval = np.zeros([highest_number_of_betas, number_of_models], dtype='O')
Bias2 = np.zeros([number_of_models,])
Variance_error = np.zeros([number_of_models,])

for m in range(number_of_models):
    
    # Polynomial order
    p = m + 2 
    
    # Design matrix
    X = design_matrix(p, x, y) 
    Xm, Xn = np.shape(X) 
    
    # Least squares 
    normal_equation = X.T@X
    B = np.linalg.solve(normal_equation, X.T@z)
    
    # Regression statistics calulations
    zhat = X@B
    MSE_train[m] = metrics.mean_squared_error(z, zhat)
    R2_train[m] = metrics.r2_score(z, zhat)
    Beta_conf_interval[:Xn, m] = metrics.confidance_interval(z, zhat, p, normal_equation, B)
    Bias2[m] = metrics.bias2(z, zhat)
    Variance_error[m] = metrics.variance_error(zhat)
    
    # Cross validation 2-fold
    CV_pred = []
    
    for X_train, X_test, z_train, z_test in k_fold_CV(k, X, z):
        
        # Least squares
        B = np.linalg.solve(X_train.T@X_train, X_train.T@z_train)
        
        # Cross validation predictions 
        CV_pred.append(X_test@B)
    
    # Cross validation regression statistics calulations
    CV_pred = np.reshape(CV_pred, [n,])    
    MSE_test[m] = metrics.mean_squared_error(z, CV_pred)
    R2_test[m] = metrics.r2_score(z, CV_pred)

# Plot model
plot3d(B, p)

