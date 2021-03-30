import numpy as np
import matplotlib.pyplot as plt
from sympy import *

def func(x):
    return np.exp(2*x + 1)


def Newton(func, x, n):
    xi = np.linspace(x-1, x+1, n)
    h = abs(xi[1] - xi[0])
    yi = func(xi)
    N = np.diff(yi, n=0)[0]
    for i in range(1, n):
        brackets = 1
        for j in range(i):
            brackets *= (x - xi[j])
        N += (np.diff(yi, n=i)[0] / np.math.factorial(i) / h**i * brackets)
    return N

def poli_info(func, X, n):
    xi = np.linspace(X-1, X+1, n)
    h = abs(xi[1] - xi[0])
    yi = func(xi)
    x = Symbol('x')
    pol = np.diff(yi, n=0)[0]
    for i in range(1, n):
        brackets = 1
        for j in range(i):
            brackets *= (x - xi[j])
        pol += (np.diff(yi, n=i)[0] / np.math.factorial(i) / h**i * brackets)

    pol = expand(pol)
    print(f'N(x)={pol}')
    print(f'N({X})={pol.subs(x, X)}')


if __name__ == '__main__':
    X = -0.5
    n = 3

    real_val = func(X)
    n_val = Newton(func, X, n)
    error = np.absolute(real_val - n_val)

    print('Функція f(x) = exp(2x + 1)')
    print(f'f({X}): {real_val}\nN({X}): {n_val}\nПохибка: {error}\n')

    poli_info(func, X, n)
