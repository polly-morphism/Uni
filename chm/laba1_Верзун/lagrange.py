import numpy as np
import matplotlib.pyplot as plt
from pylab import *


def func(x):
    return np.exp(2*x + 1)

def Lagranzh(func, x, n):
    xi = np.linspace(x-1, x+1, n)
    yi = func(xi)
    L = 0
    for i in range(n):
        Li = 1
        for j in range(n):
            if i == j:
                continue
            else:
                Li = Li * (x - xi[j]) / (xi[i] - xi[j])
        L = L + (yi[i] * Li)
    return L

if __name__ =='__main__':
    X = -0.5
    n = 3

    real_val = func(X)
    l_val = Lagranzh(func, X, n)
    error = np.absolute(real_val - l_val)

    print('Функція f(x) = exp(2x + 1)')
    print(f'f(x): {real_val}\nL(x): {l_val}\nПохибка: {error}\n')
