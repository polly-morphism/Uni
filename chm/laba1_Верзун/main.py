import numpy as np
import matplotlib.pyplot as plt
from lagrange import Lagranzh
from newton import Newton

def func(x):
    return np.exp(2*x + 1)

X = -0.5
n = 3

real_val = func(X)

print('Функція f(x) = exp(2x + 1)')
print(f'f({X}) = {real_val}\n')

choice = input('Виберіть метод (1: Ньютон; 2: Лагранж): ')
if choice == '1':
    n_val = Newton(func, X, n)
    error = np.absolute(real_val - n_val)
    r_error  = error / real_val
    print(f'f(x): {real_val}\nN(x): {n_val}\nПохибка: {error}\n')


    x_graph_func = np.linspace(X-1, X+1, 100)
    y_graph_func = [func(x) for x in x_graph_func]
    x_graph_newton = np.linspace(X-1, X+1, 100)
    y_graph_newton = [Newton(func, x_graph_newton[i], n) for i in range(len(x_graph_newton))]
    xi = np.linspace(X-1, X+1, n)
    plt.plot(xi, func(xi), 'o', color="green")
    plt.plot(x_graph_func, y_graph_func, color="red")
    plt.plot(x_graph_newton, y_graph_newton, color="blue")
    plt.title("Метод Ньютона")
    plt.legend(('Вузли', 'Графік функції', 'Графік поліному'))
    plt.grid(True)
    plt.show()

elif choice == '2':
    l_val = Lagranzh(func, X, n)
    error = np.absolute(real_val - l_val)
    r_error  = error / real_val
    print(f'f(x): {real_val}\nN(x): {l_val}\nПохибка: {error}\n')

    x_graph_func = np.linspace(X-1, X+1, 100)
    y_graph_func = [func(x) for x in x_graph_func]
    x_graph_pol = np.linspace(X-1, X+1, 100)
    y_graph_pol = [Lagranzh(func, x_graph_pol[i], n) for i in range(len(x_graph_pol))]
    xi = np.linspace(X-1, X+1, n)
    plt.plot(xi, func(xi), 'o', color="green")
    plt.plot(x_graph_func, y_graph_func, color="red")
    plt.plot(x_graph_pol, y_graph_pol, color="blue")
    plt.title("Поліном Лагранжа")
    plt.legend(('Вузли', 'Графік функції', 'Графік поліному'))
    plt.grid(True)
    plt.show()
