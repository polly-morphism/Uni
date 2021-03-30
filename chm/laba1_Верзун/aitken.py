import numpy as np
import matplotlib.pyplot as plt


def func(x):
    return np.exp(2*x + 1)

X = -0.5
n = 3
xi = np.linspace(X-1, X+1, n)
x_and_xi = X- xi

yi = func(xi)
polinoms = []
first_nums_in_polinoms = []

def polinom_calc(x, y, count):
    cur_polinom_val = []
    for i in range(len(x) - count):
        cur_polinom_val.append((x[i] * y[i + 1] - x[i + count] * y[i]) / abs(x[i + count] - x[i]))
    polinoms.append(cur_polinom_val)
    first_nums_in_polinoms.append(cur_polinom_val[0])

polinom_calc(x_and_xi, yi, 1)

for i in range(n-2):
    polinom_calc(x_and_xi, polinoms[i], i+2)

difference = np.diff(first_nums_in_polinoms)
difference = np.absolute(difference)
min_value = difference.argmin()
print('Функція f(x) = exp(2x + 1)')

real_val = func(X)
n_val = first_nums_in_polinoms[min_value]
error = np.absolute(real_val - n_val)
print(f'f(x): {real_val}\nE(x): {n_val}\nПохибка: {error}\n')
