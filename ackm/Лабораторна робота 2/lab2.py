import math

N = 40
h = 0.01
x_data = [0.2, 1]
f = lambda x: math.sqrt(4 - x ** 2) / x
F = lambda x: math.sqrt(4 - x ** 2) - 2 * math.log((2 + math.sqrt(4 - x ** 2)) / x)

newton_leibniz = lambda B, A, func: func(B) - func(A)


def f_by_step(x_start, func, step, n):
    return [func(x_start + idx * step) for idx in range(n + 1)]


print("Дифференціювання методом многочленів Лагранжа")


def lagrange_polinom(f_arr, i, step, n):
    if i == 0:
        return (-3 * f_arr[i] + 4 * f_arr[i + 1] - f_arr[i + 2]) / (2 * step)
    elif i == n:
        return (f_arr[i - 2] - 4 * f_arr[i - 1] + 3 * f_arr[i]) / (2 * step)
    else:
        return (f_arr[i + 1] - f_arr[i - 1]) / (2 * step)


def lagrange(func, interval, step, x):
    x_start, x_end = interval
    n = int((x_end - x_start) / step)
    f_arr = f_by_step(x_start, func, step, n)

    for idx in range(n):
        if x_start + idx * step <= x and x < x_start + (idx + 1) * step:
            return lagrange_polinom(f_arr, idx, step, n)


x_ = 0.5
result = lagrange(F, x_data, h, x_)
real_result = f(x_)
print(f"Iстинне значення :  {real_result}; Отримане значення:  {result}")
print(
    f"Абсолютна похибка:  {abs(result-real_result)};  Вiдносна похибка: {abs(result-real_result) / real_result * 100} %"
)

print("Інтегрування методом Сімпсона")


def simpson(func, interval, n):
    x_start, x_end = interval

    step = (x_end - x_start) / n

    # Odd
    summ_e_o = 0
    x = x_start + step
    for i in range(n // 2):
        summ_e_o += 4 * func(x)
        x += 2 * step

    # Even
    x = x_start + 2 * step
    for j in range(n // 2 - 1):
        summ_e_o += 2 * func(x)
        x += 2 * step

    return step * (func(x_start) + func(x_end) + summ_e_o) / 3


result = simpson(f, x_data, 2 * N)
real_result = newton_leibniz(*x_data[::-1], F)
print(
    f"Iстинне значення iнтегралу:  {real_result};  Наближене за {N} промiжкiв значення:  {result}"
)
print(
    f"Абсолютна похибка:  {abs(result-real_result)};  Вiдносна похибка: {abs(result-real_result) / real_result * 100} %"
)
