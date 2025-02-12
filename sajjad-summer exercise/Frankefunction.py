import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def FrankeFunction(x, y):
    term1 = 0.75 * np.exp( - (0.25 * (9 * x - 2)**2) - 0.25 * ((9 * y - 2)**2))
    term2 = 0.75 * np.exp( - (( 9 * x + 1)**2) / 49.0 - 0.1 * (9 * y + 1))
    term3 = 0.5 * np.exp( - (9 * x - 7)**2 / 4.0 - 0.25 * ((9 * y- 3)**2))
    term4 = - 0.2 * np.exp( - (9 * x - 4)**2 - (9 * y - 7)**2)
    return term1 + term2 + term3 + term4

if __name__=="__main__": 
    
    fig = plt.figure()
    ax = fig.gca(projection = '3d')

    x = np.arange(0, 1, 0.05)
    y = np.arange(0, 1, 0.05)
    x, y = np.meshgrid(x, y)
    z = FrankeFunction(x, y)  + 0.1 * np.random.randn(20, 1)

    surf = ax.plot_surface(x, y, z, cmap = cm.coolwarm, linewidth = 0, antialiased = False)

    ax.set_zlim( - 0.10, 1.40)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink = 0.5, aspect = 5)

    plt.show()